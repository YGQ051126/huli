# -*- coding: utf-8 -*-
# type: ignore
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsAdminUser
from utils.response import success_response, error_response
from patients.models import Patient
from users.models import StaffUser, FamilyUser, LeaveRequest, RegisterApplication
from users.serializers import FamilyUserSerializer, LeaveRequestSerializer, RegisterApplicationSerializer
from appointments.models import Appointment
from appointments.serializers import AppointmentSerializer
from payments.models import Bill, Payment
from rooms.models import Room
from care_records.models import CareRecord
from notifications.models import Notification
from django.db.models import Sum
from datetime import datetime
from django.utils import timezone
import openpyxl
from django.http import HttpResponse

class MonthlyReportView(APIView):
    """
    Generate monthly report
    URL: /api/v1/reports/monthly/
    """
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        year = int(request.query_params.get('year', datetime.now().year))
        month = int(request.query_params.get('month', datetime.now().month))
        
        # 1. Total Elderly (Active)
        total_elderly = Patient.objects.filter(status='active').count()  # type: ignore[attr-defined]
        
        # 2. Total Staff
        total_staff = StaffUser.objects.count()  # type: ignore[attr-defined]
        
        # 3. Total Payments (Mock or Real)
        # Assuming Bill has month field 'YYYY-MM'
        month_str = f"{year}-{month:02d}"
        # Check if Bill model has month field. Assuming yes based on payments/views.py usage.
        total_payments = 0.00
        try:
             total_payments = Bill.objects.filter(month=month_str).aggregate(Sum('total_amount'))['total_amount__sum'] or 0.00  # type: ignore[attr-defined]
        except Exception:
             pass
        
        # 4. Occupancy Rate
        total_rooms = Room.objects.count()  # type: ignore[attr-defined]
        total_capacity = total_rooms * 4 # Assuming 4 beds per room
        if total_capacity > 0:
            occupancy_rate = round(total_elderly / total_capacity, 2)
        else:
            occupancy_rate = 0.00
            
        data = {
            "year": year,
            "month": month,
            "total_elderly": total_elderly,
            "total_staff": total_staff,
            "total_payments": float(total_payments),
            "occupancy_rate": occupancy_rate
        }
        
        return success_response(data, message="Report generated successfully")

class ApprovalViewSet(ViewSet):
    permission_classes = [IsAdminUser]
    
    def list(self, request):
        print(f"ApprovalViewSet.list called by user: {request.user}")
        print(f"User role: {getattr(request.user, 'role', 'unknown')}")
        print(f"Is authenticated: {request.user.is_authenticated}")
        
        # 注册申请审批 (RegisterApplication)
        register_approvals = RegisterApplication.objects.filter(status='pending')
        register_data = RegisterApplicationSerializer(register_approvals, many=True).data
        
        # 探视预约审批
        visit_approvals = Appointment.objects.filter(status='pending', type='visit')
        print(f"Visit approvals count: {visit_approvals.count()}")
        visit_data = AppointmentSerializer(visit_approvals, many=True).data
        
        # 家属注册审批 (Legacy FamilyUser, maybe remove if RegisterApplication replaces it)
        # But for now, keeping it if legacy data exists, or just return empty
        family_approvals = FamilyUser.objects.filter(status='pending')
        print(f"Family approvals count: {family_approvals.count()}")
        family_data = FamilyUserSerializer(family_approvals, many=True).data
        
        # 员工请假审批
        leave_approvals = LeaveRequest.objects.filter(status='pending')
        print(f"Leave approvals count: {leave_approvals.count()}")
        leave_data = LeaveRequestSerializer(leave_approvals, many=True).data
        
        return Response({
            'register_approvals': list(register_data),
            'visit_approvals': list(visit_data),
            'family_approvals': list(family_data),
            'leave_approvals': list(leave_data)
        })
    
    @action(detail=True, methods=['post'], url_path='approve-family')
    def approve_family(self, request, pk=None):
        try:
            family_user = FamilyUser.objects.get(pk=pk)
            family_user.status = 'approved'
            # 同时激活用户账号
            family_user.user.status = 'active'
            family_user.user.save()
            family_user.save()
            
            # Send notification
            Notification.objects.create(
                user=family_user.user,
                type='system',
                title='账号注册审批通过',
                content=f'尊敬的{family_user.user.real_name}，您的亲属账号注册申请已通过审批，现在可以正常使用了。',
                related_id=family_user.user.id,
                related_type='family_user'
            )
            
            return success_response(message='Family user approved')
        except FamilyUser.DoesNotExist:
            return error_response(message='Family user not found', code=404)

    @action(detail=True, methods=['post'], url_path='reject-family')
    def reject_family(self, request, pk=None):
        try:
            family_user = FamilyUser.objects.get(pk=pk)
            family_user.status = 'rejected'
            reason = request.data.get('reason', '')
            if reason:
                family_user.rejection_reason = reason
            family_user.save()
            
            # Send notification
            Notification.objects.create(
                user=family_user.user,
                type='system',
                title='账号注册审批未通过',
                content=f'尊敬的{family_user.user.real_name}，很遗憾，您的亲属账号注册申请未通过审批。原因：{reason or "无"}。如有疑问请联系管理员。',
                related_id=family_user.user.id,
                related_type='family_user'
            )
            
            return success_response(message='Family user rejected')
        except FamilyUser.DoesNotExist:
            return error_response(message='Family user not found', code=404)

    @action(detail=True, methods=['post'], url_path='approve-leave')
    def approve_leave(self, request, pk=None):
        try:
            leave = LeaveRequest.objects.get(pk=pk)
            if leave.status == 'pending':
                leave.status = 'approved'
                leave.approved_by = request.user
                leave.approved_at = timezone.now()
                leave.save()
                return success_response(message='Leave request approved')
            return error_response(message='Invalid status', code=400)
        except LeaveRequest.DoesNotExist:
            return error_response(message='Leave request not found', code=404)

    @action(detail=True, methods=['post'], url_path='reject-leave')
    def reject_leave(self, request, pk=None):
        try:
            leave = LeaveRequest.objects.get(pk=pk)
            if leave.status == 'pending':
                leave.status = 'rejected'
                leave.approved_by = request.user
                leave.approved_at = timezone.now()
                reason = request.data.get('reason', '')
                if reason:
                    leave.rejection_reason = reason
                leave.save()
                return success_response(message='Leave request rejected')
            return error_response(message='Invalid status', code=400)
        except LeaveRequest.DoesNotExist:
            return error_response(message='Leave request not found', code=404)

