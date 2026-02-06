# -*- coding: utf-8 -*-
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Any
import logging
from django.conf import settings
from django.db import connection, transaction, models
from django.db.utils import OperationalError
from utils.permissions import IsStaffUser, IsAdminUser
from utils.response import success_response, error_response
from rooms.models import Room
from patients.models import Patient
from .models import BedAssignment
from users.models import StaffUser
from tasks.models import Task as WorkTask, TaskAssignment
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

logger = logging.getLogger(__name__)

class BedViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        return [IsAuthenticated()]
    
    def list(self, request):
        """获取所有床位列表"""
        try:
            self._log_api_request(request, action_name="list")
            beds_data = self._get_all_beds_data()
            resp = success_response(data=beds_data)
            self._log_api_response(request, action_name="list", status_code=200, data_preview={"beds": len(beds_data)})
            return resp
        except OperationalError as e:
            logger.exception("Database error in bed list")
            return error_response(code=500, message="数据库错误", errors={"type": "OperationalError", "detail": str(e)})
        except Exception as e:
            logger.exception("Unhandled error in bed list")
            return error_response(code=500, message="服务器内部错误", errors={"type": type(e).__name__, "detail": str(e)})

    def _get_all_beds_data(self):
        rooms_qs = Room.objects.all()
        logger.info("bed_scheduling rooms query sql=%s", str(rooms_qs.query))
        rooms = list(rooms_qs)
        if connection.queries:
            logger.info("bed_scheduling last_sql=%s", connection.queries[-1].get("sql"))
            logger.info("bed_scheduling last_sql_time=%s", connection.queries[-1].get("time"))
        logger.info("bed_scheduling rooms_count=%s", len(rooms))
        beds_data = []
        
        for room in rooms:
            # 默认每个房间4个床位
            for i in range(1, 5):
                bed_val = getattr(room, f'bed{i}')
                status = 'occupied' if bed_val else 'available'
                
                # 构造床位数据
                bed_info = {
                    'id': f"{room.pk}-{i}", # 构造唯一ID
                    'room_number': room.room_number,
                    'bed_id': str(i),
                    'building': '', # 暂无
                    'floor': 1,     # 默认
                    'status': status,
                    'patient': None, # 暂时无法关联到Patient对象，除非查询
                    'elderly_name': bed_val if status == 'occupied' else None,
                    # 为了兼容前端字段
                    'roomNumber': room.room_number,
                    'bedNumber': str(i),
                    'elderlyId': None,
                    'elderlyName': bed_val if status == 'occupied' else None,
                    'lastUpdated': room.updated_at.isoformat() if room.updated_at else None
                }
                beds_data.append(bed_info)
        if beds_data:
            logger.info("bed_scheduling beds_preview=%s", beds_data[:3])
        else:
            logger.info("bed_scheduling beds_preview=[]")
        return beds_data

    @action(detail=False, methods=['get'])
    def status(self, request):
        """获取床位状态汇总"""
        try:
            self._log_api_request(request, action_name="status")
            beds_data = self._get_all_beds_data()
            
            # 统计各种状态的床位数量
            total_count = len(beds_data)
            available_count = sum(1 for b in beds_data if b['status'] == 'available')
            occupied_count = sum(1 for b in beds_data if b['status'] == 'occupied')
            # cleaning/maintenance 暂时不支持，设为0
            cleaning_count = 0
            maintenance_count = 0
            
            payload = {
                'totalBeds': total_count,
                'available': available_count,
                'occupied': occupied_count,
                'cleaning': cleaning_count,
                'maintenance': maintenance_count,
                'beds': beds_data
            }
            resp = success_response(data=payload)
            self._log_api_response(
                request,
                action_name="status",
                status_code=200,
                data_preview={
                    "totalBeds": total_count,
                    "available": available_count,
                    "occupied": occupied_count,
                    "cleaning": cleaning_count,
                    "maintenance": maintenance_count,
                    "beds": len(beds_data),
                },
            )
            return resp
        except OperationalError as e:
            logger.exception("Database error in bed status")
            return error_response(code=500, message="数据库错误", errors={"type": "OperationalError", "detail": str(e)})
        except Exception as e:
            logger.exception("Unhandled error in bed status")
            return error_response(code=500, message="服务器内部错误", errors={"type": type(e).__name__, "detail": str(e)})
    
    @action(detail=False, methods=['post'])
    def match(self, request):
        """智能匹配床位"""
        try:
            self._log_api_request(request, action_name="match", body_preview=request.data)
            nursing_level = request.data.get('nursing_level')

            all_beds = self._get_all_beds_data()
            available_beds = [b for b in all_beds if b['status'] == 'available']

            matched_beds = []
            for bed in available_beds:
                match_score = 50

                if nursing_level == 'level1':
                    match_score += 20
                elif nursing_level == 'level2':
                    match_score += 15
                elif nursing_level == 'level3':
                    match_score += 10
                elif nursing_level == 'special':
                    match_score += 25

                match_score = min(100, max(0, match_score))

                matched_beds.append({
                    'id': bed['id'],
                    'roomNumber': bed['room_number'],
                    'bedNumber': bed['bed_id'],
                    'building': bed['building'],
                    'floor': bed['floor'],
                    'matchScore': match_score,
                    'reason': '基础匹配'
                })

            matched_beds.sort(key=lambda x: x['matchScore'], reverse=True)
            recommended_bed = matched_beds[0] if matched_beds else None

            payload = {'matchedBeds': matched_beds, 'recommendedBed': recommended_bed}
            resp = success_response(data=payload)
            self._log_api_response(
                request,
                action_name="match",
                status_code=200,
                data_preview={"matchedBeds": len(matched_beds), "hasRecommended": recommended_bed is not None},
            )
            return resp
        except OperationalError as e:
            logger.exception("Database error in bed match")
            return error_response(code=500, message="数据库错误", errors={"type": "OperationalError", "detail": str(e)})
        except Exception as e:
            logger.exception("Unhandled error in bed match")
            return error_response(code=500, message="服务器内部错误", errors={"type": type(e).__name__, "detail": str(e)})

    def _log_api_request(self, request, action_name: str, body_preview: Any = None) -> None:
        try:
            logger.info(
                "api_request action=%s method=%s path=%s query_params=%s",
                action_name,
                getattr(request, "method", None),
                getattr(request, "path", None),
                dict(getattr(request, "query_params", {}) or {}),
            )
            if body_preview is not None:
                logger.info("api_request_body action=%s body=%s", action_name, body_preview)
        except Exception:
            logger.exception("Failed to log api request")

    def _log_api_response(self, request, action_name: str, status_code: int, data_preview: Any = None) -> None:
        try:
            logger.info(
                "api_response action=%s method=%s path=%s status_code=%s data_preview=%s",
                action_name,
                getattr(request, "method", None),
                getattr(request, "path", None),
                status_code,
                data_preview,
            )
        except Exception:
            logger.exception("Failed to log api response")

    @action(detail=True, methods=['patch'])
    def set_status(self, request, id=None):
        """释放床位或更新状态"""
        try:
            self._log_api_request(request, action_name="set_status", body_preview=request.data)
            
            if id is None:
                return error_response(code=400, message="未提供床位ID")

            # id 格式为 "room_pk-bed_index"，例如 "1-2"
            try:
                room_pk, bed_index = id.split('-')
                bed_index = int(bed_index)
            except (ValueError, AttributeError):
                return error_response(code=400, message="无效的床位ID格式")
            
            try:
                room = Room.objects.get(pk=room_pk)
            except Room.DoesNotExist:
                return error_response(code=404, message="房间不存在")
            
            new_status = request.data.get('status')
            
            if new_status == 'available':
                field_name = f'bed{bed_index}'
                if not hasattr(room, field_name):
                    return error_response(code=400, message=f"无效的床位索引: {bed_index}")

                room_number = str(room.room_number)
                bed_id = str(bed_index)

                with transaction.atomic():
                    # 释放床位：清空对应的 bedX 字段
                    setattr(room, field_name, '')
                    room.save()

                    # 查找并结束关联的分配记录
                    active_assignments = BedAssignment.objects.filter(
                        room=room,
                        bed_number=str(bed_index),
                        status='active'
                    )
                    
                    for assignment in active_assignments:
                        assignment.status = 'completed'
                        assignment.release_date = timezone.now()
                        assignment.save()
                        
                        # 更新老人信息
                        if assignment.elderly:
                            assignment.elderly.room = None
                            assignment.elderly.bed_id = None
                            assignment.elderly.save()

                    # 同步清空院民床位信息，避免 patients_patient.bed_id 仍残留
                    (
                        Patient.objects
                        .filter(room=room_number, bed_id=bed_id)
                        .update(room=None, bed_id=None)
                    )

                self._log_api_response(request, action_name="set_status", status_code=200, data_preview="Bed released")
                return success_response(message="床位已释放")
            else:
                # 暂时只支持释放（变为空闲），暂不支持直接设置为 occupied（需通过分配流程）
                return error_response(code=400, message="目前仅支持释放床位（status=available）")

        except Exception as e:
            logger.exception("Error in set_status")
            return error_response(code=500, message="服务器内部错误", errors={"detail": str(e)})

class BedAssignmentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """获取分配历史"""
        # 暂时返回空列表，避免 404 错误
        return success_response(data=[])

    def create(self, request):
        """创建分配"""
        try:
            elderly_id = request.data.get('elderlyId')
            bed_id = request.data.get('bedId')
            assign_date = request.data.get('assignDate')
            
            if not elderly_id or not bed_id:
                return error_response(code=400, message="缺少必要参数")

            room_pk, bed_index = bed_id.split('-')

            try:
                patient = Patient.objects.get(pk=elderly_id)
            except Patient.DoesNotExist:
                return error_response(code=404, message="Elderly not found")

            dt = None
            if isinstance(assign_date, str) and assign_date:
                dt = parse_datetime(assign_date)
            if dt is None:
                dt = timezone.now()

            if settings.USE_TZ:
                if timezone.is_naive(dt):
                    dt = timezone.make_aware(dt, timezone.get_current_timezone())
            else:
                if timezone.is_aware(dt):
                    dt = timezone.make_naive(dt, timezone.get_current_timezone())

            with transaction.atomic():
                room = Room.objects.select_for_update().get(pk=room_pk)
                elderly_name = patient.name
                field_name = f'bed{bed_index}'
                setattr(room, field_name, elderly_name)
                room.save()

                # 更新老人床位信息
                patient.room = room.room_number
                patient.bed_id = str(bed_index)
                patient.save()

                assignment = BedAssignment.objects.create(
                    elderly=patient,
                    room=room,
                    bed_number=str(bed_index),
                    assigned_by=request.user,
                    assign_date=dt,
                    status='active',
                    cleaning_notified=False
                )

                cleaning_staff = list(
                    StaffUser.objects.select_related('user').filter(
                        models.Q(position__icontains='保洁')
                        | models.Q(position__icontains='清洁')
                        | models.Q(position__icontains='clean')
                        | models.Q(user__position__icontains='保洁')
                        | models.Q(user__position__icontains='清洁')
                        | models.Q(user__position__icontains='clean')
                    )
                )
                created_task_count = 0
                for staff_user in cleaning_staff:
                    task = WorkTask.objects.create(
                        type='bed_scheduling',
                        title=f'保洁：清理房间{room.room_number}床位{bed_index}',
                        description=f'为院民 {patient.name} 分配床位后，请清理房间 {room.room_number} 的床位 {bed_index}。',
                        staff=staff_user,
                        patient=patient,
                        due_date=dt.date(),
                        status='pending',
                        priority='high',
                        created_by=request.user
                    )
                    TaskAssignment.objects.create(task=task, staff=staff_user, assigned_by=request.user)
                    created_task_count += 1

                if created_task_count > 0:
                    assignment.cleaning_notified = True
                    assignment.save(update_fields=['cleaning_notified'])
            
            # 3. 构造返回数据
            assignment_data = {
                'id': str(assignment.pk),
                'elderlyId': str(patient.pk),
                'elderlyName': patient.name,
                'bedId': bed_id,
                'roomNumber': room.room_number,
                'bedNumber': str(bed_index),
                'assignDate': assignment.assign_date.isoformat(),
                'status': assignment.status,
                'cleaningNotified': assignment.cleaning_notified,
                'createdAt': assignment.created_at.isoformat()
            }
            return success_response(data=assignment_data)
        except Exception as e:
            logger.exception("Error assigning bed")
            return error_response(code=500, message=str(e))

    @action(detail=True, methods=['get'])
    def form(self, request, pk=None):
        """生成并下载床位分配单"""
        try:
            assignment = BedAssignment.objects.get(pk=pk)

            try:
                pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
            except Exception:
                pass

            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)
            width, height = A4

            c.setFont('STSong-Light', 16)
            c.drawString(50, height - 60, '床位分配单')

            c.setFont('STSong-Light', 11)
            y = height - 90

            def write_line(label: str, value: str) -> None:
                nonlocal y
                c.drawString(50, y, f'{label}：{value}')
                y -= 18

            def fmt_dt(dt_value) -> str:
                if not dt_value:
                    return ''
                if settings.USE_TZ and timezone.is_aware(dt_value):
                    dt_value = dt_value.astimezone(timezone.get_current_timezone())
                return dt_value.strftime('%Y-%m-%d %H:%M:%S')

            def fmt_date(dt_value) -> str:
                if not dt_value:
                    return ''
                if settings.USE_TZ and timezone.is_aware(dt_value):
                    dt_value = dt_value.astimezone(timezone.get_current_timezone())
                return dt_value.strftime('%Y-%m-%d')

            assigned_by_name = ''
            if assignment.assigned_by:
                assigned_by_name = getattr(assignment.assigned_by, 'real_name', '') or getattr(assignment.assigned_by, 'username', '') or ''

            gender_display = ''
            gender_fn = getattr(assignment.elderly, 'get_gender_display', None)
            if callable(gender_fn):
                try:
                    gender_display = gender_fn()
                except Exception:
                    gender_display = ''
            if not gender_display:
                gender_display = getattr(assignment.elderly, 'gender', '') or ''

            write_line('分配单号', str(assignment.pk))
            write_line('生成时间', fmt_dt(assignment.created_at))
            y -= 6

            c.setFont('STSong-Light', 12)
            c.drawString(50, y, '老人信息')
            y -= 18
            c.setFont('STSong-Light', 11)
            write_line('老人ID', str(assignment.elderly.pk))
            write_line('姓名', getattr(assignment.elderly, 'name', '') or '')
            write_line('性别', str(gender_display))
            write_line('年龄', str(getattr(assignment.elderly, 'age', '') or ''))
            y -= 6

            c.setFont('STSong-Light', 12)
            c.drawString(50, y, '床位信息')
            y -= 18
            c.setFont('STSong-Light', 11)
            write_line('房间号', getattr(assignment.room, 'room_number', '') or '')
            write_line('床位号', str(assignment.bed_number))
            write_line('分配日期', fmt_date(assignment.assign_date))
            y -= 6

            c.setFont('STSong-Light', 12)
            c.drawString(50, y, '操作信息')
            y -= 18
            c.setFont('STSong-Light', 11)
            write_line('操作人', assigned_by_name or 'System')
            write_line('清洁已通知', '是' if assignment.cleaning_notified else '否')

            c.showPage()
            c.save()

            pdf_bytes = buffer.getvalue()
            buffer.close()

            response = HttpResponse(pdf_bytes, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="assignment_{assignment.pk}.pdf"'
            return response
        except BedAssignment.DoesNotExist:
            return error_response(code=404, message="Assignment not found")
        except Exception as e:
            return error_response(code=500, message=str(e))
