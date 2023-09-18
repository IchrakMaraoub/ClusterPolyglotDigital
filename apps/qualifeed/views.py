from json import dumps
from django.http import HttpResponse, HttpResponseRedirect
from apps.teams.decorators import login_and_team_required
from django.views.decorators.csrf import csrf_exempt
from django.template.response import TemplateResponse
from .forms import ProductForm, CategorieForm, caractersticForm, referenceForm, BrandForm, ControlForm, DefectForm, DefectTypeForm, CheckControlForm, BoxForm, UserForm
from django.shortcuts import render, redirect
from .models import Product, ProductCategory, HaveDefect, SerialCodeBox, ReferenceProduct, DefectImage, ImageControl, DefectImage, Caracterstic, Brand, Control, Defect, DefectType, CheckControl, Box, TYPE_PRODUCT_CODE_CHOICES, Reperation
from django.http import JsonResponse
from django.conf import settings
from apps.users.models import CustomUser
from apps.teams.models import Team, Membership
from django.core import serializers
from django.db.models.functions import TruncMonth
from datetime import datetime
from django.db.models import DateField
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.template.response import TemplateResponse
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay
from django.core.paginator import Paginator, EmptyPage
from datetime import date, timedelta
from django.db.models import Prefetch
import json
import requests
from datetime import date
from collections import Counter

@login_and_team_required
@csrf_exempt
def brand(request, team_slug):
    if request.method == 'POST':  # If the form has been submitted...

        brand_form = BrandForm(request.POST)

        if brand_form.is_valid:
            # import ipdb;
            # ipdb.set_trace()
            if 'id' in brand_form.data:
                brand_obj = Brand.objects.get(id=brand_form.data['id'])
             # Update the fields of the record
                brand_obj.brand_name = brand_form.data['name']

                brand_obj.save()

            else:

                brand_name = brand_form.data['brand_name']
                brands = request.POST.getlist('brands')

                brand = Brand(team_id=request.team.id, brand_name=brand_name)
                brand.save()
            return redirect(".")
    else:
        # import ipdb;
        # ipdb.set_trace()
        brand_form = BrandForm(data={'team_slug': team_slug})
    if request.is_ajax():
        # import ipdb;
        # ipdb.set_trace()

        brand_id = request.GET['brand_id']

        brand_name = Brand.objects.filter(id=brand_id).values('brand_name')[
            0]['brand_name']

        values = {
            'brand_id': brand_id,
            'brand_name': brand_name,


        }
        return JsonResponse({
            'values': values
        })
    brand_ajax = Brand.objects.all().filter(team__name=team_slug)
    brands = Brand.objects.all().filter(team__name=team_slug)

    context = {
        'brand_ajax': brand_ajax,
        'brands': brands,
        'brand_form': brand_form,
    }
    return TemplateResponse(request, "qualifeed/brand.html", context)


@login_and_team_required
@csrf_exempt
def category(request, team_slug):
    # import ipdb;
    # ipdb.set_trace()

    if request.method == 'POST':  # If the form has been submitted...
       # import ipdb;
        # ipdb.set_trace()
        categorie_form = CategorieForm(request.POST)

        if categorie_form.is_valid:
            # import ipdb;
            # ipdb.set_trace()
            if 'id' in categorie_form.data:
                category_obj = ProductCategory.objects.get(
                    id=categorie_form.data['id'])
            # Update the fields of the record
                category_obj.category_name = categorie_form.data['name']
                if categorie_form.data['parent']:
                    category_parent = ProductCategory.objects.get(
                        category_name=categorie_form.data['parent'])
                    category_obj.parent = category_parent

                category_obj.save()
            else:

                category_name = categorie_form.data['category_name']
                categorys = request.POST.getlist('categorys')

                if categorie_form.data['parent']:
                    parent = categorie_form.data['parent']
                    category_obj = ProductCategory.objects.get(
                        category_name=parent)
                    categorie = ProductCategory(
                        team_id=request.team.id, category_name=category_name, parent=category_obj)
                else:
                    categorie = ProductCategory(
                        team_id=request.team.id, category_name=category_name)
                categorie.save()
            return redirect(".")
        # else:
          #   categorie               = ProductCategory(team_id=request.team.id,category_name=category_name)

        categorie.save()
        return redirect(".")
    else:
        categorie_form = CategorieForm(data={'team_slug': team_slug})

    if request.is_ajax():
        category_id = request.GET['category_id']

        category_name = ProductCategory.objects.filter(
            id=category_id).values('category_name')[0]['category_name']
        parent = ProductCategory.objects.filter(
            id=category_id).values('parent')[0]['parent']

        if parent is None:
            parent = None
        else:
            parent = ProductCategory.objects.filter(id=ProductCategory.objects.filter(
                id=category_id).values('parent')[0]['parent'])[0].id

        values = {
            'category_id': category_id,
            'parent': parent,
            'category_name': category_name,

        }
        return JsonResponse({
            'values': values
        })
    category_ajax = ProductCategory.objects.all().filter(team__name=team_slug)
    categorys = ProductCategory.objects.all().filter(team__name=team_slug)

    context = {
        'category_ajax': category_ajax,
        'categorys': categorys,
        'categorie_form': categorie_form, }
    return TemplateResponse(request, "qualifeed/category.html", context)


@login_and_team_required
@csrf_exempt
def caracter(request, team_slug):
    if request.method == 'POST':  # If the form has been submitted...

        caracterstic_form = caractersticForm(request.POST)

        if caracterstic_form.is_valid:
            # import ipdb;
            # ipdb.set_trace()
            if 'id' in caracterstic_form.data:
                caracterstic_obj = Caracterstic.objects.get(
                    id=caracterstic_form.data['id'])

            # Update the fields of the record
                caracterstic_obj.caracterstic_label = caracterstic_form.data['caracterstic_label']
                caracterstic_obj.caracterstic_value = caracterstic_form.data['Tvalue'].split(
                )

                caracterstic_obj.save()

            else:

                caracterstic_label = caracterstic_form.data['caracterstic_label']
                caracterstic_value = caracterstic_form.data['caracterstic_value']
                caracters = request.POST.getlist('caracters')

                caracterstique = Caracterstic.objects.create(
                    team_id=request.team.id, caracterstic_label=caracterstic_label, caracterstic_value=caracterstic_value.split())
                caracterstique.save()
            return redirect(".")
    else:
       # import ipdb;
       # ipdb.set_trace()
        caracterstic_form = caractersticForm(data={'team_slug': team_slug})
    if request.is_ajax():
        # import ipdb;
        # ipdb.set_trace()

        caracter_id = request.GET['caracter_id']

        caracterstic_label = Caracterstic.objects.filter(id=caracter_id).values(
            'caracterstic_label')[0]['caracterstic_label']
        caracterstic_value = Caracterstic.objects.filter(id=caracter_id).values(
            'caracterstic_value')[0]['caracterstic_value']

        values = {
            'caracter_id': caracter_id,
            'caracterstic_label': caracterstic_label,
            'caracterstic_value': caracterstic_value,

        }
        return JsonResponse({
            'values': values
        })
    caracter_ajax = Caracterstic.objects.all().filter(team__name=team_slug)
    caracters = Caracterstic.objects.all().filter(team__name=team_slug)

    context = {
        'caracter_ajax': caracter_ajax,
        'caracters': caracters,
        'caracterstic_form': caracterstic_form,
    }
    return TemplateResponse(request, "qualifeed/caracterstic.html", context)


