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
from services.models import ServiceOrder
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
        
        # RegisterApplication
        register_approvals = RegisterApplication.objects.filter(status='pending')
        register_data = RegisterApplicationSerializer(register_approvals, many=True).data
        
        # Visit Appointment
        visit_approvals = Appointment.objects.filter(status='pending', type='visit')
        print(f"Visit approvals count: {visit_approvals.count()}")
        visit_data = AppointmentSerializer(visit_approvals, many=True).data
        
        # Family User (Legacy)
        family_approvals = FamilyUser.objects.filter(status='pending')
        print(f"Family approvals count: {family_approvals.count()}")
        family_data = FamilyUserSerializer(family_approvals, many=True).data
        
        # Leave Request
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
            # Activate user
            family_user.user.status = 'active'
            family_user.user.save()
            family_user.save()
            
            # Send notification
            Notification.objects.create(
                user=family_user.user,
                type='system',
                title='Account Registration Approved',
                content=f'Dear {family_user.user.real_name}, your family account registration has been approved. You can now use the system.',
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
                title='Account Registration Rejected',
                content=f'Dear {family_user.user.real_name}, your family account registration was rejected. Reason: {reason or "None"}. Please contact admin.',
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
    """Report ViewSet"""
    permission_classes = [IsAdminUser]
    
    @action(detail=False, methods=['get'])
    def data(self, request):
        report_type = request.query_params.get('type')
        month_str = request.query_params.get('month') # YYYY-MM
        
        data = []
        
        if report_type == 'monthly-care':
            # 1. DailyCareTask
            tasks = DailyCareTask.objects.filter(is_completed=True)
            if month_str:
                try:
                    y, m = map(int, month_str.split('-'))
                    tasks = tasks.filter(task_date__year=y, task_date__month=m)
                except ValueError:
                    pass
            
            # Group by patient
            task_stats = tasks.values('patient__name').annotate(
                totalTasks=Count('id')
            )
            
            # 2. CareRecord
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
            
            # 3. Merge
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
                    'notes': f"Tasks:{counts['tasks']}, Records:{counts['records']}"
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
                items_name = ", ".join([i.service_name for i in o.items.all()])
                data.append({
                    'item': items_name if items_name else 'Service Fee',
                    'amount': float(o.total_amount),
                    'type': 'Income',
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
            else:
                self._fill_summary_sheet(ws)
            
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        filename = f"report_{report_type}_{datetime.now().strftime('%Y%m%d')}.xlsx"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        wb.save(response)
        return response
        
    def _fill_summary_sheet(self, ws):
        ws.append(['Statistical Report', datetime.now().strftime('%Y-%m-%d')])
        ws.append([])
        ws.append(['Item', 'Value', 'Note'])
        ws.append(['Active Elderly', Patient.objects.filter(status='active').count()])
        ws.append(['Total Staff', StaffUser.objects.count()])
        ws.append(['Pending Leaves', LeaveRequest.objects.filter(status='pending').count()])
        
    def _fill_financial_sheet(self, ws, month_str=None):
        ws.append(['Financial Report', datetime.now().strftime('%Y-%m-%d')])
        ws.append(['Date', 'Type', 'Item Name', 'Amount (CNY)'])
        
        orders = ServiceOrder.objects.filter(status__in=['completed', 'rated'])
        if month_str:
            try:
                y, m = map(int, month_str.split('-'))
                orders = orders.filter(paid_at__year=y, paid_at__month=m)
            except ValueError:
                pass
        
        for o in orders:
            date_str = o.paid_at.strftime('%Y-%m-%d') if o.paid_at else o.updated_at.strftime('%Y-%m-%d')
            items_name = ", ".join([i.service_name for i in o.items.all()])
            ws.append([
                date_str,
                'Income',
                items_name if items_name else 'Service Fee',
                float(o.total_amount)
            ])
            
    def _fill_care_sheet(self, ws, month_str=None):
        ws.append(['Monthly Care Report', datetime.now().strftime('%Y-%m-%d')])
        ws.append(['Elderly Name', 'Total Records', 'Detailed Records', 'Tasks', 'Note'])
        
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
                f"Tasks:{counts['tasks']}, Records:{counts['records']}"
            ])
