# forms.py
from django import forms
from .models import Product,ProductCategory, Caracterstic, Brand, Control, Defect, DefectType,CheckControl, Box, DefectImage, ReferenceProduct
from django.utils.translation import gettext_lazy as _
from django.forms import ClearableFileInput, ModelChoiceField, formset_factory
from apps.users.models import CustomUser


class ControlForm(forms.ModelForm):
     class Meta:
        model = Control
        fields = ['date_control','details_control', 'time_control', 'state_control', 'serial_code', 'user']
        labels = {
        'date_control': _('Control Date operation'),
        'details_control': _('Control details operation '),
        'time_control': _('Control time operation'),
        'state_control': _('Control state operation'),
        'serial_code': _('Product name'),
        'user': _('Controller name'),
        }   
        
class CategorieForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            #import ipdb;
            #ipdb.set_trace()
            team_slug =  kwargs.pop('data', {}).get('team_slug')
            super(CategorieForm,self).__init__(*args, **kwargs) 
            self.fields['parent']  = forms.ModelChoiceField(ProductCategory.objects.all().filter(team__name=team_slug),required=False)
            self.fields['parent'].label = 'Category name'

    class Meta:
        model = ProductCategory
        fields = ['category_name','parent']
        labels = {
        'parent': _('Category name'),        
        'category_name': _(' Sub Category name'),     
        }

class BrandForm(forms.ModelForm):
     class Meta:
        model = Brand
        fields = ['brand_name']
              
class caractersticForm(forms.ModelForm):
     class Meta:
        model = Caracterstic
        fields = ['caracterstic_label','caracterstic_value'] 
        labels = {
        'caracterstic_label': _('Tag name'),
        'caracterstic_value': _('Tag value: (🅘 this field could support multi value separated by space) '),
        }    
class referenceForm(forms.ModelForm):
        class Meta:
             model = ReferenceProduct
             fields = ['reference_code_label','reference_code_value'] 
             labels = {
             'caracterstic_label': _('Reference name'),
             'reference_code_value': _('Reference value: (🅘 this field could support multi value separated by space) '),
             } 

class ProductForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
                #import ipdb;
                #ipdb.set_trace()
                team_slug =  kwargs.pop('data', {}).get('team_slug')
                super(ProductForm,self).__init__(*args, **kwargs) 
                self.fields['box_id']  = forms.ModelChoiceField(Box.objects.all().filter(team__name=team_slug))
                self.fields['brand_id']  = forms.ModelChoiceField(Brand.objects.all().filter(team__name=team_slug))
                self.fields['category_id']  = forms.ModelChoiceField(ProductCategory.objects.all().filter(team__name=team_slug))

        class Meta:
                model =  Product
                fields = ['type_code','serial_code','format_of_code','product_name','category_id', 'brand_id', 'box_id']
                labels = {
                     'category_id'         : _('Category name'),
                     'brand_id'            : _('Brand name of Product'),
                     'box_id'              : _('Box name'),
                     'format_of_code'      : _('Format Of Product Reference'),
                     'serial_code'         : _('Reference Code Product ')

                     }


class DefectForm(forms.ModelForm):

        def __init__(self, *args, **kwargs):
   
                team_slug =  kwargs.pop('data', {}).get('team_slug')
                super(DefectForm,self).__init__(*args, **kwargs) 
                self.fields['products']  = forms.ModelMultipleChoiceField(queryset=Product.objects.all().filter(team__name=team_slug),
                     widget=forms.CheckboxSelectMultiple)
                self.fields['defect_type']  = forms.ModelChoiceField(DefectType.objects.all().filter(team__name=team_slug))
        class Meta:
                model = Defect
                fields = ['defect_name','defect_type','defect_type_value','pattern','description','products'] 
                labels = {
                'products': _('products Name'),
                }   

        
class DefectTypeForm(forms.ModelForm):
        
        class Meta:
                model = DefectType
                fields = ['defect_type_name','defect_type'] 
                labels = {'defect_type': _('Type of Defect'),
                          'defect_type_name': _('Label of Defect Type'),
                }    

class BoxForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = ['box_name','qte','parent']
        labels = {
        'box_name': _('Sub Box name'),
        'qte': _('Quantity'),
        'parent': _('Box name '),
        }  

class CheckControlForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
                #import ipdb;
                #ipdb.set_trace()
                team_slug =  kwargs.pop('data', {}).get('team_slug')
                super(CheckControlForm,self).__init__(*args, **kwargs) 
                self.fields['defect_id']  = forms.ModelMultipleChoiceField(queryset=Defect.objects.all().filter(team__name=team_slug),widget=forms.CheckboxSelectMultiple)
                #self.fields['user']  = forms.ModelChoiceField(CustomUser.objects.all().filter(team__name=team_slug),widget=forms.CheckboxSelectMultiple)
                #self.fields['category'] = forms.ModelMultipleChoiceField(queryset=ProductCategory.objects.all())

        class Meta:
                model = CheckControl
                fields = ['defect_id','threshold', 'post','box_id', 'user']
                labels = {
                'defect_id': _('Type of Defect '),
                'threshold': _('Threshold'),
                'box_id': _('Box name'),
                'user': _('Controller name'),
                }  

class UserForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
                #import ipdb;
                #ipdb.set_trace()
                team_slug =  kwargs.pop('data', {}).get('team_slug')
                super(UserForm,self).__init__(*args, **kwargs) 
                self.fields['email']  = forms.ModelChoiceField(queryset=CustomUser.objects.all())
                #self.fields['user']  = forms.ModelChoiceField(CustomUser.objects.all().filter(team__name=team_slug),widget=forms.CheckboxSelectMultiple)
        class Meta:
                model = CustomUser
                fields = ['email','code_user','poste','products'] 
                labels = {'code_user': _('Reference of User'),
                          'email': _('Email of User'),
                          'poste': _('Post of User'),
                          'products':_('Product'),
                }  