@login_and_team_required
@csrf_exempt
def reference(request, team_slug):
    if request.method == 'POST':  # If the form has been submitted...

        reference_form = referenceForm(request.POST)

        if reference_form.is_valid:
            # import ipdb;
            # ipdb.set_trace()
            if 'id' in reference_form.data:
                reference_obj = ReferenceProduct.objects.get(
                    id=reference_form.data['id'])

            # Update the fields of the record
                reference_obj.reference_code_label = reference_form.data['reference_code_label']
                reference_obj.reference_code_value = reference_form.data['reference_code_value'].split(
                )

                reference_obj.save()

            else:

                reference_code_label = reference_form.data['reference_code_label']
                reference_code_value = reference_form.data['reference_code_value']
                references = request.POST.getlist('references')

                reference = ReferenceProduct.objects.create(
                    team_id=request.team.id, reference_code_label=reference_code_label, reference_code_value=reference_code_value.split())
                reference.save()
            return redirect(".")
    else:
       # import ipdb;
       # ipdb.set_trace()
        reference_form = referenceForm(data={'team_slug': team_slug})
    if request.is_ajax():
        # import ipdb;
        # ipdb.set_trace()

        reference_id = request.GET['reference_id']

        reference_code_label = ReferenceProduct.objects.filter(id=reference_id).values(
            'reference_code_label')[0]['reference_code_label']
        reference_code_value = ReferenceProduct.objects.filter(id=reference_id).values(
            'reference_code_value')[0]['reference_code_value']

        values = {
            'reference_id': reference_id,
            'reference_code_label': reference_code_label,
            'reference_code_value': reference_code_value,

        }
        return JsonResponse({
            'values': values
        })
    reference_ajax = ReferenceProduct.objects.all().filter(team__name=team_slug)
    references = ReferenceProduct.objects.all().filter(team__name=team_slug)

    context = {
        'reference_ajax': reference_ajax,
        'references': references,
        'reference_form': reference_form,
    }
    return TemplateResponse(request, "qualifeed/reference.html", context)


@login_and_team_required
@csrf_exempt
def product(request, team_slug):
    # import ipdb;
    # ipdb.set_trace()
    if request.method == 'POST':  # If the form has been submitted...
        # import ipdb;
        # ipdb.set_trace()
        product_form = ProductForm(request.POST, team_slug)
        if product_form.is_valid:
            if 'id' in product_form.data:
                product_obj = Product.objects.get(id=product_form.data['id'])
                # Update the fields of the record
                product_obj.product_name = product_form.data['name']
                product_obj.category_id = ProductCategory.objects.get(
                    category_name=product_form.data['category_name'])
                product_obj.type_code = product_form.data['type']
                product_obj.format_of_code = product_form.data['format']
                product_obj.brand_id = Brand.objects.get(
                    brand_name=product_form.data['brand'])
                product_obj.box_id = Box.objects.get(
                    box_name=product_form.data['box'])
                product_obj.serial_code = product_form.data['serial_code']

                # product_obj.reference_code_id = ReferenceProduct.objects.get(
                # reference_code_label=product_form.data['reference_code'])
                # product_obj.caracterstics    = Caracterstic.objects.get(category_name=product_form.data['tag'])

                # Remove any existing relations not in the new list of defects
                existing_defects = set(
                    product_obj.defects.filter(team__name=team_slug))
                new_defects = set(Defect.objects.filter(
                    id__in=request.POST.getlist('defects')))
                to_remove = existing_defects - new_defects
                product_obj.defects.remove(*to_remove)

                product_obj.save()
                defects = request.POST.getlist('defects')
                defect_products = Defect.objects.filter(
                    products=product_obj, team__name=team_slug)
                for defect_id in defects:
                    if defect_id not in defect_products:
                        defect = Defect.objects.get(id=defect_id)
                        defect.products.add(product_obj)
                product_obj.save()

            else:
                product_name = product_form.data['product_name']
                category_name = product_form.data['category_id']
                type_code = product_form.data['type_code']
                format_of_code = product_form.data['format_of_code']
                product_category = ProductCategory.objects.get(
                    id=category_name)
                brand_name = product_form.data['brand_id']
                product_brand = Brand.objects.get(id=brand_name)
                box_id = product_form.data['box_id']
                product_box = Box.objects.get(id=box_id)
                serial_code = product_form.data['serial_code']
                # if product_form.data['reference_code_id']:
                #    reference_code_id = product_form.data['reference_code_id']
                #    product_reference_code = ReferenceProduct.objects.get(id=reference_code_id)
                #    product = Product.objects.create(team_id=request.team.id, type_code=type_code,format_of_code=format_of_code,
                #                                 product_name=product_name, category_id=product_category, brand_id=product_brand, box_id=product_box,reference_code_id=product_reference_code)

                product = Product.objects.create(team_id=request.team.id, type_code=type_code, serial_code=serial_code, format_of_code=format_of_code,
                                                 product_name=product_name, category_id=product_category, brand_id=product_brand, box_id=product_box)

                defects = request.POST.getlist('defects')
                product.save()
                for defect_id in defects:
                    defect = Defect.objects.get(id=defect_id)
                    defect.products.add(product)
                product.save()
            return redirect(".")
    else:
        product_form = ProductForm(data={'team_slug': team_slug})

    if request.is_ajax():
        if request.GET.get('product_id'):

            # import ipdb;
            # ipdb.set_trace()
            product_id = request.GET['product_id']
            product_name = Product.objects.filter(id=product_id).values('product_name')[
                0]['product_name']
            category_name = ProductCategory.objects.filter(id=Product.objects.filter(
                id=product_id).values('category_id')[0]['category_id'])[0].category_name
            type_code = Product.objects.filter(
                id=product_id).values('type_code')[0]['type_code']
            format_of_code = Product.objects.filter(id=product_id).values(
                'format_of_code')[0]['format_of_code']
            brand_name = Brand.objects.filter(id=Product.objects.filter(
                id=product_id).values('brand_id')[0]['brand_id'])[0].brand_name
            box_name = Box.objects.filter(id=Product.objects.filter(
                id=product_id).values('box_id')[0]['box_id'])[0].box_name
            serial_code = Product.objects.filter(id=product_id).values('serial_code')[
                0]['serial_code']
            product_query = Product.objects.filter(
                id=product_id).values('reference_code_id')
            if product_query:
                reference_code_id = product_query[0]['reference_code_id']
                reference_product_query = ReferenceProduct.objects.filter(
                    id=reference_code_id)
                if reference_product_query:
                    reference_code_name = ReferenceProduct.objects.filter(id=Product.objects.filter(
                        id=product_id).values('reference_code_id')[0]['reference_code_id'])[0].reference_code_label
                # caracterstics = Caracterstic.objects.filter(id=Product.objects.filter(id=product_id).values(
                #    'caracterstics')[0]['caracterstics']).values('caracterstic_label')[0]['caracterstic_label']
                else:
                    reference_code_name = None
            all_defects = Defect.objects.all().filter(team__name=team_slug)
            defect_list = []
            for defect in all_defects:
                defect_list.append({
                    'id': defect.id,
                    'name': defect.defect_name,
                })
            product = Product.objects.get(id=product_id)

            defect_products = Defect.objects.filter(
                products=product, team__name=team_slug)
            defect_product_list = []
            for defect_related in defect_products:
                defect_product_list.append({
                    'id': defect_related.id,
                    'name': defect_related.defect_name,

                })
            values = {
                'product_id': product_id,
                'product_name': product_name,
                'category_name': category_name,
                'type_code': type_code,
                'format_of_code': format_of_code,
                'box_name': box_name,
                'reference_code_name': reference_code_name,
                'brand_name': brand_name,
                'serial_code': serial_code,
                'defect_list': defect_list,
                'defect_products': defect_product_list

            }

            return JsonResponse({
                'values': values
            })
        if request.GET.get('reference_item_product'):
            product_id = request.GET.get('reference_item_product')
            product = Product.objects.get(id=product_id)
            reference = product.reference_code_id
            data = {
                'reference': {
                    'id': reference.id,
                    'reference_code_label': reference.reference_code_label,
                    'reference_code_value': reference.reference_code_value,
                }
            }
            return JsonResponse(data)
    category_ajax = ProductCategory.objects.all().filter(team__name=team_slug)
    products = Product.objects.all().filter(team__name=team_slug)
    boxs = Box.objects.all().filter(team__name=team_slug)
    brands = Brand.objects.all().filter(team__name=team_slug)
    reference_code_list = ReferenceProduct.objects.all().filter(team__name=team_slug)
    list_type_code = ['QrCode', 'ZebraCode', 'BarCode']
    defects = Defect.objects.all().filter(team__name=team_slug)
    context = {
        'category_ajax': category_ajax,
        'products': products,
        'product_form': product_form,
        'boxs': boxs,
        'reference_code_list': reference_code_list,
        'brands': brands,
        'list_type_code': list_type_code,
        'defects': defects

    }
    return TemplateResponse(request, "qualifeed/product.html", context)


