from apps.teams.models import BaseTeamModel
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.conf import settings


TYPE_PRODUCT_CODE_CHOICES = [
    ('QrCode', 'QRCODE'),
    ('ZebraCode', 'ZebraCode'),
    ('BarCode', 'BarCode'),
]

TYPE_DEFECT_CHOICES = [
    ('Minor', 'MINOR'),
    ('Major', 'MAJOR'),
    ('Critical', 'CRITICAL'),

]


class ProductCategory(BaseTeamModel):
    category_name = models.CharField(max_length=255, blank=False, unique=True)
    parent = models.ForeignKey("self", blank=True, null=True,
                               related_name="subcategories", on_delete=models.PROTECT)

    def __str__(self):
        return self.category_name


class Brand(BaseTeamModel):
    brand_name = models.CharField(max_length=100, blank=False, unique=True)

    def __str__(self):
        return self.brand_name


class Caracterstic(BaseTeamModel):
    caracterstic_label = models.CharField(max_length=255)
    caracterstic_value = ArrayField(models.CharField(
        max_length=200, blank=True), default=list, size=50, null=True, blank=True)

    def __str__(self):
        return self.caracterstic_label


class Box(BaseTeamModel):
    box_name = models.CharField(max_length=255, blank=False)
    qte = models.IntegerField(blank=False)
    parent = models.ForeignKey(
        "self", blank=True, null=True, related_name="boxes", on_delete=models.PROTECT)

    def __str__(self):
        return self.box_name


class ReferenceProduct(BaseTeamModel):
    reference_code_label = models.CharField(max_length=255)
    reference_code_value = ArrayField(models.CharField(
        max_length=200, blank=True), default=list, size=50, null=True, blank=True)

    def __str__(self):
        return self.reference_code_label


class Product(BaseTeamModel):
    serial_code = models.CharField(
        max_length=255, unique=True)
    type_code = models.CharField(
        max_length=255,  choices=TYPE_PRODUCT_CODE_CHOICES)
    format_of_code = models.CharField(max_length=255, null=True, blank=True)
    photo_code = models.ImageField()
    product_name = models.CharField(max_length=500)
    photo_product = models.ImageField()
    status = models.CharField(max_length=100)
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    caracterstics = models.ManyToManyField(Caracterstic)
    box_id = models.ForeignKey(Box, on_delete=models.CASCADE)
    reference_code_id = models.ForeignKey(
        ReferenceProduct, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.product_name


class ProductType(BaseTeamModel):
    product_type_name = models.CharField(max_length=255)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)


class have_Tags(BaseTeamModel):
    serial_code = models.ForeignKey(Product, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Caracterstic, on_delete=models.CASCADE)
    value_tag = models.CharField(max_length=255)

    def __str__(self):
        return self.value_tag


class DefectType(BaseTeamModel):
    defect_type_name = models.CharField(max_length=100,  blank=False)
    defect_type = ArrayField(models.CharField(
        max_length=200, blank=True), default=list, size=50, null=True, blank=False)

    def __str__(self):
        return self.defect_type_name


class Defect(BaseTeamModel):
    defect_name = models.CharField(max_length=100,  blank=False, unique=True)
    description = models.TextField(blank=True)
    pattern = models.CharField(max_length=100, blank=True, null=True)
    defect_type = models.ForeignKey(DefectType, on_delete=models.CASCADE)
    defect_type_value = models.CharField(max_length=100, blank=False)
    photo = models.ImageField(blank=True)
    products = models.ManyToManyField(Product, related_name="defects")

    def __str__(self):
        return self.defect_name


class DefectImage(models.Model):
    defect = models.ForeignKey(
        Defect, on_delete=models.CASCADE, related_name='images')
    photo = models.ImageField(blank=True)

    def __str__(self):
        return f"Image for {self.defect.defect_name}"


class Control (BaseTeamModel):
    date_control = models.DateField(blank=False)
    details_control = models.CharField(max_length=100, blank=False)
    time_control = models.TimeField(blank=False)
    state_control = models.CharField(max_length=100, blank=True)
    photo_control = models.ImageField(blank=True, null=True)
    serial_code = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    defect_id = models.ManyToManyField(
        Defect, related_name="controls", blank=True)

    def __str__(self):
        return self.details_control
    
class HaveDefect(BaseTeamModel):
    serial_code = models.ForeignKey(Product, on_delete=models.CASCADE)
    defect_id = models.ForeignKey(Defect, on_delete=models.CASCADE)
    number_defect = models.IntegerField(blank=True)
    control_id = models.ForeignKey(Control, on_delete=models.CASCADE)


class ImageControl(BaseTeamModel):
    control_id = models.ForeignKey(
        Control, on_delete=models.CASCADE, related_name="images")
    photo_control = models.ImageField()


class SerialCodeBox(BaseTeamModel):
    box_id = models.ForeignKey(Box, on_delete=models.CASCADE)
    serial_number_box = models.CharField(max_length=255, blank=True, null=True)
    nbr_of_good_product = models.IntegerField(blank=True)
    control_id = models.ForeignKey(Control, on_delete=models.CASCADE, related_name='serial_code_boxes')



class SerialCodeProduct(BaseTeamModel):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    serial_number_product = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    control_id = models.ForeignKey(Control, on_delete=models.CASCADE)

    def __str__(self):
        return self.serial_number_product


class Reperation (BaseTeamModel):
    date_reperation = models.DateField(blank=False)
    details_reperation = models.CharField(max_length=100, blank=False)
    time_reperation = models.TimeField(blank=False)
    state_reperation = models.CharField(max_length=100, blank=False)
    photo_reperation = models.ImageField()
    defect_id = models.ForeignKey(
        Defect, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    control_id = models.ForeignKey(
        Control, on_delete=models.CASCADE, blank=True, null=True)


class Invoice (BaseTeamModel):
    amount_invoice = models.CharField(max_length=100, blank=False)
    date_invoice = models.DateField(blank=False)
    id_reperation = models.ForeignKey(Reperation, on_delete=models.CASCADE)
    id_control = models.ForeignKey(Control, on_delete=models.CASCADE)


class CheckControl (BaseTeamModel):
    box_id = models.ForeignKey(Box, on_delete=models.CASCADE)
    defect_id = models.ForeignKey(Defect, on_delete=models.CASCADE)
    threshold = models.IntegerField(blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    post = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.threshold


class Image (BaseTeamModel):
    image = models.ImageField(null=False, blank=False)
    serial_code = models.ForeignKey(Product, on_delete=models.CASCADE)
    defect_id = models.ForeignKey(Defect, on_delete=models.CASCADE)

    def __str__(self):
        return self.image


class Block (BaseTeamModel):
    date_block = models.DateField(blank=False)
    details_block = models.CharField(max_length=100, blank=False)
    photo_block = models.ImageField()
    defect_id = models.ForeignKey(
        Defect, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    control_id = models.ForeignKey(
        Control, on_delete=models.CASCADE, blank=True, null=True)
