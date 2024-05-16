import sys
from datetime import date

from django.contrib import messages
from django.shortcuts import render, redirect

from Mensorama import settings
from igadmin.forms import userForm, contactForm
from igadmin.models import USERS, PRODUCT, FEEDBACK, CART, ADDRESSES, ORDER, ORDER_ITEM, SUBCATEGORY, CATEGORY, \
    WISHLISTS


# Create your views here.
def c_index(request):
    if 'client_id' in request.session:

        id = request.session['client_id']
        c = CART.objects.filter(u_id_id=id)

        sum = 0
        for val in c:
            sum = sum + (val.amount * val.pd_qty)
        print("2----------", sum)
        shipping = sum + 50
        x = FEEDBACK.objects.all()
        product = PRODUCT.objects.order_by('-pd_id')
        return render(request, "client_index.html",
                      {"item": c, "total": sum, "shipping": shipping, "feedback": x, "product": product, })
    else:
        cart = Cart(request)
        total = cart.get_total_price()
        print(total)
        x = FEEDBACK.objects.all()
        product = PRODUCT.objects.order_by('-pd_id')
        return render(request, "client_index.html", {"total": total, "feedback": x, "product": product})


def profile_update(request):
    u=request.session["client_id"]
    dat = USERS.objects.get(u_id=u)
    d = dat.dob
    d11 = d.strftime('%Y-%m-%d')
    print("9999999999999999999999",d11)
    up=USERS.objects.get(u_id=u)
    form=userForm(request.POST,instance=up)
    print("++++++fff+++++++++++",form.errors)
    if form.is_valid():
        try:
            form.save()
            return redirect('/client/c_account/')
        except:
            print("------------",sys.exc_info())

    return render(request,"account.html",{'users':up,'d11':d11})

def c_shop(request):
    obj = PRODUCT.objects.all()

    if 'sub_id' in request.session:
        del request.session['sub_id']

    if 'cat_id' in request.session:
        del request.session['cat_id']
    if 'client_id' in request.session:
        id1 = request.session["client_id"]
        w = WISHLISTS.objects.filter(u_id=id1).values('pd_id')
        wlist = []
        for data in w:
            wlist.append(data['pd_id'])
    else:
        wlist=[]

    return render(request, "shop.html", {"product": obj,"wish":wlist})


def c_shop1(request, id):
    obj = PRODUCT.objects.filter(scat_id=id)
    obj1 = SUBCATEGORY.objects.all()
    request.session['sub_id'] = id


    if 'client_id' in request.session:
        id1 = request.session["client_id"]
        print("====================================",id1)

        w = WISHLISTS.objects.filter(u_id=id1).values('pd_id')
        wlist=[]
        for data in w:
            wlist.append(data['pd_id'])
            print("--------------++++++++++++++++++++-------------",wlist)
            # print("000000000000000000000000000000000", w)
    else:
        wlist=[]
    return render(request, "shop.html", {"product": obj, "subcategory": obj1,"wish":wlist})

def c_shop2(request, id):

    if 'sub_id' in request.session:
        del request.session['sub_id']

    request.session['cat_id'] = id
    s = SUBCATEGORY.objects.filter(cat_id=id).values('scat_id')
    print("++++++++++++++++++",s)
    obj = PRODUCT.objects.filter(scat_id_id__in = s)
    print("++++++++++++++++++",obj)
    if 'client_id' in request.session:
        id1 = request.session["client_id"]
        w = WISHLISTS.objects.filter(u_id=id1).values('pd_id')
        wlist=[]
        for data in w:
            wlist.append(data['pd_id'])
    else:
        wlist=[]
    return render(request, "shop.html", {"product": obj , "wish":wlist})


def c_account(request):
    if 'client_id' in request.session:
        id1 = request.session['client_id']
        users = USERS.objects.get(u_id=id1)
        order = ORDER.objects.filter(u_id_id=id1)
        address = ADDRESSES.objects.filter(u_id_id=id1)

        return render(request, "account.html", {"order": order, "address": address, "users": users})
    else:
        return redirect("/client/clientlogin/")


def order_list(request, id):
    o = ORDER.objects.get(ord_id=id)
    oi = ORDER_ITEM.objects.filter(ord_id=o)
    print("00000000000000000000000000000000000", oi)
    return render(request, "order_list.html", {"order_items": oi})


