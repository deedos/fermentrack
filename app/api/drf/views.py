from django.contrib.auth.models import User
from rest_framework import viewsets, pagination, filters
#from rest_framework_filter import rest_framework_filters as filters
from rest_framework.decorators import api_view, action, detail_route
from rest_framework.permissions import IsAuthenticated, AllowAny
from app.api.drf.serializers import CreateUserSerializer, UserSerializer, BeerSerializer, BrewPiDeviceSerializer, FermentationProfileSerializer, FermentationProfilePointSerializer, BeerLogPointSerializer
from app.models import Beer, BrewPiDevice, FermentationProfile, FermentationProfilePoint, BeerLogPoint
from rest_framework import generics
from dateutil.parser import parse
import json

class CreateUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be created
    """
    permission_classes = [AllowAny,]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = CreateUserSerializer
    http_method_names = ['post']

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [IsAuthenticated,]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BeerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [IsAuthenticated,]
    queryset = Beer.objects.all()
    serializer_class = BeerSerializer
    http_method_names = ['get','update', 'post']
    

class BrewPiDeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows brewpidevices to be viewd and created.
    """
    permission_classes = [IsAuthenticated,]
    queryset = BrewPiDevice.objects.all()
    serializer_class = BrewPiDeviceSerializer
    http_method_names = ['get','update', 'put', 'post']
 
class FermentationProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [IsAuthenticated,]
    queryset = FermentationProfile.objects.all()
    serializer_class = FermentationProfileSerializer

class FermentationProfilePointViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [IsAuthenticated,]
    queryset = FermentationProfilePoint.objects.all()
    serializer_class = FermentationProfilePointSerializer

#class OrderFilter(filters.FilterSet):
#    log_time = filters.RangeFilter(name='log_time')

class BeerLogPagination(pagination.LimitOffsetPagination):
    # Class to define custom limits to queries (applied here only to BeerLogPoint endpoint)
    default_limit = 50

class BeerLogPointViewSet(viewsets.ModelViewSet):
    """
    API endpoint for devices/beers logpoints 
    """
    permission_classes = [IsAuthenticated,]
    #queryset = BeerLogPoint.objects.all()
    serializer_class = BeerLogPointSerializer
    #pagination_class = BeerLogPagination 
    
    # allow the query to specify a start and end time 
    def get_queryset(self):
        filter = {}
        start = self.request.query_params.get('start', None)
        end   = self.request.query_params.get('end', None)
        beer =  self.request.query_params.get('beer', None)
        all_queryset = BeerLogPoint.objects.all()
        if start is not None:
            filter['log_time__gte'] = parse(start)
        if end is not None:
            filter['log_time__lte'] = parse(end)
        if beer is not None:
            filter['associated_beer'] = beer
        queryset = all_queryset.filter(**filter)
        return queryset