@login_and_team_required
@csrf_exempt
def defectType(request, team_slug):
    if request.method == 'POST':  # If the form has been submitted...
        # import ipdb;
        # ipdb.set_trace()
        typedefect_form = DefectTypeForm(request.POST)
        if typedefect_form.is_valid:
            if 'id' in typedefect_form.data:
                defect_obj = DefectType.objects.get(
                    id=typedefect_form.data['id'])
                # Update the fields of the record
                defect_obj.defect_type_name = typedefect_form.data['type']
                defect_obj.defect_type = typedefect_form.data['defect-type'].split(
                )
                # defect_obj.pattern     = defect_form.data['pattern']
                defect_obj.save()
            else:
                defect_type_name = typedefect_form.data['defect_type_name']
                defect_type = typedefect_form.data['defect_type']
                defectType = DefectType.objects.create(
                    team_id=request.team.id, defect_type_name=defect_type_name, defect_type=defect_type.split())
                defectType.save()
                return redirect(".")
    else:
        typedefect_form = DefectTypeForm(data={'team_slug': team_slug})

    if request.is_ajax():
        # import ipdb;
        # ipdb.set_trace()
        if request.GET.get('defect_id') is None:
            defect_type_name = DefectType.objects.filter(
                defect_type_name=request.GET['defect_type'])
            defect_type = defect_type[0].defect_type
            values = None
        else:
            defect_id = request.GET['defect_id']
            defect_type_name = DefectType.objects.filter(id=defect_id).values(
                'defect_type_name')[0]['defect_type_name']
            defect_type = DefectType.objects.filter(
                id=defect_id).values('defect_type')[0]['defect_type']

            values = {
                'defect_id': defect_id,
                'defect_name': defect_type_name,
                'defect_type': defect_type,

            }
            defect_type_value = []

        return JsonResponse({
            'data': defect_type,
            'values': values
        })
    # import ipdb;
    # ipdb.set_trace()
    defect_type_ajax = DefectType.objects.all().filter(team__name=team_slug)

    defectsType = DefectType.objects.all().filter(team__name=team_slug)
    context = {
        'defectsType': defectsType,
        'typedefect_form': typedefect_form,
        'defect_type_ajax': defect_type_ajax
    }
    return TemplateResponse(request, "qualifeed/defetType.html", context)


@login_and_team_required
@csrf_exempt
def defect(request, team_slug):
    if request.method == 'POST':  # If the form has been submitted...
        # import ipdb
        # ipdb.set_trace()
        defect_form = DefectForm(request.POST)
        if defect_form.is_valid:
            if 'id' in defect_form.data:
                defect_obj = Defect.objects.get(id=defect_form.data['id'])
                # Update the fields of the record
                defect_obj.defect_name = defect_form.data['name']
                defect_obj.defect_type = DefectType.objects.get(
                    defect_type_name=defect_form.data['defect_type'])
                defect_obj.defect_type_value = defect_form.data['defect_type_value']
                defect_obj.description = defect_form.data['description']
                defect_obj.save()
                defect_products = defect_obj.products.all()
                products = defect_form.data.getlist('products')
                # Remove any existing relations not in the new list of products
                existing_products = set(defect_obj.products.all())
                new_products = set(Product.objects.filter(
                    id__in=defect_form.data.getlist('products')))
                to_remove = existing_products - new_products
                defect_obj.products.remove(*to_remove)

                for _ in products:
                    if _ not in defect_products:
                        defect_obj.products.add(_)
                defect_obj.save()
            else:
                # import ipdb;
                # ipdb.set_trace()
                defect_name = defect_form.data['defect_name']
                description = defect_form.data['description']
                defect_type_value = defect_form.data['defect_type_value']
                defect_type = defect_form.data['defect_type']
                pattern = defect_form.data['pattern']
                defect_type = DefectType.objects.get(
                    defect_type_name=defect_type)

                products = request.POST.getlist('products')
                defect = Defect.objects.create(team_id=request.team.id, pattern=pattern, defect_name=defect_name,
                                               defect_type_value=defect_type_value, description=description, defect_type=defect_type)
                defect.save()
                for _ in products:
                    defect.products.add(_)
                defect.save()
            for photo in request.FILES.getlist('photos'):
                DefectImage.objects.create(defect=defect, photo=photo)
            return redirect(".")
    else:
        defect_form = DefectForm(data={'team_slug': team_slug})

    if request.is_ajax():

        if request.GET.get('defect_type'):
            defect_type = DefectType.objects.filter(
                defect_type_name=request.GET['defect_type'])
            defect_type_value = defect_type[0].defect_type
            return JsonResponse({
                'data': defect_type_value
            })
        if request.GET.get('defect_id'):
            defect_id = request.GET['defect_id']
            defect_name = Defect.objects.filter(id=defect_id).values('defect_name')[
                0]['defect_name']
            description = Defect.objects.filter(id=defect_id).values('description')[
                0]['description']
            defect_type = DefectType.objects.filter(id=Defect.objects.filter(
                id=defect_id).values('defect_type')[0]['defect_type'])[0].defect_type_name
            defect_type_value = Defect.objects.filter(id=defect_id).values(
                'defect_type_value')[0]['defect_type_value']
            defect_type_list = DefectType.objects.filter(id=Defect.objects.filter(
                id=defect_id).values('defect_type')[0]['defect_type'])[0].defect_type

            all_products = Product.objects.all().filter(team__name=team_slug)
            product_list = []
            for product in all_products:
                product_list.append({
                    'id': product.id,
                    'name': product.product_name,
                })
            defect = Defect.objects.get(id=defect_id, team__name=team_slug)

            defect_products = defect.products.all().filter(team__name=team_slug)
            defect_product_list = []
            for product in defect_products:
                defect_product_list.append({
                    'id': product.id,
                    'name': product.product_name,

                })

            values = {
                'defect_id': defect_id,
                'defect_name': defect_name,
                'description': description,
                'defect_type': defect_type,
                'defect_type_value': defect_type_value,
                'defect_type_list': defect_type_list,
                'all_products': product_list,
                'defect_products': defect_product_list
            }

            # defect_type_value = []
            return JsonResponse({
                # 'data': defect_type_value,
                'values': values,
            })
        if request.GET.get('defect_item'):
            # import ipdb;
            # ipdb.set_trace()
            defect_id = request.GET['defect_item']
            product_id = request.GET['product_id']
            defect = Defect.objects.get(
                id=defect_id)
            product = Product.objects.get(
                id=product_id)
            defect.products.remove(product)
            return JsonResponse({'message': 'removed'}, status=200)
        if request.GET.get('defect_item_product'):
            defect_id = request.GET.get('defect_item_product')
            defect = Defect.objects.get(id=defect_id)
            products = defect.products.all()
            data = {
                'products': [{
                    'id': product.id,
                    'product_name': product.product_name,
                    'serial_code': product.serial_code,
                } for product in products]
            }
            return JsonResponse(data)

    # import ipdb;
    # ipdb.set_trace()
    defect_type_ajax = DefectType.objects.all().filter(team__name=team_slug)
    defects = Defect.objects.all().order_by('id').filter(team__name=team_slug)
    context = {
        'defects': defects,
        'defect_form': defect_form,
        'defect_type_ajax': defect_type_ajax
    }
    return TemplateResponse(request, "qualifeed/defect.html", context)