def pd_details(request, id):
    obj = PRODUCT.objects.filter(pd_id=id).first()
    x = FEEDBACK.objects.filter(pd_id=id)

    return render(request, "product_details.html", {"product": obj, "feedback": x})


def c_feedback(request):
    try:
        d = date.today()
        pid = request.POST["pd_id"]
        des = request.POST["feed_description"]
        uid = request.session["client_id"]
        f = FEEDBACK(feed_date=d, feed_description=des, pd_id_id=pid, u_id_id=uid)
        f.save()
        return redirect("/client/pd_details/%s" % pid)
    except:
        print("----------", sys.exc_info())
        return redirect("/client/clientlogin/")

def contact(request):
    if request.method == "POST":
        form=contactForm(request.POST)
        print("contact line --159",form.errors)
        if form.is_valid():
            try:
                form.save()
                return redirect('/client/contact/')
            except:
                print("else form",sys.exc_info())
    else:
        form=contactForm()
    return render(request,"contact.html",{'form':form})


def clientlogin(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        val = USERS.objects.filter(email=email, password=password,is_admin=0).count()
        print("-------------", email, "-------------", password, val)
        if val == 1:

            data = USERS.objects.filter(email=email, password=password, is_admin=0)
            for i in data:
                request.session['client_id'] = i.u_id
                request.session['client_name'] = i.u_name
                request.session['client_mail'] = i.email

            if 'cart' in request.session:
                product_ids = request.session['cart'].keys()
                print("----------", product_ids)
                products = PRODUCT.objects.filter(pd_id__in=product_ids)
                for product in product_ids:
                    val = request.session['cart'][product]
                    count = 0
                    list1 = []
                    for item in val:
                        list1.append(val[item])
                        print("++++++++++++++++++++++++++", list1[0])
                        count = count + 1
                        if count == 4:
                            cc1 = CART.objects.filter(pd_id_id=list1[0]).count()
                            print(cc1)
                            if cc1 == 0:
                                d = date.today()
                                uid = request.session['client_id']
                                c = CART(u_id_id=uid, pd_id_id=list1[0], pd_qty=int(list1[1]),
                                         amount=int(list1[1]) * float(list1[2]), added_date=d)
                                c.save()
                            else:
                                c = CART.objects.get(pd_id_id=list1[0])
                                c.pd_qty = c.pd_qty + int(list1[1])
                                c.save()

                cart = Cart(request)
                cart.clear()
            if request.POST.get("remember"):
                response = redirect("/client/c_index/")
                response.set_cookie('cookie_admin_email', request.POST["email"], 3600 * 24 * 365 * 2)
                response.set_cookie('cookie_admin_password', request.POST["password"], 3600 * 24 * 365 * 2)
                return response
            return redirect('/client/c_index/')
        else:
            messages.error(request, "Invalid user name and password")
            return redirect("/client/clientlogin/")
    else:
        if request.COOKIES.get("cookie_admin_email"):
            return render(request, "client_login.html", {'cookie_admin_email1': request.COOKIES['cookie_admin_email'],
                                                         'cookie_admin_password1': request.COOKIES[
                                                             'cookie_admin_password']})
        else:
            return render(request, "client_login.html")


from django.core.mail import send_mail
import random


def c_send_otp(request):
    otp1 = random.randint(10000, 99999)

    e = request.POST['email']

    request.session['temail'] = e

    obj = USERS.objects.filter(email=e).count()

    if obj == 1:
        val = USERS.objects.filter(email=e).update(otp=otp1, otp_used=0)

        subject = 'OTP Verification'

        message = str(otp1)

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]

        send_mail(subject, message, email_from, recipient_list)

        return render(request, 'c_set_password.html')


def client_forgot_password(request):
    return render(request, "client_forgot_password.html")


def c_set_password(request):
    if request.method == "POST":

        T_otp = request.POST['otp']
        T_pass = request.POST['password']

        T_cpass = request.POST['cpassword']

        if T_pass == T_cpass:

            e = request.session['temail']

            val = USERS.objects.filter(email=e, otp=T_otp, otp_used=0).count()

            if val == 1:

                USERS.objects.filter(email=e).update(otp_used=1, password=T_pass)

                return redirect("/client/clientlogin/")
            else:

                messages.error(request, "Invalid OTP")

                return render(request, "client_forgot_password.html")

        else:

            messages.error(request, "New password and Confirm password does not match ")
            return render(request, "c_set_password.html")

    else:
        return redirect("client/client_forgot_password/")


