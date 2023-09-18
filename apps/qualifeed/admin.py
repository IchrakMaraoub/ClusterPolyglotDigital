from .models import Product,DefectImage,ReferenceProduct, Defect,HaveDefect, Brand, ImageControl, SerialCodeBox, Caracterstic, ProductCategory, Control, Reperation, Invoice, DefectType, SerialCodeProduct, ProductType, Block

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


@admin.register(Product)
class ProductUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Defect)
class DefectUserAdmin(admin.ModelAdmin):
    pass


@admin.register(DefectType)
class DefecTypetUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Brand)
class BrandUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Caracterstic)
class VariationUserAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductCategory)
class ProductCategoryUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Control)
class ControlUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Reperation)
class ReperationUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Invoice)
class InvoiceUserAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductType)
class ProductTypeUserAdmin(admin.ModelAdmin):
    pass


@admin.register(SerialCodeProduct)
class SerialCodeProductUserAdmin(admin.ModelAdmin):
    pass


@admin.register(ImageControl)
class ImageControlUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Block)
class BlockUserAdmin(admin.ModelAdmin):
    pass


@admin.register(SerialCodeBox)
class SerialCodeBoxAdmin(admin.ModelAdmin):
    pass

@admin.register(DefectImage)
class DefectImageUserAdmin(admin.ModelAdmin):
   pass

@admin.register(HaveDefect)
class HaveDefectUserAdmin(admin.ModelAdmin):
   pass

@admin.register(ReferenceProduct)
class ReferenceProductUserAdmin(admin.ModelAdmin):
   pass