@login_and_team_required
@csrf_exempt
def checkControl(request, team_slug):
    if request.method == 'POST':  # If the form has been submitted...
        # import ipdb;
        # ipdb.set_trace()
        checkdefect_form = CheckControlForm(request.POST)
        if checkdefect_form.is_valid:

            if 'id' in checkdefect_form.data:
                # import ipdb;
                # ipdb.set_trace()
                id = int(checkdefect_form.data['id'])
                control_obj = CheckControl.objects.get(id=id)
                # Update the fields of the record
                # control_obj.category_name = ProductCategory.objects.get(category_name=checkdefect_form.data['category_name'])
                defect_name = checkdefect_form.data['defect_name']
                threshold = checkdefect_form.data['threshold']
                post = checkdefect_form.data['post']
                user = checkdefect_form.data['user'].replace(
                    "<", "").replace(">", "")
                user = CustomUser.objects.get(email=user)
                box_id = checkdefect_form.data['box']
                box_name = Box.objects.get(box_name=box_id)
                defect_name = Defect.objects.get(defect_name=defect_name)

                control_obj.defect_id = defect_name
                control_obj.box_id = box_name
                control_obj.user = user
                control_obj.post = post
                control_obj.save()

            else:
                defect_name = checkdefect_form.data['defect_name']
                threshold = checkdefect_form.data['threshold']
                category_name = checkdefect_form.data['category']
                post = checkdefect_form.data['post']
                category_name = ProductCategory.objects.get(
                    category_name=category_name)
                user = checkdefect_form.data['user']
                user = CustomUser.objects.get(id=user)
                box_id = checkdefect_form.data['box_id']
                box_name = Box.objects.get(id=box_id)
                defect_name = Defect.objects.get(defect_name=defect_name)

                checkControl = CheckControl.objects.create(
                    team_id=request.team.id, threshold=threshold, defect_id=defect_name, post=post, box_id=box_name, user=user)
                checkControl.save()

            return redirect(".")
    else:
        checkdefect_form = CheckControlForm(data={'team_slug': team_slug})

    if request.is_ajax():
        # import ipdb;
        # ipdb.set_trace()

        if request.GET.get('alert_id') is None:
            # import ipdb;
            # ipdb.set_trace()
            category_name = request.GET['category']
            if Product.objects.filter(category_id__category_name=category_name).exists():
                products = Product.objects.filter(
                    category_id__category_name=category_name)
                defects = []
                for product in products:
                    defects.extend(product.defects.all())
                names = [obj.defect_name for obj in defects]
                names = []

                for obj in defects:
                    if obj.defect_name not in names:
                        names.append(obj.defect_name)
            else:
                names = []
            values = None

        else:
            # import ipdb;
            # ipdb.set_trace()
            alert_id = request.GET['alert_id']
            defect_id = Defect.objects.filter(id=CheckControl.objects.filter(
                id=alert_id).values('defect_id')[0]['defect_id'])[0].defect_name
            threshold = CheckControl.objects.filter(
                id=alert_id).values('threshold')[0]['threshold']
            post = CheckControl.objects.filter(
                id=alert_id).values('post')[0]['post']
            box_id = Box.objects.filter(id=CheckControl.objects.filter(
                id=alert_id).values('box_id')[0]['box_id'])[0].box_name
            user = CustomUser.objects.filter(id=CheckControl.objects.filter(
                id=alert_id).values('user')[0]['user'])[0].email
            product_id = Defect.objects.filter(
                defect_name=defect_id).values('products')[0]['products']
            category_id = Product.objects.filter(id=product_id).values('category_id')[
                0]['category_id']
            category_name = ProductCategory.objects.filter(
                id=category_id).values('category_name')[0]['category_name']
            defects = Defect.objects.filter(products=product_id)
            # values = list(defects)
            # data = serializers.serialize('json', values)
            names = [obj.defect_name for obj in defects]
            values = {
                'alert_id': alert_id,
                'defect_id': defect_id,
                'threshold': threshold,
                'post': post,
                'box_id': box_id,
                'user': user,
                'category_name': category_name
            }
        return JsonResponse({
            'names': names,
            'values': values
        })

    display_category = ProductCategory.objects.all().filter(team__name=team_slug)
    checkControls = CheckControl.objects.all().filter(team__name=team_slug)
    display_defect = Defect.objects.all().filter(team__name=team_slug)
    display_box = Box.objects.all().filter(team__name=team_slug)
    display_user = CustomUser.objects.all()

    context = {
        'display_category': display_category,
        'checkControls': checkControls,
        'checkdefect_form': checkdefect_form,
        'display_defect': display_defect,
        'display_box': display_box,
        'display_user': display_user
    }
    return TemplateResponse(request, "qualifeed/checkControl.html", context)


@login_and_team_required
@csrf_exempt
def box(request, team_slug):
    # import ipdb;
    # ipdb.set_trace()

    if request.method == 'POST':  # If the form has been submitted...

        box_form = BoxForm(request.POST)

        if box_form.is_valid:
            # import ipdb;
            # ipdb.set_trace()
            if 'id' in box_form.data:
                box_obj = Box.objects.get(id=box_form.data['id'])
             # Update the fields of the record
                box_obj.box_name = box_form.data['name']
                box_obj.qte = box_form.data['qte']

                if box_form.data['parent']:
                    box_parent = Box.objects.get(
                        box_name=box_form.data['parent'])

                    box_obj.parent = box_parent

                box_obj.save()
            else:

                box_name = box_form.data['box_name']
                qte = box_form.data['qte']
                boxes = request.POST.getlist('boxes')

                if box_form.data['parent']:
                    parent = box_form.data['parent']
                    box_object = Box.objects.get(box_name=parent)
                    box = Box(team_id=request.team.id,
                              box_name=box_name, qte=qte, parent=box_object)

                else:
                    box = Box(team_id=request.team.id,
                              box_name=box_name, qte=qte)

                box.save()
            return redirect(".")

    else:
        # import ipdb;
        # ipdb.set_trace()
        box_form = BoxForm(data={'team_slug': team_slug})

    if request.is_ajax():
        # import ipdb;
        # ipdb.set_trace()

        # values=None
        box_id = request.GET['box_id']

        box_name = Box.objects.filter(id=box_id).values('box_name')[
            0]['box_name']
        parent = Box.objects.filter(id=box_id).values('parent')[0]['parent']
        qte = Box.objects.filter(id=box_id).values('qte')[0]['qte']

        if parent is None:
            parent = None
        else:
            parent = Box.objects.filter(id=Box.objects.filter(
                id=box_id).values('parent')[0]['parent'])[0].box_name

        values = {
            'box_id': box_id,
            'parent': parent,
            'box_name': box_name,
            'qte': qte

        }
        return JsonResponse({
            'values': values
        })
    box_ajax = Box.objects.all().filter(team__name=team_slug)
    boxes = Box.objects.all().filter(team__name=team_slug)

    context = {
        'box_ajax': box_ajax,
        'boxes': boxes,
        'box_form': box_form,
    }
    return TemplateResponse(request, "qualifeed/box.html", context)