def c_register(request):
    if request.method == "POST":
        # form = userForm(request.POST)
        # print("-------------------", form.errors)
        # if form.is_valid():
        #     try:
        #         form.save()
        #         return redirect("/client/clientlogin/")
        #     except:
        #         print("----------------", sys.exc_info())
        fname = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        dob1 = request.POST.get('dob')
        phone_no = request.POST.get('phone_no')
        is_admin = request.POST.get('is_admin')
        address = request.POST.get('address')
        state = request.POST.get('state')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        addres = request.POST.get('address')


        user = USERS(u_name=fname, email=email, password=password, dob=dob1, phone_no=phone_no, address=address,
                     is_admin=is_admin)
        user.save()
        id = USERS.objects.latest('u_id')
        print("============================", )
        ad = ADDRESSES(u_id=id, address=addres, pincode=pincode, state=state, city=city)
        ad.save()
        return redirect("/client/clientlogin/")
    else:
       print("rt")
    return render(request, "client_register.html", )


def c_logout(request):
    try:
        del request.session['client_id']
        del request.session['client_name']
        del request.session['client_email']

    except:
        pass
    return redirect("/client/clientlogin/")


import math
from .cart import Cart


def insert_cart(request, id):
    # noinspection PyUnreachableCode
    if request.method == "POST":
        print("-----------------------inside post")
        if 'client_id' in request.session:

            try:
                u = request.session["client_id"]
                if "qty" in request.POST:
                    qty = request.POST["qty"]
                    print("55555555555555555555555555555555555555555",qty)
                else:
                    qty = 1

                if "price" in request.POST:
                    print("------ price --------", request.POST["price"])
                    p = math.ceil(float(request.POST["price"]))

                d = date.today().strftime("%Y-%m-%d")
                print("-------f------", u, qty, math.ceil(p), d)

                ccount = CART.objects.filter(pd_id=id,u_id_id=u).count()
                if ccount > 0:
                    obj = CART.objects.get(pd_id_id=id)
                    obj.pd_qty = obj.pd_qty + qty
                    obj.amount = obj.amount + (obj.pd_id.pd_price * qty)
                    obj.save()
                else:
                    print("--- Else -----")
                    C = CART(u_id_id=u, pd_id_id=id, pd_qty=qty, amount=math.ceil(p), added_date=d)
                    C.save()

            except:
                print("-----xcc--", sys.exc_info())

            return redirect('/client/c_cart')

        else:

            try:
                pd_id = id
                if "qty" in request.POST:
                    qty = request.POST["qty"]
                else:

                    qty = 1

                    d = date.today()
                    # pd_id = request.POST['product_id']

                if "product_name" in request.POST:
                    pd_name = request.POST['product_name']
                    amt = request.POST['amount']

                else:
                    data = PRODUCT.objects.get(pd_id=id)
                    pd_name = data.pd_name
                    amount = data.pd_price

                    amt = data.pd_price

                print("----", qty, "---------", amt)
                total = int(qty) * int(amt)

                cart = Cart(request)

                product = PRODUCT.objects.get(pd_id=id)
                print(product)
                cart.add(product=product, quantity=int(qty))
                print(cart)


            except:
                print("-------", sys.exc_info())

            return redirect('/client/c_cart')
    return render(request, "product_details.html")


def c_cart(request):
    if 'client_id' in request.session:
        id = request.session['client_id']
        c = CART.objects.filter(u_id_id=id)

        sum = 0
        for val in c:
            sum = sum + (val.pd_id.pd_price * val.pd_qty)
        print("2----------", sum)
        shipping = sum + 50
        return render(request, "cart.html", {"item": c, "total": int(sum), "shipping": shipping})
    else:
        cart = Cart(request)
        total = cart.get_total_price()
        print(total)
        return render(request, "cart.html", {"total": total, 'cart': cart})

