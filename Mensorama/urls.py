"""Mensorama URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
zIncluding another URLconf
    1. Import the included() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path

from igadmin import views
# from django.conf.urls import url
from django.urls import include, re_path as url
from igadmin.views import HomeView, ChartData

urlpatterns = [
    url(r'home', HomeView.as_view(), name='home'),
    url(r'^api/chart/data/$', ChartData.as_view(), name='api-data'),





    path('admin/', admin.site.urls),
    path('show/', views.show),
    path('delete/<int:id>', views.destroy),
    path('insert/', views.insert_emp),
    path('select_data/<int:id>', views.select_data),
    path('update/<int:id>', views.update),
    path('index/', views.index),
    path('login/', views.login),
    path('logout/', views.logout),

    path('upload/', views.upload_images),


    path('cat_show/', views.cat_show),
    path('cat_insert/', views.cat_insert),
    path('cat_update/<int:id>', views.cat_update),
    path('cat_delete/<int:id>', views.cat_destroy),



    path('scat_show/', views.scat_show),
    path('scat_insert/', views.scat_insert),
    path('scat_update/<int:id>', views.scat_update),
    path('scat_delete/<int:id>', views.scat_destroy),

    path('contact_ad/', views.contact_ad),
    path('contact/<int:id>',views.contact),
    path('reply/<int:id>', views.reply),

    path('brd_show/', views.brd_show),
    path('brd_insert/', views.brd_insert),
    path('brd_update/<int:id>', views.brd_update),
    path('brd_delete/<int:id>', views.brd_destroy),


    path('pd_show/', views.pd_show),
    path('pd_insert/', views.pd_insert),
    path('pd_update/<int:id>', views.pd_update),
    path('pd_delete/<int:id>', views.pd_destroy),




    path('dashboard/', views.dashboard),
    path('basic_form/', views.basic_form),


    path('img_show/', views.img_show),

    path('add_show/', views.add_show),

    path('feed_show/', views.feed_show),

    path('ord_show/', views.ord_show),

    path('ord_item_show/<int:id>', views.ord_item_show),

    path('order_report1/', views.order_report1),
    path('order_report2/', views.order_report2),
    path('order_report3/', views.order_report3),
    path('dropdown_report/', views.dropdown_report),
    path('brand_report/', views.brand_report),

    path('accept_order/<int:id>', views.accept_order),
    path('reject_order/<int:id>', views.reject_order),

    path('forgot_password/', views.forgot_password),
    path('Password_update/', views.Password_update),

    path('send_otp/', views.send_otp),

    path('set_pass/', views.set_password),

    path('profile/', views.profile),
    path('table1/', views.table1),

    path('client/', include('client.c_urls'))


]