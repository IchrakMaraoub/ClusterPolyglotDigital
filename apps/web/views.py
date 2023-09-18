from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from apps.qualifeed.models import Product, ProductCategory, Caracterstic, Brand, Control, Defect, DefectType, CheckControl, Box, Reperation
from apps.teams.decorators import login_and_team_required
from django.db.models import Count
import json
from django.db.models.functions import TruncDay
from django.http import JsonResponse
from django.db import models
from django.db.models import Count
from django import template
import random
from django.db.models.functions import ExtractMonth
from collections import defaultdict
from django.db.models.functions import TruncMonth
from datetime import date, timedelta
from apps.teams.models import Team, Membership
from datetime import datetime
from django.utils import timezone


def random_color():
    def r(): return random.randint(0, 255)
    return f'rgba({r()}, {r()}, {r()}, 0.2)'


def home(request):
    if request.user.is_authenticated:
        team = request.team
        if team:
            return HttpResponseRedirect(reverse('web_team:home', args=[team.slug]))
        else:
            messages.info(request, _(
                'Teams are enabled but you have no teams. '
                'Create a team below to access the rest of the dashboard.'
            ))
            return HttpResponseRedirect(reverse('teams:manage_teams'))
    else:
        return render(request, 'web/landing_page.html')


def logs_view(request):
    active_tab = 'logs'
    return render(request, 'logs.html', {'active_tab': active_tab})


@login_and_team_required
def team_home(request, team_slug):
    assert request.team.slug == team_slug
    # labelcat=[]
    # datacat = []
    defects = []
    product_names = []
    category_data = []
    defects = Defect.objects.filter(team__name=team_slug).annotate(num_products=Count('products')).values(
        'defect_name').annotate(count=Count('defect_name'))

    categories = ProductCategory.objects.filter(team__name=team_slug).annotate(
        num_products=Count('product'))
    category_data = [{'category_name': category.category_name,
                      'num_products': category.num_products} for category in categories]

    controls = Control.objects.all().filter(team__name=team_slug)
    product_names = []
    # defect_month = []
    defect_counts = []

    for defect in defects:
        # defect_month.append(defect.created_at.month)
        product_names.append(defect['defect_name'])
        defect_counts.append(defect['count'])

      # Prepare the data for the chart
    labels = product_names
    data_defect = defect_counts

    defaut = Defect.objects.all().filter(team__name=team_slug)

    controls = Control.objects.filter(team__name=team_slug).annotate(num_defects=Count('defect_id'))

    defect_counts_by_user = {}
    defect_counts_by_user_month = {}
    for check_control in controls:
        month = check_control.created_at.month
        user = check_control.user
        defect_count = check_control.num_defects
        if user.email not in defect_counts_by_user_month:
            defect_counts_by_user_month[user.email] = {}
        if month not in defect_counts_by_user_month[user.email]:
            defect_counts_by_user_month[user.email][month] = 0
        defect_counts_by_user_month[user.email][month] += defect_count
    user_email = {}
    defect_counts_by_user = {}
    for user_email, defect_counts_by_month in defect_counts_by_user_month.items():
        total_defect_count = sum(defect_counts_by_month.values())
        defect_counts_by_user[user_email] = total_defect_count

    defects_by_month = (
        Control.objects.filter(team__name=team_slug).annotate(month=TruncMonth('date_control'))
        .values('month')
        .annotate(defect_count=Count('defect_id'))
        .order_by('month')
    )
    data_control = {'labels': [], 'values': []}
    for defect in defects_by_month:
        data_control['labels'].append(defect['month'].strftime('%b %Y'))
        data_control['values'].append(defect['defect_count'])
    chart_control_data_month = json.dumps(data_control)

    defects_by_day = (
        Control.objects.filter(team__name=team_slug).annotate(day=TruncDay('date_control'))
        .values('day')
        .annotate(defect_count=Count('defect_id'))
        .order_by('day')
    )
    data_control = {'labels': [], 'values': []}
    for defect in defects_by_day:
        data_control['labels'].append(defect['day'].strftime('%b %d, %Y'))
        data_control['values'].append(defect['defect_count'])
    chart_control_data_day = json.dumps(data_control)

    product_count = Product.objects.filter(team__name=team_slug).count()

    control_count = Control.objects.filter(team__name=team_slug).count()

    reperation_count = Reperation.objects.filter(team__name=team_slug).count()
    defect_count = Defect.objects.filter(team__name=team_slug).count()
    # Get the count of Reparation objects per month

    reparations_by_month = (
        Reperation.objects.filter(team__name=team_slug).annotate(month=TruncMonth('date_reperation'))
        .values('month')
        .annotate(reparation_count=Count('id'))
        .order_by('month')
    )
    # Prepare the data for the chart
    data_repair = {'labels': [], 'values': []}
    for reparation in reparations_by_month:
        data_repair['labels'].append(reparation['month'].strftime('%b %Y'))
        data_repair['values'].append(reparation['reparation_count'])
    chart_repair_data = json.dumps(data_repair)

    post = request.GET.get('post')
    if post:
        datacheck = Control.objects.filter(user__poste=post, team__name=team_slug)\
            .annotate(month=TruncMonth('created_at'))\
            .values('month')\
            .annotate(count=Count('id'))\
            .order_by('month')
    else:
        datacheck = []


    created_at = request.GET.get('created_at')
    if created_at:
        controls = Control.objects.filter(created_at__month=created_at.month,
                                          created_at__year=created_at.year, team__name=team_slug)
    else:
        controls = Control.objects.all().filter(team__name=team_slug)
    return render(request, 'web/app_home.html', context={
        'defect_counts_by_user': defect_counts_by_user,
        'datacheck': datacheck,
        'user_email': user_email,
        'reparations_by_month': reparations_by_month,
        'chart_repair_data': chart_repair_data,
        'chart_control_data_month': chart_control_data_month,
        'chart_control_data_day': chart_control_data_day,
        #  'labelsmonth':labelsmonth,
        # 'defect_counts_by_month':defect_counts_by_month,
        'defaut': defaut,
        'user': request.user,  # pass the current user to the context
        'categories': categories,
        'defects': defects,
        'product_names': product_names,
        'defect_counts': defect_counts,
        'controls': controls,
        'category_data': category_data,
        'labels': labels,
        'data_defect': data_defect,
        'team': request.team,
        'active_tab': 'dashboard',
        'page_title': _('{team} Dashboard').format(team=request.team),
        'product_count': product_count,
        'control_count': control_count,
        'reperation_count': reperation_count,
        'defect_count': defect_count,

    })


@login_and_team_required
def category_list(request, team_slug):
    assert request.team.slug == team_slug
    # import ipdb;
    # ipdb.set_trace()
    categories = ProductCategory.objects.annotate(
        num_products=Count('product'))
    for category in categories:
        print(f'{category.name}: {category.num_products}')
    context = {'categories': categories}
    return render(request, 'web/app_home.html', context)


def simulate_error(request):
    raise Exception('This is a simulated error.')