def wishlist_destroy(request, id):
    if 'client_id' in request.session:
        print("----wish")
        wishlist = WISHLISTS.objects.get(w_id=id)
        print("----wishhhh")
        wishlist.delete()
        print("----wishlist")
        return redirect("/client/wishlist/")
    else:
        return redirect("/client/clientlogin/")

def cart_destroy(request, id):
    if 'client_id' in request.session:
        cart = CART.objects.get(cart_id=id)
        cart.delete()
        return redirect("/client/c_cart/")

    else:
        cart = Cart(request)
        product = PRODUCT.objects.get(pd_id=id)
        cart.remove(product)
        return redirect("/client/c_cart/")


def update_quantity(request, id):
    if 'client_id' in request.session:

        qty = request.GET.get('qty')

        val = CART.objects.get(cart_id=id)
        new_qty = val.pd_qty + int(qty)
        p = CART.objects.get(cart_id=id)
        price = new_qty * p.pd_id.pd_price

        if new_qty > 0:
            val = CART.objects.filter(cart_id=id).update(pd_qty=new_qty, amount=price)

    else:

        cart = Cart(request)

        product = PRODUCT.objects.get(pd_id=id)

        qty = request.GET.get('qty')

        CART.add(product=product, quantity=int(qty), update_quantity=False)

    return redirect("/client/cart")


def wishlist(request):
    # return render(request, "wishlist.html", )
    if 'client_id' in request.session:
        id = request.session['client_id']
        u = WISHLISTS.objects.filter(u_id_id=id)
        # wishlist = WISHLISTS.objects.get(w_id=id)
    else:
        return redirect("/client/clientlogin/")
    return render(request, "wishlist.html", {'us': u})


def ins_wish(request):
    print("00000000000000000000000000000000 inside wish list")
    if 'client_id' in request.session:
        if request.method == "POST":
            try:
                d = date.today().strftime("%Y-%m-%d")
                pid = request.POST.get("pd_id")
                print("-----------------------------", pid)
                uid = request.session['client_id']
                print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&", uid)
                f = WISHLISTS.objects.filter(pd_id_id=pid, u_id_id=uid).count()
                print("+++++++++++++++++++++++++++++++++++++", f)
                ab = int(1)
                if f == ab:
                    messages.error(request, "You Can't add! Item is already exist in wishlist")
                    return redirect('/client/wishlist/')
                else:
                    obj = WISHLISTS(w_date=d, pd_id_id=pid, u_id_id=uid)
                    obj.save()
                    return redirect('/client/wishlist/')
            except:
                print("===============", sys.exc_info())
        return render(request, "wishlist.html")
    else:
        return redirect("/client/clientlogin/")


def load_menu(request):
    print("------------ Load menu -----------------------")
    c = CATEGORY.objects.all()
    s = SUBCATEGORY.objects.all()
    return render(request, "test.html", {"category": c, "subcategory": s})

def load_cart(request):
    print("------------ Load cart -----------------------")
    if 'client_id' in request.session:
        cid = request.session['client_id']
        c1 = CART.objects.filter(u_id_id = cid).count()
    else:
        c = Cart(request)
        c1=0
        for x in c:
            c1=c1+1
        print("------------- count ---------------",c1)
    return render(request, "count.html", {"total": c1})

def c_404(request):
    return render(request, "pd_404.html", )

def update_password(request):
    # User_lemail = request.POST.get('admin_email')
    passwa = request.session['client_pass']
    User_lemail = request.session['client_mail']
    id11 = request.session['client_id']
    T_pass = request.POST['password']
    T_cpass = request.POST['cpassword']

    print("-----------------------",User_lemail,passwa,id11)

    val = USERS.objects.filter(email=User_lemail, password=passwa, u_id=id11).count()
    user = USERS.objects.get(u_id=id11)
    print("------------------------------", val)

    if T_pass == T_cpass:
        val = USERS.objects.filter(email=User_lemail).count()
        if val == 1:
            USERS.objects.filter(email=User_lemail).update(password=T_pass)
            return redirect("/client/c_index/")
        else:
            messages.error(request, "Something went Wrong")
            return render(request, "client_index.html")
    else:
        messages.error(request, "New password and Confirm password does not match ")
        return render(request, 'client_index.html', {'uid': user})

