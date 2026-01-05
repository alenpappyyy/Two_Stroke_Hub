from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Bike
from .serializers import BikeSerializer




class BikeListAPI(APIView):
    def get(self, request):
        bikes = Bike.objects.all()
        serializer = BikeSerializer(bikes, many=True)
        return Response(serializer.data)