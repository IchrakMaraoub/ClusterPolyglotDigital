from django.urls import path
from . import views
from .views_api import CustomUserList,ImageControlList,SerialCodeBoxList, SerialCodeProductList,  CustomUserUpdate, ControlList, DefectList, ProductList, ReperationList, ProductTypeList, ControlGetViewSet, BlockList


app_name = 'qualifeed'
urlpatterns = [
    path('category/', views.category, name='category'),
    path('brand/', views.brand, name='brand'),
    path('product/', views.product, name='product'),
    path('caracterstic/', views.caracter, name='caracter'),
    path('defectType/', views.defectType, name='defectType'),
    path('defect/', views.defect, name='defect'),
    path('checkControl/', views.checkControl, name='checkControl'),
    path('box/', views.box, name='box'),
    path('user/', views.user, name='user'),
    path('CustomUserList/', CustomUserList.as_view(), name='CustomUser-list'),
    path('ControlApi/', ControlList.as_view(), name='Control-list'),
    path('DefectApi/', DefectList.as_view(), name='Defect-list'),
    path('ProductApi/', ProductList.as_view(), name='Porduct-list'),
    path('ReperationApi/', ReperationList.as_view(), name='Reperation-list'),
    path('ProductTypeApi/', ProductTypeList.as_view(), name='ProductType-list'),
    path('ControlGetApi/', ControlGetViewSet.as_view(), name='ControlGet'),
    path('CustomUserUpdate/<int:id>',
         CustomUserUpdate.as_view(), name='user-update'),
    path('BlockApi/', BlockList.as_view(), name='Block-list'),
    path('ImageControlList/', ImageControlList.as_view(), name='Image-list'),
    path('SerialCodeBoxList/', SerialCodeBoxList.as_view(), name='serialCodeBox-list'),
    path('SerialCodeProductList/', SerialCodeProductList.as_view(), name='SerialCodeProduct-list'),


    path('logs/', views.logs, name='logs'),
    path('repar_logs/', views.reparation, name='reparation'),
    path('photos/', views.photo, name='photo'),
    path('reference/', views.reference, name='reference'),
    path('webhook/', views.webhook, name='webhook'),

]