def change_address(request):
    if request.method == "POST":
        # address = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        addres = request.POST.get('address')

        #id = USERS.objects.latest('u_id')
        u_id1 = request.session['client_id']
        print("============================", )
        ad1 = ADDRESSES(u_id_id=u_id1, address=addres, pincode=pincode, city=city)
        ad1.save()
        return redirect("/client/r_checkout/")
    else:
        return render(request,"checkout.html")



from django.http import JsonResponse


# def autosuggest(request):
#     if 'term' in request.GET:
#         qs = PRODUCT.objects.filter(pd_name__istartswith=request.GET.get('term'))
#
#         names = list()
#
#         for x in qs:
#             names.append(x.pd_name)
#         return JsonResponse(names, safe=False)
#     return render(request, "client_header.html")
#
#
# def search(request):
#     if request.method == "POST":
#         name = request.POST["pd_name"]
#         prod = PRODUCT.objects.filter(pd_name=name)
#         pro = PRODUCT.objects.filter(pd_name=name).count()
#         if pro == 0:
#             return redirect('/client/404/')
#     else:
#         prod = PRODUCT.objects.all()
#     return render(request, 'shop.html', {'product': prod})
def autosuggest(request):
    if 'term' in request.GET:
        a = PRODUCT.objects.filter(pd_name__istartswith=request.GET.get('term'))

        names = list()

        for x in a:
            names.append(x.pd_name)
        return JsonResponse(names, safe=False)
    return render(request, "shop.html")



def search(request):
    if request.method == "GET":
        pd_name=request.GET.get('pd_name')
        if pd_name:
            request.session['search'] = pd_name
            obj=PRODUCT.objects.filter(pd_name__icontains=pd_name)
            return render(request, 'shop.html', {'product': obj})
        else:
            return redirect('/client/pd_404/')

def sort_product(request):
    sid = request.GET.get('sort')
    print("Ajx value -----" + sid)
    # subcat_id = request.session['s_id']
    # print("-----------session ---",request.session['s_id'])
    if sid == '1':
        print("----------- SORT PRODUCTS------" + sid)

        if 'sub_id' in request.session:
            cid = request.session['sub_id']
            results = PRODUCT.objects.filter(scat_id_id=cid).order_by("pd_price")
        elif 'cat_id' in request.session:
            id = request.session['cat_id']
            s = SUBCATEGORY.objects.filter(cat_id=id).values('scat_id')
            print("++++++++++++++++++", s)
            results = PRODUCT.objects.filter(scat_id_id__in=s).order_by("pd_price")
        elif 'search' in request.session:
            pd_name = request.session['search']
            results = PRODUCT.objects.filter(pd_name__icontains=pd_name).order_by("pd_price")
        else:
            results = PRODUCT.objects.all().order_by("pd_price")
    elif sid == '2':
        if 'sub_id' in request.session:
            cid = request.session['sub_id']
            results = PRODUCT.objects.filter(scat_id_id=cid).order_by("-pd_price")
        elif 'cat_id' in request.session:
            id = request.session['cat_id']
            s = SUBCATEGORY.objects.filter(cat_id=id).values('scat_id')
            print("++++++++++++++++++", s)
            results = PRODUCT.objects.filter(scat_id_id__in=s).order_by("-pd_price")
        elif 'search' in request.session:
            pd_name = request.session['search']
            results = PRODUCT.objects.filter(pd_name__icontains=pd_name).order_by("-pd_price")
        else:
            results = PRODUCT.objects.all().order_by("-pd_price")

    elif sid == '3':
        if 'sub_id' in request.session:
            cid = request.session['sub_id']
            results = PRODUCT.objects.filter(scat_id_id=cid).order_by("pd_name")
        elif 'cat_id' in request.session:
            id = request.session['cat_id']
            s = SUBCATEGORY.objects.filter(cat_id=id).values('scat_id')
            print("++++++++++++++++++", s)
            results = PRODUCT.objects.filter(scat_id_id__in=s).order_by("pd_name")
        elif 'search' in request.session:
            pd_name = request.session['search']
            results = PRODUCT.objects.filter(pd_name__icontains=pd_name).order_by("pd_name")
        else:
            results = PRODUCT.objects.filter().order_by('pd_name')
    elif sid == '4':
        if 'sub_id' in request.session:
            cid = request.session['sub_id']
            results = PRODUCT.objects.filter(scat_id_id=cid).order_by("-pd_name")
        elif 'cat_id' in request.session:
            id = request.session['cat_id']
            s = SUBCATEGORY.objects.filter(cat_id=id).values('scat_id')
            print("++++++++++++++++++", s)
            results = PRODUCT.objects.filter(scat_id_id__in=s).order_by("-pd_name")
        elif 'search' in request.session:
            pd_name = request.session['search']
            results = PRODUCT.objects.filter(pd_name__icontains=pd_name).order_by("-pd_name")
        else:
            results = PRODUCT.objects.filter().order_by('-pd_name')

    elif sid == '5':
        if 'sub_id' in request.session:
            cid = request.session['sub_id']
            results = PRODUCT.objects.filter(scat_id_id=cid).order_by("-pd_id")
        elif 'cat_id' in request.session:
            id = request.session['cat_id']
            s = SUBCATEGORY.objects.filter(cat_id=id).values('scat_id')
            print("++++++++++++++++++", s)
            results = PRODUCT.objects.filter(scat_id_id__in=s).order_by("-pd_id")
        elif 'search' in request.session:
            pd_name = request.session['search']
            results = PRODUCT.objects.filter(pd_name__icontains=pd_name).order_by("-pd_id")
        else:
            results = PRODUCT.objects.filter().order_by('-pd_id')

    return render(request, 'sort.html', {'p': results, 'n': results, 'i': results})


