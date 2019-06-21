from django.contrib.auth.models import User
from rest_framework import viewsets, pagination, filters
#from rest_framework_filter import rest_framework_filters as filters
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from app.api.drf.serializers import CreateUserSerializer, UserSerializer, BeerSerializer, BrewPiDeviceSerializer, FermentationProfileSerializer, FermentationProfilePointSerializer, BeerLogPointSerializer
from app.models import Beer, BrewPiDevice, FermentationProfile, FermentationProfilePoint, BeerLogPoint
from rest_framework import generics
from dateutil.parser import parse

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
    

    	#if request.method == 'POST':

    #@api_view(['GET', 'POST'])
    #def hello_world(request):
    #	if request.method == 'POST':
    #    	return Response({"message": "Got some data!", "data": request.data})
    #	return Response({"message": "Hello, world!"})


class BrewPiDeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows brewpidevices to be viewd and created.
    """
    permission_classes = [IsAuthenticated,]
    queryset = BrewPiDevice.objects.all()
    serializer_class = BrewPiDeviceSerializer
    http_method_names = ['get','update', 'put', 'post']
 
    #def post(self, request, format=None):
    #    serializer = BrewPiDeviceSerializer(data=request.data)
    #    if serializer.is_valid():
    #        serializer.save()
    #        return Response(serializer.data, status=status.HTTP_201_CREATED)
    #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #def update(self, request, *args, **kwargs):
    #    instance = self.get_object()
    #    instance.active_beer = request.data.get("active_beer")
    #    instance.save()

     #   serializer = self.get_serializer(instance)
      #  serializer.is_valid(raise_exception=True)
       # self.perform_update(serializer)

        #return Response(serializer.data)


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
    pagination_class = BeerLogPagination
    

    
    def get_queryset(self):
        #name = self.kwargs.get('ak', None)
        filter = {}
        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', None)
        #queryset = BeerLogPoint.objects.all()
        #if log_time is not None:
        #queryset = BeerLogPoint.objects.filter(log_time__range(start, end))
        queryset = BeerLogPoint.objects.all()
        if start is not None:
            filter['log_time__gte'] = parse(start)

        if end is not None:
            filter['log_time__lte'] = parse(end)

        queryset = queryset.filter(**filter)

        return queryset 
        #return queryset


