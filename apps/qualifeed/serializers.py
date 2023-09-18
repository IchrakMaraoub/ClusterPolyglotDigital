from rest_framework import serializers
from apps.users.models import CustomUser
from apps.teams.models import Team
from .filters import ControlFilterSet

from .models import Product, ProductCategory, ReferenceProduct,HaveDefect, DefectImage, SerialCodeProduct, ImageControl, SerialCodeBox, Caracterstic, Brand, Control, Defect, DefectType, CheckControl, Box, Reperation, ProductType, Block
from rest_framework.fields import ImageField
from PIL import Image
import base64
import io
from django.core.files.base import ContentFile
from apps.teams.models import Team, Membership

from django_filters import rest_framework as filters

class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            # 12 characters are more than enough.
            file_name = str(uuid.uuid4())[:12]
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["name"]


class MembershipSerializer(serializers.ModelSerializer):
    team = TeamSerializer()

    class Meta:
        model = Membership
        fields = ["role", "team"]


class CustomUserSerializer(serializers.ModelSerializer):
    user = MembershipSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "email",
                  "poste", "code_user", "is_active", "user", "products"]


class CustomUserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name",
                  "email", "poste", "code_user", "is_active"]


class DefectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefectImage
        fields = "__all__"


class DefectSerializer(serializers.ModelSerializer):
    products = serializers.StringRelatedField(many=True)
    defect_type = serializers.StringRelatedField(read_only=True)
    team = serializers.StringRelatedField(read_only=True)
    images = DefectImageSerializer(many=True)

    class Meta:
        model = Defect
        fields = ["id", "team", "defect_name", "description", "pattern",
                  "defect_type", "defect_type_value", "photo", "products", "images"]

class ReferenceProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReferenceProduct
        fields = '__all__'
        
class ProductSerializer(serializers.ModelSerializer):
    users = CustomUserSerializer(many=True)
    defects = DefectSerializer(many=True)
    brand_id = serializers.StringRelatedField(read_only=True)
    category_id = serializers.StringRelatedField(read_only=True)
    reference_code_id = ReferenceProductSerializer()
    team = serializers.StringRelatedField(read_only=True)
    photo_product = Base64ImageField(
        max_length=None, use_url=True,
    )
    photo_code = Base64ImageField(
        max_length=None, use_url=True,
    )
    #caracterstic_value = filters.CharFilter(
    #    method='filter_by_caracterstic_value'
    #)
#
    #def filter_by_caracterstic_value(self, queryset, name, value):
    #    # Filter the products by the caracterstic_value
    #    queryset = queryset.filter(caracterstics__caracterstic_value__contains=[value])
    #    return queryset
    class Meta:
        model = Product
        fields = ["id", "team", "serial_code", "type_code", "format_of_code", "product_name", "status",
                  "brand_id", "category_id", "reference_code_id", "box_id", "photo_code", "photo_product", "defects", "users"]


class ReperationSerializer(serializers.ModelSerializer):
    # defect_id = serializers.StringRelatedField(read_only=True)
    defect_name = serializers.CharField(write_only=True)
    team_name = serializers.CharField(write_only=True)
    photo_reperation = Base64ImageField(
        max_length=None, use_url=True,
    )

    class Meta:
        model = Reperation
        fields = ["id", "team_name", "date_reperation", "details_reperation", "time_reperation",
                  "state_reperation", "defect_name", "photo_reperation", "user", "control_id"]

    def create(self, validated_data):
        defect_name = validated_data.pop('defect_name')
        defect_id = Defect.objects.get(defect_name=defect_name)

        team_name = validated_data.pop('team_name')
        team = Team.objects.get(name=team_name)

        validated_data['defect_id'] = defect_id
        validated_data['team'] = team
        return super().create(validated_data)


class ImageControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageControl
        fields = ('id', 'control_id', 'photo_control')


class HaveDefectSerializer(serializers.ModelSerializer):
    class Meta:
        model = HaveDefect
        fields = ('defect_id', 'number_defect')