@login_and_team_required
@csrf_exempt
def user(request, team_slug):
    if request.method == 'POST':  # If the form has been submitted...
        # import ipdb;
        # ipdb.set_trace()
        user_form = UserForm(request.POST)
        if user_form.is_valid:

            if 'id' in user_form.data:
                # import ipdb;
                # ipdb.set_trace()
                user_obj = CustomUser.objects.get(id=user_form.data['id'])
             # Update the fields of the record
                user_obj.email = user_form.data['email'].replace(
                    "<", "").replace(">", "")
                user_obj.poste = user_form.data['poste']
                user_obj.code_user = user_form.data['code_user']
                user_obj.save()
                user_products = user_obj.products.all()
                products = user_form.data.getlist('products')
                for _ in products:
                    if _ not in user_products:
                        user_obj.products.add(_)
                user_obj.save()

            else:
                # import ipdb;
                # ipdb.set_trace()
                email = user_form.data['email']
                user_obj = CustomUser.objects.get(id=email)
                user_obj.code_user = user_form.data['code_user']
                user_obj.poste = user_form.data['poste']
                user_obj.save()
                products = user_form.data.getlist('products')
                for _ in products:
                    user_obj.products.add(_)
                user_obj.save()
            return redirect(".")

    else:
        user_form = UserForm()
    if request.is_ajax():
        # import ipdb;
        # ipdb.set_trace()
        if request.GET.get('user_id'):
            user_id = request.GET['user_id']
            email = CustomUser.objects.filter(
                id=user_id).values('email')[0]['email']
            code_user = CustomUser.objects.filter(
                id=user_id).values('code_user')[0]['code_user']
            poste = CustomUser.objects.filter(
                id=user_id).values('poste')[0]['poste']

            all_products = Product.objects.all()
            product_list = []
            for product in all_products:
                product_list.append({
                    'id': product.id,
                    'name': product.product_name,
                })
            user = CustomUser.objects.get(id=user_id)

            user_products = user.products.all()
            user_product_list = []
            for product in user_products:
                user_product_list.append({
                    'id': product.id,
                    'name': product.product_name,

                })
            values = {
                'user_id': user_id,
                'email': email,
                'code_user': code_user,
                'poste': poste,
                'all_products': product_list,
                'user_products': user_product_list
            }

            return JsonResponse({'values': values})
        if request.GET.get('user'):
            user_id = request.GET['user']
            product_id = request.GET['product_id']
            user = CustomUser.objects.get(
                id=user_id)
            product = Product.objects.get(
                id=product_id)
            user.products.remove(product)
            return JsonResponse({'message': 'removed'}, status=200)
        if request.GET.get('user_item_product'):
            user_id = request.GET.get('user_item_product')
            user = CustomUser.objects.get(id=user_id)
            products = user.products.all()
            data = {
                'products': [{
                    'id': product.id,
                    'product_name': product.product_name,
                    'serial_code': product.serial_code,
                } for product in products]
            }
            return JsonResponse(data)

    user_ajax = CustomUser.objects.all()
    users = CustomUser.objects.all().order_by('id')
    all_products = Product.objects.all()

    context = {
        'user_ajax': user_ajax,
        'users': users,
        'user_form': user_form,
        'all_products': all_products
    }
    return TemplateResponse(request, "qualifeed/user.html", context)


