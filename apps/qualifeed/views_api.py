import json
from rest_framework import generics
from apps.users.models import CustomUser
from .serializers import CustomUserSerializer, SerialCodeProductSerializer, ControlGetSerializer, SerialCodeBoxSerializer, CustomUserUpdateSerializer, ImageControlApiSerializer, ControlSerializer, DefectSerializer, ProductSerializer, ReperationSerializer, ProductTypeSerializer, BlockSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.teams.decorators import login_and_team_required
from django.views.decorators.csrf import csrf_exempt
from .models import Product, ProductCategory, Caracterstic, ImageControl, SerialCodeBox, Brand, Control, Defect, DefectType, CheckControl, Box, Reperation, ProductType, Block, SerialCodeProduct
from django_filters import rest_framework as filters
from .filters import ControlFilterSet
from rest_framework.filters import SearchFilter
import django_filters.rest_framework
from rest_framework import viewsets


class CustomUserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend, SearchFilter)
    filterset_fields = ["id", "username", "first_name", "last_name", "email",
                        "poste", "code_user", "is_active", "user__team", "user__role", "products"]


class CustomUserUpdate(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserUpdateSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        # Get the instance of the model to be updated
        instance = self.get_object()

        # Update the is_active field
        instance.is_active = request.data.get('is_active', instance.is_active)

        # Save the updated instance
        instance.save(update_fields=['is_active'])

        # Return a response with the serialized data
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ControlList(generics.ListCreateAPIView):
    queryset = Control.objects.all()
    serializer_class = ControlSerializer
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend, SearchFilter)
    filterset_fields = ["created_at", "updated_at", "date_control", "details_control",
                        "time_control", "state_control", "team", "serial_code", "user", "defect_id"]


class DefectList(generics.ListAPIView):
    queryset = Defect.objects.all()
    serializer_class = DefectSerializer
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend, SearchFilter)
    filterset_fields = ["team", "defect_name", "description",
                        "pattern", "defect_type", "defect_type_value", "products"]

class ArrayFilter(filters.BaseCSVFilter, filters.CharFilter):
    pass

class ProductFilter(filters.FilterSet):
    reference_code_id__reference_code_value = ArrayFilter(field_name="reference_code_id__reference_code_value", lookup_expr='contains')

    class Meta:
        model = Product
        fields = {
           "team", "serial_code", "type_code", "format_of_code",
           "product_name", "status", "brand_id", "category_id", 
           "reference_code_id__reference_code_value", "box_id","users__email"
        }

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, SearchFilter)
    filterset_class = ProductFilter


class ReperationList(generics.ListCreateAPIView):
    queryset = Reperation.objects.all()
    serializer_class = ReperationSerializer
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend, SearchFilter)
    filterset_fields = ["team", "date_reperation", "details_reperation",
                        "time_reperation", "state_reperation", "defect_id", "user", "control_id"]


class ProductTypeList(generics.ListCreateAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend, SearchFilter)
    filterset_fields = ["id", "team", "product_type_name", "product_id"]


class ControlFilter(filters.FilterSet):
    start_date = filters.DateTimeFilter(
        field_name='date_control', lookup_expr='gte')
    end_date = filters.DateTimeFilter(
        field_name='date_control', lookup_expr='lte')

    class Meta:
        model = Control
        fields = {
            "created_at",
            "updated_at",
            "date_control",
            "details_control",
            "time_control",
            "state_control",
            "team__name",
            "serial_code__product_name",
            "user__email",
            "defect_id__defect_name"
        }


class ControlGetViewSet(generics.ListCreateAPIView):
    queryset = Control.objects.all()
    serializer_class = ControlGetSerializer
    filterset_class = ControlFilter
    pagination_class = None


class BlockList(generics.ListCreateAPIView):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend, SearchFilter)
    filterset_fields = ["team", "date_block",
                        "details_block", "defect_id", "user", "control_id"]


class ImageControlList(generics.ListCreateAPIView):
    queryset = ImageControl.objects.all()
    serializer_class = ImageControlApiSerializer
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend, SearchFilter)
    filterset_fields = ["id", "control_id"]


class SerialCodeBoxList(generics.ListCreateAPIView):
    queryset = SerialCodeBox.objects.all()
    serializer_class = SerialCodeBoxSerializer
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend, SearchFilter)
    filterset_fields = ['box_id', 'serial_number_box',
                        'nbr_of_good_product', 'control_id']


class SerialCodeProductList(generics.ListCreateAPIView):
    queryset = SerialCodeProduct.objects.all()
    serializer_class = SerialCodeProductSerializer
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend, SearchFilter)
    filterset_fields = ['product_id',
                        'serial_number_product', 'status', 'control_id']