class ControlSerializer(serializers.ModelSerializer):

    user_email = serializers.EmailField(write_only=True)
    team_name = serializers.CharField(write_only=True)
    product_name = serializers.CharField(write_only=True)
    have_defect = HaveDefectSerializer(many=True, required=False)
    images = ImageControlSerializer(many=True, required=False)
    defect_id = serializers.PrimaryKeyRelatedField(
        queryset=Defect.objects.all(),
        many=True,
        required=False
    )
    # defect_id = DefectSerializer(many=True)

    class Meta:
        model = Control
        fields = ["id", "created_at", "updated_at", "date_control", "details_control", "time_control",
                  "state_control", "team_name", "product_name", "user_email", "defect_id", "images", "have_defect"]
        filter_overrides = {
            ImageField: {
                'filter_class': ControlFilterSet,
            },
        }

    def create(self, validated_data):

        # user = CustomUser.objects.get(email=validated_data['user'] )
        # validated_data['user'] = user
        #import ipdb;
        #ipdb.set_trace()
        email = validated_data.pop('user_email')
        product_name = validated_data.pop('product_name')
        team_name = validated_data.pop('team_name')

        team = Team.objects.get(name=team_name)
        serial_code = Product.objects.get(product_name=product_name)
        user = CustomUser.objects.get(email=email)

        validated_data['team'] = team
        validated_data['serial_code'] = serial_code
        validated_data['user'] = user

        defects_data = validated_data.pop('defect_id', [])

        have_defect_data = validated_data.pop('have_defect', [])

        control = Control.objects.create(**validated_data)
        control.defect_id.set(defects_data)

        for hd_data in have_defect_data:
            hd_data['serial_code'] = serial_code
            hd_data['control_id'] = control
            HaveDefect.objects.create(team=team, **hd_data)
        return control


class ProductTypeSerializer(serializers.ModelSerializer):
    product_id = serializers.StringRelatedField(many=True)
    team = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProductType
        fields = ["id", "team", "product_type_name", "product_id"]


class SerialCodeBoxGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SerialCodeBox
        fields = ("nbr_of_good_product",)

class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ('qte',)
    def to_representation(self, instance):
        return instance.qte
        
class ImageControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageControl
        fields = ('photo_control',)
        
        
class ControlGetSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    team = serializers.StringRelatedField(read_only=True)
    defect_id = serializers.StringRelatedField(many=True)
    serial_code = serializers.StringRelatedField(read_only=True)
    date_control = serializers.DateField()
    #serial_code_box = SerialCodeBoxGetSerializer(many=True, source='serial_code_boxes')
    nbr_of_good_product = serializers.SerializerMethodField()
    qte_product_box = BoxSerializer(source='serial_code.box_id', read_only=True)
    total_number_defects = serializers.SerializerMethodField()
    images = ImageControlSerializer(many=True, read_only=True)

    def get_total_number_defects(self, obj):
        total = 0
        for defect_name in obj.defect_id.all():
            defect = HaveDefect.objects.filter(
                serial_code__product_name=obj.serial_code.product_name,
                defect_id__defect_name=defect_name,
                control_id=obj.id
            )
            if defect.exists():
                total += defect.values('number_defect')[0]['number_defect']
        return total
    def get_nbr_of_good_product(self, obj):
        try:
            serial_code_box = obj.serial_code_boxes.first()
            return serial_code_box.nbr_of_good_product if serial_code_box else None
        except SerialCodeBox.DoesNotExist:
            return None
        
    class Meta:
        model = Control
        fields = (
            "id",
            "team",
            "date_control",
            "details_control",
            "time_control",
            "state_control",
            "photo_control",
            "serial_code",
            "user",
            "defect_id",
            "qte_product_box",
            "nbr_of_good_product",
            "total_number_defects",
            "images",
        )

class BlockSerializer(serializers.ModelSerializer):
    defect_name = serializers.CharField(write_only=True)
    team_name = serializers.CharField(write_only=True)
    photo_block = Base64ImageField(
        max_length=None, use_url=True,
    )

    class Meta:
        model = Block
        fields = ["id", "team_name", "date_block", "details_block",
                  "defect_name", "photo_block", "user", "control_id"]

    def create(self, validated_data):
        defect_name = validated_data.pop('defect_name')
        defect_id = Defect.objects.get(defect_name=defect_name)

        team_name = validated_data.pop('team_name')
        team = Team.objects.get(name=team_name)

        validated_data['defect_id'] = defect_id
        validated_data['team'] = team
        return super().create(validated_data)


class ImageControlApiSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(write_only=True)

    class Meta:
        model = ImageControl
        fields = ('id', 'team_name', 'control_id', 'photo_control')

    def create(self, validated_data):

        team_name = validated_data.pop('team_name')
        team = Team.objects.get(name=team_name)

        validated_data['team'] = team
        return super().create(validated_data)


class SerialCodeBoxSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(write_only=True)

    class Meta:
        model = SerialCodeBox
        fields = ('box_id', 'team_name', 'serial_number_box',
                  'nbr_of_good_product', 'control_id')

    def create(self, validated_data):

        team_name = validated_data.pop('team_name')
        team = Team.objects.get(name=team_name)

        validated_data['team'] = team
        return super().create(validated_data)


class SerialCodeProductSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(write_only=True)

    class Meta:
        model = SerialCodeProduct
        fields = ('product_id', 'team_name', 'serial_number_product',
                  'status', 'control_id')

    def create(self, validated_data):

        team_name = validated_data.pop('team_name')
        team = Team.objects.get(name=team_name)

        validated_data['team'] = team
        return super().create(validated_data)