@login_and_team_required
def logs(request, team_slug):
    last_three_controls_with_defects = {}
    controls = {}
    control_count = {}
    post_list = {}
    last_updated_control = {}
    last_defect = {}
    last_user_control_email = {}
    last_control = {}
    latest_repair = {}
    last_product = {}
    results = {}
    users = {}
    products = {}
    defects = {}
    defects_pareto_data = []
    # import ipdb;
    # ipdb.set_trace()
    controls = Control.objects.filter(team__name=team_slug).order_by('-id').prefetch_related(
        Prefetch('defect_id', queryset=Defect.objects.only('defect_name'))
    )

    control_list = []

    for control in controls:
        # Get the control details
        try:
            serial_code_box = SerialCodeBox.objects.get(control_id=control.id)
            nbr_of_good_product = serial_code_box.nbr_of_good_product
        except SerialCodeBox.DoesNotExist:
            nbr_of_good_product = None
        defect_counts = 0
        for defect_name in control.defect_id.all():
            # defect = Defect.objects.get(id=defect_name)
            defect = HaveDefect.objects.filter(
                serial_code__product_name=control.serial_code.product_name,
                defect_id__defect_name=defect_name,
                control_id=control.id
            )
            if defect.exists():
                defect_counts += defect.values('number_defect')[
                    0]['number_defect']
        control_details = {
            'id': control.id,
            'date_control': control.date_control,
            'details_control': control.details_control,
            'time_control': control.time_control,
            'state_control': control.state_control,
            'nbr_of_good_product': nbr_of_good_product,
            'photo_control': control.photo_control,
            'user': control.user.email,
            'serial_code': control.serial_code.product_name,
            'qte': control.serial_code.box_id.qte,
            'defect_counts': defect_counts,
        }

        # Get the associated defects as an array
        defect_list = []
        for defect in control.defect_id.all():
            defect_list.append(defect.defect_name)

        # Add the defect array to the control details
        control_details['defects'] = defect_list

        # Add the control details to the list
        control_list.append(control_details)

        defects = Defect.objects.all()
        defects_pareto_data = []
        for defect in defects:
            number_defect = HaveDefect.objects.filter(
                defect_id=defect).aggregate(Sum('number_defect'))
            defects_pareto_data.append({
                'defect_name': defect.defect_name,
                'number_defect': number_defect['number_defect__sum'] if number_defect['number_defect__sum'] else 0
            })

    now = timezone.now()
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end = start.replace(month=start.month+1, day=1) - \
        timezone.timedelta(microseconds=1)
    if Control.objects.exists():
        # get the count of controls that were created in the current month
        control_count = Control.objects.filter(
            created_at__gte=start, created_at__lte=end, team__name=team_slug).count()
        last_updated_control = Control.objects.latest('updated_at')
        last_control = Control.objects.latest('created_at')
        last_user_control_email = last_control.user.email
        last_product = last_control.serial_code.product_name
        # Combine results into a dictionary keyed by date
        checks_per_day = Control.objects.filter(date_control__range=[start, end]).annotate(
            date=TruncDate('date_control')).values('date').annotate(count=Count('id'))
        results = {}
        for entry in checks_per_day:
            results[entry['date']] = {'checks': entry['count'], 'repairs': 0}

        # Count number of checks and group by checks_per_day
        last_three_controls_with_defects = Control.objects.order_by(
            '-date_control')[:3]

        for control in last_three_controls_with_defects:
            num_defects = control.defect_id.count()

    else:
        control_count = 0
        last_updated_control = {}
        last_control = {}
        last_user_control_email = "Doesn't exist"
        last_product = "Doesn't exist"
        last_three_controls_with_defects = {}
        results = {}
    if Defect.objects.exists():
        last_defect = Defect.objects.latest('defect_name')
    else:
        last_defect = "Doesn't exist"
    if Reperation.objects.exists():

        # Get the current month
        now = timezone.now()
        latest_repair = Reperation.objects.order_by(
            '-date_reperation', '-time_reperation').first()
    else:
        latest_repair = "Doesn't exist"

    team = Team.objects.get(slug=team_slug)

    # retrieve all the membership objects related to the team
    memberships = Membership.objects.filter(team=team)

    # get the user IDs of all the users in the team
    user_ids = memberships.values_list('user_id', flat=True)

    # retrieve all the users with the IDs obtained in the previous step
    users = CustomUser.objects.filter(id__in=user_ids)
    products = Product.objects.all().filter(team__name=team_slug)
    defects = Defect.objects.all().filter(team__name=team_slug)

    post_list = []
    for item in users:
        if item.poste not in post_list and item.poste is not None and item.poste != "":
            post_list.append(item.poste)
    if request.is_ajax():
        #import ipdb;
        #ipdb.set_trace()
        if request.GET.get('end_date'):
            # import ipdb;
            # ipdb.set_trace()
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
            end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
            data = Control.objects.filter(date_control__range=(
                start_datetime, end_datetime), team__name=team_slug)
            controls_per_day = data.values('date_control').annotate(
                num_controls=Count('id')).order_by('date_control')
            chart_data = {'dates': [], 'num_controls': []}
            for control in controls_per_day:
                chart_data['dates'].append(
                    control['date_control'].strftime('%Y-%m-%d'))
                chart_data['num_controls'].append(control['num_controls'])

            return JsonResponse({
                "chart_data": chart_data
            })
        if request.GET.get('product_ref_chart') or request.GET.get('poste') or request.GET.get('end_date_chart') or request.GET.get('user_chart') or request.GET.get('product_chart') or request.GET.get('defect_chart'):
            # import ipdb
            # ipdb.set_trace()
            post = request.GET.get('poste')
            start_date_chart = request.GET.get('start_date_chart')
            end_date_chart = request.GET.get('end_date_chart')
            if request.GET.get('user_chart'):
                user_chart = request.GET.get('user_chart').replace(
                    '<', '').replace('>', '').strip()
            product_chart = request.GET.get('product_chart')
            product_ref_chart = request.GET.get('product_ref_chart')

            defect_chart = request.GET.get('defect_chart')
            filter_args = {'team__name': team_slug}
            if post:
                filter_args['user__poste'] = post
            if start_date_chart and end_date_chart:
                filter_args['date_control__range'] = (
                    start_date_chart, end_date_chart)
            if request.GET.get('user_chart'):
                filter_args['user__email'] = user_chart
            if product_chart:
                filter_args['serial_code__product_name'] = product_chart
            if product_ref_chart:
                filter_args['serial_code__serial_code'] = product_ref_chart
            if defect_chart:
                filter_args['defect_id__defect_name'] = defect_chart
            datacontrol = Control.objects.filter(**filter_args)\
                .annotate(day=TruncDay('date_control'))\
                .values('day')\
                .annotate(count=Count('id'))\
                .order_by('day')

            labels = []
            data = []
            for item in datacontrol:
                labels.append(item['day'].strftime('%Y-%m-%d'))
                data.append(item['count'])
            return JsonResponse({
                "data": data,
                "labels": labels
            })
        if request.GET.get('user_pareto_chart') or request.GET.get('start_date_pareto_chart') or request.GET.get('end_date_pareto_chart') or request.GET.get('product_pareto_chart'):

            user_pareto_chart = request.GET.get('user_pareto_chart')
            end_date_pareto_chart = request.GET.get('end_date_pareto_chart')
            start_date_pareto_chart = request.GET.get(
                'start_date_pareto_chart')

            product_pareto_chart = request.GET.get('product_pareto_chart')
            filter_args = {'team__name': team_slug}
            if user_pareto_chart:
                filter_args['control_id__user__email'] = user_pareto_chart
            if start_date_pareto_chart and end_date_pareto_chart:
                filter_args['control_id__date_control__range'] = (
                    start_date_pareto_chart, end_date_pareto_chart)
            if request.GET.get('product_pareto_chart'):
                filter_args['serial_code__product_name'] = product_pareto_chart

            defects = Defect.objects.all()
            defects_pareto_data = []
            for defect in defects:
                filter_args['defect_id'] = defect

                number_defect = HaveDefect.objects.filter(
                    **filter_args).aggregate(Sum('number_defect'))
                defects_pareto_data.append({
                    'defect_name': defect.defect_name,
                    'number_defect': number_defect['number_defect__sum'] if number_defect['number_defect__sum'] else 0
                })
            return JsonResponse({
                'defectsPareto': defects_pareto_data

            })
        if request.GET.get('reset'):
            controls = Control.objects.filter(team__name=team_slug).order_by('-id').prefetch_related(
                Prefetch('defect_id', queryset=Defect.objects.only('defect_name'))
            )

            controls_dis = []

            for control in controls:
                # Get the control details
                try:
                    serial_code_box = SerialCodeBox.objects.get(
                        control_id=control.id)
                    nbr_of_good_product = serial_code_box.nbr_of_good_product
                except SerialCodeBox.DoesNotExist:
                    nbr_of_good_product = None
                defect_counts = 0
                for defect_name in control.defect_id.all():
                    # defect = Defect.objects.get(id=defect_name)
                    defect = HaveDefect.objects.filter(
                        serial_code__product_name=control.serial_code.product_name,
                        defect_id__defect_name=defect_name,
                        control_id=control.id
                    )
                    if defect.exists():
                        defect_counts += defect.values('number_defect')[
                            0]['number_defect']
                control_details = {
                    'id': control.id,
                    'date_control': control.date_control,
                    'details_control': control.details_control,
                    'time_control': control.time_control,
                    'state_control': control.state_control,
                    'nbr_of_good_product': nbr_of_good_product,
                    'user__username': control.user.email,
                    'serial_code__product_name': control.serial_code.product_name,
                    'qte': control.serial_code.box_id.qte,
                    'defect_counts': defect_counts,
                }

                # Get the associated defects as an array
                defect_list = []
                for defect in control.defect_id.all():
                    defect_list.append(defect.defect_name)

                # Add the defect array to the control details
                control_details['defects'] = defect_list

                # Add the control details to the list
                controls_dis.append(control_details)
            return JsonResponse({
                "controls_dis": controls_dis
            })
        if request.GET.get('user_csv') or request.GET.get('defect_name_csv') or request.GET.get('product_name_csv') or request.GET.get('start_date_csv'):
            user = request.GET.get('user_csv')

            product_name = request.GET.get('product_name_csv')
            defect_name = request.GET.get('defect_name_csv')
            start_date = request.GET.get('start_date_csv')
            end_date = request.GET.get('end_date_csv]')
            filter_args = {'team__name': team_slug}

            if user:
                filter_args['user__username'] = user

            if product_name:
                filter_args['serial_code__product_name'] = product_name
            if defect_name:
                filter_args['defect_id__defect_name'] = defect_name
            if start_date and end_date:
                filter_args['date_control__range'] = (start_date, end_date)

            controls = Control.objects.filter(**filter_args).values(
                'date_control',
                'details_control',
                'time_control',
                'nbr_of_good_product',
                'photo_control',
                'user__username',
                'defect_id__defect_name',
                'serial_code__product_name',
            )
            controls_list_csv = list(controls)
            return JsonResponse({
                "controls_list_csv": controls_list_csv
            })
        if request.GET.get('show_control_id'):
            control_id = request.GET.get('show_control_id')
            defectsArray = request.GET.getlist('show_defect_id[]')
            product_name = request.GET.get('show_product_id')
            # product = Product.objects.get(id=product_name)
            defect_counts = {}
            # import ipdb;
            # ipdb.set_trace()
            for defect_name in defectsArray:
                # defect = Defect.objects.get(id=defect_name)

                defect = HaveDefect.objects.filter(
                    serial_code__product_name=product_name,
                    defect_id__defect_name=defect_name.strip(),
                    control_id=control_id
                )
                if defect.exists():
                    defect_counts[defect_name] = defect.values('number_defect')[
                        0]['number_defect']
                else:
                    defect_counts[defect_name] = 0

            return JsonResponse({'defect_counts': defect_counts})
        if request.GET.get('control_id_image'):
            images = ImageControl.objects.filter(
                control_id=request.GET.get('control_id_image'))
            image_urls = [image.photo_control.url for image in images]
            return JsonResponse({'image_urls': image_urls})

        else:
            # import ipdb;
            # ipdb.set_trace()
            # Get the filter parameters from the request
            user = request.GET.get('formData[user]')
            product_name = request.GET.get('formData[product_name]')
            product_ref = request.GET.get('formData[product_ref]')
            defect_name = request.GET.get('formData[defect_name]')
            start_date = request.GET.get('formData[start_date]')
            end_date = request.GET.get('formData[end_date]')

            # Build the filter arguments for the Control objects
            filter_args = {'team__name': team_slug}
            if user:
                filter_args['user__username'] = user
            if product_name:
                filter_args['serial_code__product_name'] = product_name
            if product_ref:
                filter_args['serial_code__serial_code'] = product_ref
            if defect_name:
                filter_args['defect_id__defect_name'] = defect_name
            if start_date and end_date:
                filter_args['date_control__range'] = (start_date, end_date)

            # Filter the Control objects and prefetch the related Defect objects
            controls = Control.objects.filter(
                **filter_args).order_by('-id').prefetch_related('defect_id')

            # Build a list of control details, including a list of defects for each control
            controls_list = []
            for control in controls:
                try:
                    serial_code_box = SerialCodeBox.objects.get(
                        control_id=control.id)
                    nbr_of_good_product = serial_code_box.nbr_of_good_product
                except SerialCodeBox.DoesNotExist:
                    nbr_of_good_product = None
                defect_counts = 0
                for defect_name in control.defect_id.all():
                    # defect = Defect.objects.get(id=defect_name)
                    defect = HaveDefect.objects.filter(
                        serial_code__product_name=control.serial_code.product_name,
                        defect_id__defect_name=defect_name,
                        control_id=control.id
                    )
                    if defect.exists():
                        defect_counts += defect.values('number_defect')[
                            0]['number_defect']

                control_details = {
                    'id': control.id,
                    'date_control': control.date_control,
                    'details_control': control.details_control,
                    'time_control': control.time_control,
                    'state_control': control.state_control,
                    'nbr_of_good_product': nbr_of_good_product,
                    'user__username': control.user.username,
                    'serial_code__product_name': control.serial_code.product_name,
                    'defects': [defect.defect_name for defect in control.defect_id.all()],
                    'qte': control.serial_code.box_id.qte,
                    "defect_counts": defect_counts,
                }
                controls_list.append(control_details)

            return JsonResponse({
                "controls_list": controls_list

            })
    image_controls = ImageControl.objects.all()

    return TemplateResponse(request, "qualifeed/logs.html", context={
        'defectsPareto': defects_pareto_data,
        'last_three_controls_with_defects': last_three_controls_with_defects,
        'controls': control_list,
        'control_count': control_count,
        'post_list': post_list,
        'last_updated_control': last_updated_control,
        'last_defect': last_defect,
        'last_user_control_email': last_user_control_email,
        'last_control': last_control,
        'latest_repair': latest_repair,
        'last_product': last_product,
        'results': results,
        'users': users,
        'products': products,
        'defects': defects,
        'image_controls': image_controls
    })


