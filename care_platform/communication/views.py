from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import Message
from .serializers import MessageSerializer, MessageCreateSerializer
from django.db.models import Q

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # 获取发送给当前用户或由当前用户发送的消息
        queryset = Message.objects.filter( # type: ignore
            Q(sender=user) | Q(receiver=user)
        ).order_by('created_at')

        # 如果指定了对方用户ID，则只返回与该用户的聊天记录
        target_user_id = self.request.query_params.get('receiver') # type: ignore
        if target_user_id:
            queryset = queryset.filter(
                Q(sender_id=target_user_id) | Q(receiver_id=target_user_id)
            )
            
        return queryset
        
    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer
        
    @action(detail=True, methods=['post'])
    def read(self, request, pk=None):
        message = self.get_object()
        if message.receiver != request.user:
            return Response({'detail': '鏃犳潈鎿嶄綔'}, status=status.HTTP_403_FORBIDDEN)
            
        if not message.is_read:
            message.is_read = True
            message.read_at = timezone.now()
            message.save()
            
        return Response({'status': 'marked as read'})