from django.db.models import Count, Avg
from care_records.models import CareRecord, DailyCareTask

class ReportViewSet(ViewSet):
    """统计报表视图集"""
    permission_classes = [IsAdminUser]
    
    @action(detail=False, methods=['get'])
    def data(self, request):
        report_type = request.query_params.get('type')
        month_str = request.query_params.get('month') # YYYY-MM
        
        data = []
        
        if report_type == 'monthly-care':
            # 1. 优先统计 DailyCareTask (员工端打卡数据)
            tasks = DailyCareTask.objects.filter(is_completed=True)
            if month_str:
                try:
                    y, m = map(int, month_str.split('-'))
                    tasks = tasks.filter(task_date__year=y, task_date__month=m)
                except ValueError:
                    pass
            
            # 按老人分组统计
            task_stats = tasks.values('patient__name').annotate(
                totalTasks=Count('id')
            )
            
            # 2. 同时也统计 CareRecord (详细护理记录)
            records = CareRecord.objects.all()
            if month_str:
                try:
                    y, m = map(int, month_str.split('-'))
                    records = records.filter(record_date__year=y, record_date__month=m)
                except ValueError:
                    pass
            
            record_stats = records.values('patient__name').annotate(
                totalRecords=Count('id')
            )
            
            # 3. 合并数据
            stats_map = {}
            
            for s in task_stats:
                name = s['patient__name']
                stats_map[name] = stats_map.get(name, {'tasks': 0, 'records': 0})
                stats_map[name]['tasks'] = s['totalTasks']
                
            for s in record_stats:
                name = s['patient__name']
                stats_map[name] = stats_map.get(name, {'tasks': 0, 'records': 0})
                stats_map[name]['records'] = s['totalRecords']
                
            for name, counts in stats_map.items():
                total = counts['tasks'] + counts['records']
                data.append({
                    'elderlyName': name,
                    'totalRecords': total,
                    'averageScore': 'N/A', 
                    'notes': f"任务打卡:{counts['tasks']}, 详细记录:{counts['records']}"
                })
                
        elif report_type == 'bed-usage':
            # Room occupancy
            # Assuming 4 beds per room based on Room model fields (bed1..bed4)
            # Or checking Patient room/bed assignment
            rooms = Room.objects.all()
            active_patients = Patient.objects.filter(status='active')
            
            for room in rooms:
                # Find patients in this room
                patients_in_room = active_patients.filter(room=room.room_number)
                
                # We iterate 1-4 beds
                for i in range(1, 5):
                    bed_id = str(i)
                    p = patients_in_room.filter(bed_id=bed_id).first()
                    
                    # Row per bed
                    data.append({
                        'roomNumber': room.room_number,
                        'bedNumber': f"{i}号床",
                        'occupancyRate': "100%" if p else "0%", # Bed level occupancy is binary
                        'status': "已入住" if p else "空闲",
                        'patientName': p.name if p else ''
                    })

        elif report_type == 'finance':
            # Service Order income
            orders = ServiceOrder.objects.filter(status__in=['completed', 'rated'])
            if month_str:
                try:
                    y, m = map(int, month_str.split('-'))
                    # Using paid_at or updated_at
                    orders = orders.filter(paid_at__year=y, paid_at__month=m)
                except ValueError:
                    pass
            
            for o in orders:
                data.append({
                    'item': o.service_item.name if o.service_item else '服务费',
                    'amount': float(o.total_amount),
                    'type': '收入',
                    'date': o.paid_at.strftime('%Y-%m-%d') if o.paid_at else o.updated_at.strftime('%Y-%m-%d')
                })
                
        return success_response(data)

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Dashboard summary stats"""
        total_elderly = Patient.objects.filter(status='active').count()
        total_staff = StaffUser.objects.count()
        total_beds = Room.objects.count() * 4 # Approximate
        occupied_beds = Patient.objects.filter(status='active', bed_id__isnull=False).count()
        
        return Response({
            'total_elderly': total_elderly,
            'total_staff': total_staff,
            'occupancy_rate': round(occupied_beds / total_beds, 2) if total_beds else 0,
            'pending_approvals': LeaveRequest.objects.filter(status='pending').count() + Appointment.objects.filter(status='pending').count()
        })

    @action(detail=False, methods=['get'])
    def export(self, request):
        """Export report to Excel"""
        report_type = request.query_params.get('type', 'summary')
        month_str = request.query_params.get('month') # YYYY-MM
        
        wb = openpyxl.Workbook()
        ws = wb.active
        if ws:
            ws.title = report_type.capitalize()
            
            if report_type == 'finance':
                self._fill_financial_sheet(ws, month_str)
            elif report_type == 'monthly-care':
                self._fill_care_sheet(ws, month_str)
            elif report_type == 'bed-usage':
                self._fill_bed_usage_sheet(ws)
            else:
                self._fill_summary_sheet(ws)
            
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        filename = f"report_{report_type}_{datetime.now().strftime('%Y%m%d')}.xlsx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        wb.save(response)
        return response
        
    def _fill_summary_sheet(self, ws):
        ws.append(['统计报表', datetime.now().strftime('%Y-%m-%d')])
        ws.append([])
        ws.append(['项目', '数值', '备注'])
        ws.append(['在院人数', Patient.objects.filter(status='active').count()])
        ws.append(['员工总数', StaffUser.objects.count()])
        ws.append(['待审批请假', LeaveRequest.objects.filter(status='pending').count()])
        
    def _fill_financial_sheet(self, ws, month_str=None):
        ws.append(['财务收支统计报表', datetime.now().strftime('%Y-%m-%d')])
        ws.append(['日期', '收支类型', '项目名称', '金额 (元)'])
        
        orders = ServiceOrder.objects.filter(status__in=['completed', 'rated'])
        if month_str:
            try:
                y, m = map(int, month_str.split('-'))
                orders = orders.filter(paid_at__year=y, paid_at__month=m)
            except ValueError:
                pass
        
        for o in orders:
            date_str = o.paid_at.strftime('%Y-%m-%d') if o.paid_at else o.updated_at.strftime('%Y-%m-%d')
            ws.append([
                date_str,
                '收入',
                o.service_item.name if o.service_item else '服务费',
                float(o.total_amount)
            ])
            
    def _fill_care_sheet(self, ws, month_str=None):
        ws.append(['月度护理记录报表', datetime.now().strftime('%Y-%m-%d')])
        ws.append(['老人姓名', '护理记录数 (详细+打卡)', '详细记录数', '任务打卡数', '备注'])
        
        # Logic same as data()
        tasks = DailyCareTask.objects.filter(is_completed=True)
        records = CareRecord.objects.all()
        
        if month_str:
            try:
                y, m = map(int, month_str.split('-'))
                tasks = tasks.filter(task_date__year=y, task_date__month=m)
                records = records.filter(record_date__year=y, record_date__month=m)
            except ValueError:
                pass
                
        task_stats = tasks.values('patient__name').annotate(totalTasks=Count('id'))
        record_stats = records.values('patient__name').annotate(totalRecords=Count('id'))
        
        stats_map = {}
        for s in task_stats:
            name = s['patient__name']
            stats_map[name] = stats_map.get(name, {'tasks': 0, 'records': 0})
            stats_map[name]['tasks'] = s['totalTasks']
            
        for s in record_stats:
            name = s['patient__name']
            stats_map[name] = stats_map.get(name, {'tasks': 0, 'records': 0})
            stats_map[name]['records'] = s['totalRecords']
            
        for name, counts in stats_map.items():
            total = counts['tasks'] + counts['records']
            ws.append([
                name,
                total,
                counts['records'],
                counts['tasks'],
                f"任务打卡:{counts['tasks']}, 详细记录:{counts['records']}"
            ])

    def _fill_bed_usage_sheet(self, ws):
        ws.append(['床位使用状况报表', datetime.now().strftime('%Y-%m-%d')])
        ws.append(['房间号', '床位号', '占用状态', '当前状态', '入住老人'])
        
        rooms = Room.objects.all()
        active_patients = Patient.objects.filter(status='active')
        
        for room in rooms:
            patients_in_room = active_patients.filter(room=room.room_number)
            for i in range(1, 5):
                bed_id = str(i)
                p = patients_in_room.filter(bed_id=bed_id).first()
                ws.append([
                    room.room_number,
                    f"{i}号床",
                    "100%" if p else "0%",
                    "已入住" if p else "空闲",
                    p.name if p else ''
                ])