@ login_and_team_required
def reparation(request, team_slug):
    users = {}
    Reparations = {}
    products = {}
    defects = {}
    post_list = {}
    total_reparations = {}
    last_three_reparations = {}
    latest_repair = {}
    last_three_repairs = {}
    latest_repair_defect = {}
    latest_repair_date = {}
    latest_repair_user = {}
    latest_repair_product = {}
    Reparations = Reperation.objects.all().filter(team__name=team_slug).values(
        'date_reperation',
        'details_reperation',
        'time_reperation',
        'state_reperation',
        'photo_reperation',
        'defect_id__defect_name',
        'control_id',
        'user__username'
    )
    team = Team.objects.get(slug=team_slug)

    # retrieve all the membership objects related to the team
    memberships = Membership.objects.filter(team=team)

    # get the user IDs of all the users in the team
    user_ids = memberships.values_list('user_id', flat=True)

    # retrieve all the users with the IDs obtained in the previous step
    users = CustomUser.objects.filter(id__in=user_ids)
    post_list = []
    for item in users:
        if item.poste not in post_list and item.poste is not None and item.poste != "":
            post_list.append(item.poste)

    if Product.objects.exists():
        products = Product.objects.all().filter(team__name=team_slug)
    else:
        products = {}
    if Product.objects.exists():
        defects = Defect.objects.all().filter(team__name=team_slug)
    else:
        defects = {}
    if Reperation.objects.exists():

        # Get the current month
        now = timezone.now()
        month_start = now.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0)

        # Get the total number of repairs done this month
        total_reparations = Reperation.objects.filter(
            team__name=team_slug, date_reperation__gte=month_start).count()

        latest_repair = Reperation.objects.order_by(
            '-date_reperation', '-time_reperation').first()

        if latest_repair:

            # Get the date of the last repair
            latest_repair_date = latest_repair.date_reperation

            # Get the user who performed the last repair
            latest_repair_user = latest_repair.user.username
            # Get the defect of the last repair
            latest_repair_defect = latest_repair.defect_id.defect_name
            if Reperation.objects.filter(control_id__isnull=False).exists():
                # Get the product of the last repair
                latest_repair_product = Reperation.objects.filter(control_id__isnull=False).latest(
                    'date_reperation').control_id.serial_code.product_name
            else:
                latest_repair_product = "Does not exist"

        else:
            # Handle the case where there are no repairs
            latest_repair_date = "Unknown"
            latest_repair_user = "Unknown"
            latest_repair_defect = "Unknown"
            # latest_repair_product = "Unknown"

        # Get the current day
        end_date = date.today()
        start_date = end_date - timedelta(days=30)

        # Retrieve the last three Reperation instances done in the last month

        current_date = timezone.now().date()

        last_three_repairs = Reperation.objects.filter(
            date_reperation__lte=current_date
        ).order_by('-date_reperation', '-time_reperation')[:3]

        last_three_reparations = Reperation.objects.filter(
            date_reperation__range=[start_date, end_date]).order_by('-date_reperation')[:3]

    else:
        total_reparations = 0
        latest_repair = {}
        last_three_repairs = {}
        last_three_reparations = {}
        latest_repair_defect = "Doesn't exist"
        latest_repair_date = "Doesn't exist"
        latest_repair_user = "Doesn't exist"
        latest_repair_product = "Doesn't exist"

    if request.is_ajax():
        # import ipdb;
        # ipdb.set_trace()
        if request.GET.get('formData[user]') or request.GET.get('formData[status]') or request.GET.get('formData[product_name]') or request.GET.get('formData[defect_name]') or request.GET.get('formData[start_date]'):
            user = request.GET.get('formData[user]').replace(
                '<', '').replace('>', '').strip()
            status = request.GET.get('formData[status]')
            product_name = request.GET.get('formData[product_name]')
            defect_name = request.GET.get('formData[defect_name]')
            start_date = request.GET.get('formData[start_date]')
            end_date = request.GET.get('formData[end_date]')
            filter_args = {'team__name': team_slug}

            if user:
                filter_args['user__username'] = user
            if status:
                filter_args['state_reperation'] = status
            if product_name:
                filter_args['defect_id__products__product_name'] = product_name
            if defect_name:
                filter_args['defect_id__defect_name'] = defect_name
            if start_date and end_date:
                filter_args['date_reperation__range'] = (start_date, end_date)

            reparations = Reperation.objects.filter(**filter_args).values(
                'date_reperation',
                'details_reperation',
                'time_reperation',
                'state_reperation',
                'photo_reperation',
                'defect_id__defect_name',
                'control_id',
                'user__username'
            )
            reparation_list = list(reparations)
            return JsonResponse({
                "reparation_list": reparation_list

            })
        if request.GET.get('reset'):
            Reparations = Reperation.objects.all().filter(team__name=team_slug).values(
                'date_reperation',
                'details_reperation',
                'time_reperation',
                'state_reperation',
                'photo_reperation',
                'defect_id__defect_name',
                'control_id',
                'user__username'
            )
            reparation_list = list(Reparations)
            return JsonResponse({
                "reparation_list": reparation_list
            })
        if request.GET.get('poste') or request.GET.get('end_date_chart') or request.GET.get('user_chart') or request.GET.get('product_chart') or request.GET.get('defect_chart'):
            # import ipdb
            # ipdb.set_trace()
            post = request.GET.get('poste')
            start_date_chart = request.GET.get('start_date_chart')
            end_date_chart = request.GET.get('end_date_chart')
            if request.GET.get('user_chart'):
                user_chart = request.GET.get('user_chart').replace(
                    '<', '').replace('>', '').strip()
            product_chart = request.GET.get('product_chart')
            defect_chart = request.GET.get('defect_chart')
            filter_args = {'team__name': team_slug}
            if post:
                filter_args['user__poste'] = post
            if start_date_chart and end_date_chart:
                filter_args['date_reperation__range'] = (
                    start_date_chart, end_date_chart)
            if request.GET.get('user_chart'):
                filter_args['user__username'] = user_chart
            if product_chart:
                filter_args['defect_id__products__product_name'] = product_chart
            if defect_chart:
                filter_args['defect_id__defect_name'] = defect_chart
            data_reparation = Reperation.objects.filter(**filter_args)\
                .annotate(day=TruncDay('date_reperation'))\
                .values('day')\
                .annotate(count=Count('id'))\
                .order_by('day')

            labels = []
            data = []
            for item in data_reparation:
                labels.append(item['day'].strftime('%Y-%m-%d'))
                data.append(item['count'])
            return JsonResponse({
                "data": data,
                "labels": labels
            })
    context = {
        'users': users,
        'Reparations': Reparations,
        'products': products,
        'defects': defects,
        'post_list': post_list,
        'total_reparations': total_reparations,
        'last_three_reparations': last_three_reparations,
        'latest_repair': latest_repair,
        'last_three_repairs': last_three_repairs,
        'latest_repair_defect': latest_repair_defect,
        'latest_repair_date': latest_repair_date,
        'latest_repair_user': latest_repair_user,
        'latest_repair_product': latest_repair_product,

    }
    return TemplateResponse(request, "qualifeed/repar_logs.html", context)


