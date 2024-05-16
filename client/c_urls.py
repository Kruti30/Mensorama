from django.urls import path

from client import c_views

urlpatterns = [
    path('c_index/', c_views.c_index),
    path('c_index/c_index/', c_views.c_index),
    path('clientlogin/', c_views.clientlogin),
    path('c_register/', c_views.c_register),
    path('c_shop1/<int:id>', c_views.c_shop1),
    path('c_shop2/<int:id>', c_views.c_shop2),
    path('c_shop/', c_views.c_shop),
    path('pd_details/<int:id>', c_views.pd_details),
    path('c_feedback/', c_views.c_feedback),
    path('c_account/', c_views.c_account),
    path('insert_cart/<int:id>',c_views.insert_cart),
    path('c_cart/', c_views.c_cart),
    path('client/c_cart/', c_views.c_cart),
    path('c_logout/', c_views.c_logout),
    path('cart_delete/<int:id>', c_views.cart_destroy),
    path('wishlist_delete/<int:id>', c_views.wishlist_destroy),
    #path('cart_update/<int:id>', c_views.cart_update),
    path('update_quantity/<int:id>', c_views.update_quantity),

    path('profile_update/',c_views.profile_update),
    path('search_product/', c_views.autosuggest, name='pro_search'),
    path('', c_views.c_index, name='index'),

    path('searchp/', c_views.search),
    path('wishlist/', c_views.wishlist),
    path('ins_wishlist/', c_views.ins_wish),
    path('order_list/<int:id>', c_views.order_list),

    path('change_address/', c_views.change_address),
    path('update_password/', c_views.update_password),


    path('client_forgot_password/', c_views.client_forgot_password),
    path('c_set_pass/', c_views.c_set_password),
    path('c_send_otp/', c_views.c_send_otp),

    path('ajax/load-products/', c_views.sort_product, name='ajax_sort_products'),


    path('order_success/<int:id>', c_views.pay_success),
    path('placeorder1/', c_views.place_order1),
    path('place_order_cod/', c_views.place_order_cod),
    path('order_cancel/', c_views.pay_cancel),
    path('r_checkout/',c_views.ch),

    path('c_404/', c_views.c_404),

    path('client_header_menu/',c_views.load_menu),
    path('client_header_cart/', c_views.load_cart),

    path('c_about/',c_views.c_about),
    path('contact/',c_views.contact),
]
