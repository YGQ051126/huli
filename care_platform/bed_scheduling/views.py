# -*- coding: utf-8 -*-
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Any
import logging
from django.db import connection
from django.db.utils import OperationalError
from utils.permissions import IsStaffUser, IsAdminUser
from utils.response import success_response, error_response
from rooms.models import Room

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
                # 释放床位：清空对应的 bedX 字段
                field_name = f'bed{bed_index}'
                if hasattr(room, field_name):
                    setattr(room, field_name, '')
                    room.save()
                    
                    self._log_api_response(request, action_name="set_status", status_code=200, data_preview="Bed released")
                    return success_response(message="床位已释放")
                else:
                    return error_response(code=400, message=f"无效的床位索引: {bed_index}")
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
        # TODO: 实现分配逻辑
        return success_response(message="暂未实现")