@ login_and_team_required
def photo(request, team_slug):
    if Product.objects.exists():
        products = Product.objects.all().filter(team__name=team_slug)
    else:
        products = {}
    if Product.objects.exists():
        defects = Defect.objects.all().filter(team__name=team_slug)
    else:
        defects = {}
    image_controls = ImageControl.objects.all()
    if request.is_ajax():
        if request.GET.get('product_name_image'):
            images = ImageControl.objects.filter(
                control_id__serial_code_id=request.GET.get('product_name_image'))
            image_urls = [image.photo_control.url for image in images]
            return JsonResponse({'image_urls': image_urls})
        if request.GET.get('defect_name_image'):
            images = DefectImage.objects.filter(
                defect__id=request.GET.get('defect_name_image'))
            image_urls = [image.photo.url for image in images]
            return JsonResponse({'image_urls': image_urls})
    context = {
        'defects': defects,
        'image_controls': image_controls,
        'products': products
    }
    return TemplateResponse(request, "qualifeed/photos.html", context)




@csrf_exempt
def webhook(request,team_slug):
 # Get the user's request from the Dialogflow webhook request
  # Parse the request data
   #import ipdb;
   #ipdb.set_trace()
   req = request.body.decode('utf-8') # convert bytes to string
   req_dict = json.loads(req) # convert string to dictionary
   intent_name = req_dict['queryResult']['intent']['displayName']
    # Extract the date parameter from the request, if it exists
   parameters = req_dict['queryResult']['parameters']
   date_str = parameters.get('date')
   if date_str:
       date_obj = datetime.fromisoformat(date_str)
   else:
       date_obj = date.today()
    

   # Call your business logic to generate a response
   if intent_name == 'Control':
       # Use Django ORM to fetch data from the database
      
        controls = Control.objects.filter(date_control=date_obj)
        control_count = controls.count()      
        if control_count > 0:
           user_names = ', '.join([control.user.username for control in controls])
           response_text = f"{control_count} controls were affected on {date_obj.strftime('%Y-%m-%d')}. The controls were made by: {user_names}."
        else:
             response_text = f"No controls today."

  
   elif intent_name == 'Controlcount':
       # Use Django ORM to fetch data from the database
       total_controls = Control.objects.count()
       response_text = f"Total controls: {total_controls}"
          
   elif intent_name == 'Product_Defect':
       # Use Django ORM to fetch data from the database
      # product_name = parameters.get('product_name')
      # product = Product.objects.filter(product_name__icontains=product_name).first()
      # 
      # if product:
      #     defects = product.defects.filter(date_control=date_obj)
      #     defect_count = defects.count()
      #     defect_names = ', '.join([defect.defect_name for defect in defects])
      #     
      #     response_text = f"{defect_count} defects were found for product {product.product_name} on {date_obj.strftime('%Y-%m-%d')}. The defects were: {defect_names}."
      # else:
      #     response_text = f"Sorry, I couldn't find a product with the name {product_name} in the database."
        products = Product.objects.all()
        response_text = "Here are the defect counts for each product: "

        for product in products:
            defect_count = product.defects.count()
            if defect_count > 0:
                        response_text += f"\n{product.product_name}: {defect_count} defects found."
   elif intent_name == 'Distribution':
       # Use Django ORM to fetch data from the database
       products = Product.objects.all()
   
       if products.exists():
           response_text = "Defect types for all products:\n"
           for product in products:
               defects = Defect.objects.filter(product=product)
               defect_types = [defect.defect_type for defect in defects]
               defect_types_str = ', '.join(defect_types)
               response_text += f"{product.name}: {defect_types_str}\n"
       else:
           response_text = "No product data available."

   
   elif intent_name == 'Defect':
       defects = Defect.objects.all()
       response_text = "Here are the the list of defect name: "
       defect_counts = [f"\n the defect {defect.defect_name}  was created at {defect.created_at.date()}" for defect in defects]
       response_text = ", ".join(defect_counts) 
   
   elif intent_name == 'Defect_type':
        defect_types = DefectType.objects.all()
        response_text = "Here are the defect types for each defect: "
        for defect_type in defect_types:
            defects = defect_type.defect_set.all()
            defect_names = ', '.join([defect.defect_name for defect in defects])
            response_text += f"\n{defect_type.defect_type_name}: {defect_names}."

   elif intent_name == 'CommonControl':
        # Use Django ORM to fetch data from the database
       defect_records = Control.objects.all()
   
       if defect_records.exists():
           defect_types = [defect.defect_type for defect in defect_records]
           defect_counts = Counter(defect_types)
           most_common_defect = defect_counts.most_common(1)[0][0]
   
           response_text = f"The most frequently occurring defect type is: {most_common_defect}\n"
   
           total_defects = len(defect_types)
   
           response_text += "Defect percentages:\n"
           for defect, count in defect_counts.items():
               percentage = (count / total_defects) * 100
               response_text += f"{defect}: {percentage:.2f}%\n"
       else:
          response_text = "No defect data available."
     
   elif intent_name == 'ProductQuality':
       
         # Use Django ORM to fetch data from the database
        products = Product.objects.all()
        response_text = "Here are the defect counts for each product: "

        for product in products:
            defect_count = product.defects.count()
            if defect_count > 0:
                        response_text += f"\n{product.product_name}: {defect_count} defects found."


   elif intent_name == 'GoodProduct':
        products = Product.objects.all()
        response_text = "Here products which have no defects: "

        for product in products:
            number_defects = product.defects.count()
            if number_defects == 0:
                response_text += f"\n  {product.product_name}"
           
   elif intent_name == 'GetReparationByDate':
    #  date_str = parameters.get('date')
     # formats = ['%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y']
     
      repairs = Reperation.objects.filter(date_reperation=date_obj)
      repair_count = repairs.count()
      if repair_count > 0:
          user_names = ', '.join([repair.user.username for repair in repairs])
          defect_names = ', '.join([repair.defect_id.defect_name for repair in repairs])
          response_text = f"{repair_count} repairs were made on {date_obj}. The repair man were made by: {user_names}. The defects that were repaired are: {defect_names}."
      else:
             response_text = f"No repairs have been made on {date_obj}."
   
   elif intent_name == 'GetControlByDate':
       #date_str = parameters.get('date')
       controls = Control.objects.filter(date_control=date_obj)
       control_count = controls.count()      
       if control_count > 0:
           user_names = ', '.join([control.user.username for control in controls])
           #defect_names = ', '.join([control.defect_id.defect_name for control in controls])
           response_text = f"{control_count} controls were affected on {date_obj.strftime('%Y-%m-%d')}. The controls were made by: {user_names}."
           #The defects that were controlled are: {defect_names}."
       else:
           response_text = f"No controls have been made on {date_obj}."


   elif intent_name == 'Reparation':
     # Use Django ORM to fetch data from the database
        repairs = Reperation.objects.filter(date_reperation=datetime.today())
        repair_count = repairs.count()
        if repair_count > 0:
            user_names = ', '.join([repair.user.username for repair in repairs])
            defect_names = ', '.join([repair.defect_id.defect_name for repair in repairs])
            response_text = f"{repair_count} repairs were made today. The repair man were made by: {user_names}. The defects that were repaired are: {defect_names}."
        else:
            response_text = f"No repairs were made today."
  
   elif intent_name == 'Box':
        products = Product.objects.all()
        
        # Create a dictionary to store the box names for each product
        product_box_dict = {}
        
        # Loop through the products and retrieve their corresponding box names
        for product in products:
            box_name = product.box_id.box_name
            product_name = product.product_name
            product_box_dict[product_name] = box_name
            
        # Generate a response text using the product_box_dict
        response_text = ""
        for product_name, box_name in product_box_dict.items():
            response_text += f"{product_name} is in the {box_name}. "


   else:
       response_text = "Sorry, I didn't get that can you rephrase?"


   # Return the response to Dialogflow
   response = {
       'fulfillmentText': response_text
   }
   return JsonResponse(response)