import razorpay


def ch(request):
    if 'client_id' in request.session :
        print("------- Checkout client ----------------")
        id2 = request.session['client_id']

        c= CART.objects.filter(u_id=id2).count()
        print("---------count----------",c)
        if c > 0 :
            cr = CART.objects.filter(u_id=id2)
            us = USERS.objects.get(u_id=id2)
            #address = ADDRESSES.objects.filter(add_id=id2).order_by('-add_id')
            address = ADDRESSES.objects.filter(u_id=id2).latest('add_id')

            print("+++++++++++++++++++++++++",address)
            sum = 0
            for val in cr:
                sum = sum + (val.pd_id.pd_price * val.pd_qty)
            print("-----sumcheckout-----", sum)

            return render(request, "checkout.html", {'cart': cr, 'total': sum, "users": us, "data": us, 'a': address})
        else:
            messages.error(request,"your cart is empty")
            return redirect("/client/c_cart")
    elif request.method == 'POST':
        amount = 50
        currency = 'INR'
        client = razorpay.Client(auth=("rzp_test_p6Rv2SyUgeI5cb", "iV3KBQqgpTScHL6eHpGwfneT"))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    else:
        return redirect("/client/c_logout/")



def place_order1(request):
    print("==============================================")
    if 'client_id' in request.session:
        pay = request.POST.get('payment_status')
        # amt = request.POST.get('amount')
        uid = request.session['client_id']
        print("11111111111111111111111111111111111111111111111111111111111111111111111111", uid)
        ca = CART.objects.filter(u_id_id=uid)
        print("======================", ord)
        amt = 0
        for val in ca:
            amt = amt + (int(val.pd_id.pd_price) * int(val.pd_qty))
        amt = amt + 50
        print("----------", amt)
        # ord = Order.objects.filter(user_id_id=uid)
        date1 = date.today().strftime("%Y-%m-%d")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", date1)
        o = ORDER(u_id_id=uid, total=amt, ord_date=date1, payment_status='2', ord_status=0)
        o.save()
        id = ORDER.objects.latest('ord_id')
        print("--------------------order id--", id)
        c = CART.objects.filter(u_id_id=uid)
        c1 = CART.objects.filter(u_id_id=uid).count()
        print("+++++++++++++++++++++++++++++++++++", c1)
        if c1 >= 1:
            for data in c:
                pid = data.pd_id_id
                qty = data.pd_qty
                pri = data.pd_id.pd_price
                total = int(qty) * pri
                print("0000000000000000000000000000000000", total)
                od = ORDER_ITEM(quantity=int(qty), pd_id_id=pid, ord_id_id=id.ord_id, oi_amt=total)
                od.save()
            e1 = request.session['client_mail']
            obj = USERS.objects.filter(email=e1).count()
            val = USERS.objects.get(email=e1)
            print("---------------------------------------------", val)
            if obj == 1:
                ord1 = ORDER_ITEM.objects.filter(ord_id_id=id)
                subject = 'Order Conformation'
                message = f'Dear {val.u_name} , \n\n\t Your order has been accepted and will deliver soon. Order details are as follows:'
                message += f'\n---------------------------------------------------------------------'
                message += f'\n  Product name'
                message += f'\n----------------------------------------------------------------------'
                for data in ord1:
                    print("---------------------------------", data)
                    message += f'\n {data.pd_id.pd_name}'
                message += f'\n----------------------------------------------------------------------'
                message += f'\n  Total \t\t\t {amt}'
                message += f'\n----------------------------------------------------------------------'
                message += f'\n\n Thank uou,\n Regards The PVR-Zone'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [e1, ]
                send_mail(subject, message, email_from, recipient_list)
        else:
            messages.error(request, "You don't have any product in your Cart!")
            return render(request, "checkout.html")
        c_delete = CART.objects.filter(u_id_id=uid)
        c_delete.delete()
        return redirect("/client/c_account/")
    return render(request, 'checkout.html')


