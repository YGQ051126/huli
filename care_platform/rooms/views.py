from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from utils.response import success_response, error_response
from .models import Room
from .serializers import RoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all() # type: ignore
    serializer_class = RoomSerializer
    pagination_class = None
    permission_classes = [AllowAny]
    
    def list(self, request, *args, **kwargs):
        print("DEBUG: RoomViewSet.list method called!")
        print(f"Request user: {request.user}")
        
        rooms = Room.objects.all() # type: ignore
        print(f"Total rooms in database: {rooms.count()}")
        
        room_data = []
        for room in rooms:
            room_data.append({
                'id': room.id,
                'room_number': room.room_number,
                'bed1': room.bed1,
                'bed2': room.bed2,
                'bed3': room.bed3,
                'bed4': room.bed4,
            })
        
        print(f"Built room data count: {len(room_data)}")
        if room_data:
            print(f"First room data: {room_data[0]}")
        
        return Response(room_data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def available_beds(self, request, pk=None):
        try:
            room = self.get_object()
            available_beds = room.get_available_beds()
            return success_response({
                'room_number': room.room_number,
                'available_beds': available_beds,
                'bed_count': len(available_beds)
            })
        except Room.DoesNotExist: # type: ignore
            return error_response(code=404, message='Room not found')