def place_order_cod(request):
    print("==============================================")
    if 'client_id' in request.session:
        pay = request.POST.get('payment_status')
        # amt = request.POST.get('amount')
        uid = request.session['client_id']
        print("11111111111111111111111111111111111111111111111111111111111111111111111111", uid)
        ca = CART.objects.filter(u_id_id=uid)
        print("======================", ord)
        amt = 0
        for val in ca:
            amt = amt + (int(val.pd_id.pd_price) * int(val.pd_qty))
        amt = amt + 50
        print("----------", amt)
        # ord = Order.objects.filter(user_id_id=uid)
        date1 = date.today().strftime("%Y-%m-%d")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++", date1)
        o = ORDER(u_id_id=uid, total=amt, ord_date=date1, payment_status='1', ord_status=0)
        o.save()
        id = ORDER.objects.latest('ord_id')
        print("--------------------order id--", id)
        c = CART.objects.filter(u_id_id=uid)
        c1 = CART.objects.filter(u_id_id=uid).count()
        print("+++++++++++++++++++++++++++++++++++", c1)
        if c1 >= 1:
            for data in c:
                pid = data.pd_id_id
                qty = data.pd_qty
                pri = data.pd_id.pd_price
                total = int(qty) * pri
                print("0000000000000000000000000000000000", total)
                od = ORDER_ITEM(quantity=int(qty), pd_id_id=pid, ord_id_id=id.ord_id, oi_amt=total)
                od.save()
            e1 = request.session['client_mail']
            obj = USERS.objects.filter(email=e1).count()
            val = USERS.objects.get(email=e1)
            print("---------------------------------------------", val)
            if obj == 1:
                ord1 = ORDER_ITEM.objects.filter(ord_id_id=id)
                subject = 'Order Conformation'
                message = f'Dear {val.u_name} , \n\n\t Your order has been accepted and will deliver soon. Order details are as follows:'
                message += f'\n---------------------------------------------------------------------'
                message += f'\n  Product name'
                message += f'\n----------------------------------------------------------------------'
                for data in ord1:
                    print("---------------------------------", data)
                    message += f'\n {data.pd_id.pd_name}'
                message += f'\n----------------------------------------------------------------------'
                message += f'\n  Total \t\t\t {amt}'
                message += f'\n----------------------------------------------------------------------'
                message += f'\n\n Thank uou,\n Regards The PVR-Zone'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [e1, ]
                send_mail(subject, message, email_from, recipient_list)
        else:
            messages.error(request, "You don't have any product in your Cart!")
            return render(request, "checkout.html")
        c_delete = CART.objects.filter(u_id_id=uid)
        c_delete.delete()
        return redirect("/client/c_account/")
    return render(request, 'checkout.html')


def pay_cancel(request):
    return render(request, 'Payment_cancel.html')


def pay_success(request, id):
    # or1 = id
    # or2 = ORDER.objects.filter(order_id=or1).count()
    # print("===========================", or2)
    place_order1(request)
    return render(request, 'account.html')

def c_about(request):
    return render(request, "c_about.html")