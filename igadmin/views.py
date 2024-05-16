import sys

from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect

from Mensorama import settings
from igadmin.forms import userForm, categoryForm, subcategoryForm, brandForm, productForm, imageForm, contactForm
from igadmin.function import handle_uploaded_file
from igadmin.models import USERS, CATEGORY, SUBCATEGORY, BRAND, PRODUCT, ORDER, ORDER_ITEM, FEEDBACK, IMAGE, ADDRESSES, \
    CONTACT

import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


# Create your views here.
def profile(request):
    ui = request.session['admin_id']
    data = USERS.objects.get(u_id=ui)
    d = data.dob
    d1 = d.strftime('%Y-%m-%d')
    print("9999999999999999999999",d1)
    uid = USERS.objects.get(u_id=ui)
    form = userForm(request.POST, instance=uid)
    print("-----------ssssss-------", form.errors)
    if form.is_valid():
            try:
                form.save()
                return redirect("/dashboard/")
            except:
                print("------dddd-----", sys.exc_info())
    return render(request, 'profile.html', {'uid': uid,'d1':d1})

def table1(request):

    return render(request, "exporttable.html")
def show(request):
    users = USERS.objects.all()
    return render(request, "user.html", {'users': users})


def destroy(request, id):
    users = USERS.objects.get(u_id=id)
    users.delete()
    return redirect("/show")


def insert_emp(request):
    if request.method == "POST":
        form = userForm(request.POST)
        print("----------------", form.errors)

        if form.is_valid():
            try:
                form.save()
                return redirect('/show')
            except:
                print("-----------", sys.exc_info())
    else:
        form = userForm()

    return render(request, 'insert.html', {'form': form})


def upload_images(request):
    if request.method == 'POST':
        g = imageForm(request.POST, request.FILES)
        print("----------", g.errors)

        if g.is_valid():
            try:
                handle_uploaded_file(request.FILES['g_path'])
                g.save()
                return HttpResponse("File uploaded successfully")
            except:
                print("----------", sys.exc_info())
    else:
        g = imageForm()
        return render(request, "gallery.html", {'form': g})


def select_data(request, id):
    employee = USERS.objects.get(u_id=id)
    return render(request, 'edit.html', {'users': employee})


def update(request, id):
    users = USERS.objects.get(u_id=id)
    form = userForm(request.POST, instance=users)
    if form.is_valid():
        form.save()
        return redirect("/show")
    return render(request, 'edit.html', {'users': users})







def index(request):
    users = USERS.objects.all()
    return render(request, "user.html", {'users': users})


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        val = USERS.objects.filter(email=email, password=password, is_admin=1).count()
        print("----------", email, "----------", password)
        if val == 1:
            data=USERS.objects.filter(email=email, password=password, is_admin=1)
            for i in data:
                request.session['admin_id']= i.u_id
                request.session['admin_name'] = i.u_name
                request.session['admin_email'] = i.email
                request.session['admin_pass'] = i.password
                print("***********")
            print("---------------------------psdd-----------")
            if request.POST.get("remember"):
                response = redirect("/dashboard")
                response.set_cookie("cookie_admin_email", request.POST["email"],3600*24*365*2)
                response.set_cookie("cookie_admin_password", request.POST["password"],3600*24*365*2)
                return response
            return redirect('/dashboard/')

        else:
            messages.error(request, "Invalid user name and password")
            return redirect("/login")

    else:
        if request.COOKIES.get("cookie_admin_email"):
            return render(request, "auth-login.html",{'cookie_admin_email1':request.COOKIES['cookie_admin_email'],'cookie_admin_password1':request.COOKIES['cookie_admin_password']})
        else:
            return render(request,"auth-login.html")



def logout(request):
    try:
        del request.session['admin_id']
        del request.session['admin_name']
        del request.session['admin_email']
        del request.session['admin_pass']
    except:
        pass
    return redirect("/login/")






#============================================================CATEGORY=========================================================================

def cat_show(request):
    cat_id = CATEGORY.objects.all()
    return render(request, "category.html", {'category': cat_id})


def cat_destroy(request, id):
    category = CATEGORY.objects.get(cat_id=id)
    category.delete()
    return redirect("/cat_show")



def cat_insert(request):
    if request.method == "POST":
        form = categoryForm(request.POST)
        print("----------------", form.errors)

        if form.is_valid():
            try:
                form.save()
                return redirect('/cat_show')
            except:
                print("-----------", sys.exc_info())
    else:
        form = categoryForm()

    return render(request, 'category-insert.html', {'form': form})

def cat_upload_images(request):
    if request.method == 'POST':
        g = imageForm(request.POST, request.FILES)
        print("----------", g.errors)

        if g.is_valid():
            try:
                handle_uploaded_file(request.FILES['g_path'])
                g.save()
                return HttpResponse("File uploaded successfully")
            except:
                print("----------", sys.exc_info())
    else:
        g = imageForm()
        return render(request, "gallery.html", {'cat_form': g})


def cat_select_data(request, id):
    category = CATEGORY.objects.get(cat_id=id)
    return render(request, 'category-edit.html', {'category': category})


def cat_update(request, id):
    category = CATEGORY.objects.get(cat_id=id)
    form = categoryForm(request.POST, instance=category)
    if form.is_valid():
        form.save()
        return redirect("/cat_show")
    return render(request, 'category-edit.html', {'category': category})


def cat_destroy(request, id):
    category = CATEGORY.objects.get(cat_id=id)
    category.delete()
    return redirect("/cat_show")





#==============================================SUB-CATEGORY===========================================================================================

def scat_show(request):
    scat_id = SUBCATEGORY.objects.all()
    return render(request, "subcategory.html", {'subcategory': scat_id})


def scat_destroy(request, id):
    subcategory = SUBCATEGORY.objects.get(scat_id=id)
    subcategory.delete()
    return redirect("/scat_show")


def scat_insert(request):
    if request.method == "POST":
        scat_form = subcategoryForm(request.POST)
        print("----------------", scat_form.errors)

        if scat_form.is_valid():
            try:
                scat_form.save()
                return redirect('/scat_show')
            except:
                print("-----------", sys.exc_info())
    else:
        scat_form = ()

    return render(request, 'subcategory-insert.html', {'subcategory': scat_form})


def scat_select_data(request, id):
    subcategory = SUBCATEGORY.objects.get(scat_id=id)
    return render(request, 'subcategory-edit.html', {'subcategory': subcategory})


def scat_update(request, id):
    subcategory = SUBCATEGORY.objects.get(scat_id=id)
    form = subcategoryForm(request.POST, instance=subcategory)
    if form.is_valid():
        form.save()
        return redirect("/scat_show/")
    return render(request, 'subcategory-edit.html', {'subcategory': subcategory})


def scat_upload_images(request):
    if request.method == 'POST':
        g = imageForm(request.POST, request.FILES)
        print("----------", g.errors)

        if g.is_valid():
            try:
                handle_uploaded_file(request.FILES['g_path'])
                g.save()
                return HttpResponse("File uploaded successfully")
            except:
                print("----------", sys.exc_info())
    else:
        g = imageForm()
        return render(request, "gallery.html", {'form': g})

#================================================BRAND TBALE=========================================================================================
def contact_ad(request):
    contact = CONTACT.objects.all()
    return render(request, "contact_ad.html", {'contact': contact})

def contact(request,id):
    x=CONTACT.objects.get(contact_id=id)
    print(x)
    return render(request,"reply.html",{"x":x})
def reply(request, id):
    if request.method=="POST":
        print("1")
        user_email=request.POST.get('user_email')
        print("2")
        contact = CONTACT.objects.all()
        print("3")
        name=request.POST.get('user_name')
        print("4")
        print(user_email)
        print("5")
        subject = "gutm2158@gmail.com"
        print("6")
        message = 'Dear '+request.POST.get('user_name')+ '\n\n\nwe got your mail and here is the reply\n\n\n'+' " '+request.POST.get('contactForm')+' " '
        email_form = 'gutm2158@gmail.com'
        print("7")
        recipient_list = [user_email]
        print("8")
        send_mail(subject, message, email_form,recipient_list,name)
        print("9")
        reply = CONTACT.objects.get(contact_id=id)
        print("10")


        return render(request, 'contact_ad.html', {'reply': reply,'contact': contact})

def brd_show(request):
    brand = BRAND.objects.all()
    return render(request, "brand.html", {'brand': brand})


def brd_destroy(request, id):
    brand = BRAND.objects.get(brd_id=id)
    brand.delete()
    return redirect("/brd_show")


def brd_insert(request):
    if request.method == "POST":
        form = brandForm(request.POST)
        print("----------------", form.errors)

        if form.is_valid():
            try:
                form.save()
                return redirect('/brd_show')
            except:
                print("-----------", sys.exc_info())
    else:
        form = brandForm()

    return render(request, 'brand-insert.html', {'brand': form})


def brd_upload_images(request):
    if request.method == 'POST':
        g = imageForm(request.POST, request.FILES)
        print("----------", g.errors)

        if g.is_valid():
            try:
                handle_uploaded_file(request.FILES['g_path'])
                g.save()
                return HttpResponse("File uploaded successfully")
            except:
                print("----------", sys.exc_info())
    else:
        g = imageForm()
        return render(request, "gallery.html", {'form': g})


def brd_select_data(request, id):
    brand = BRAND.objects.get(brd_id=id)
    return render(request, 'brand-edit.html', {'brand': brand})


def brd_update(request, id):
    brand = BRAND.objects.get(brd_id=id)
    form = brandForm(request.POST, instance=brand)
    if form.is_valid():
        form.save()
        return redirect("/brd_show")
    return render(request, 'brand-edit.html', {'brand': brand})


def brd_index(request):
    brand = BRAND.objects.all()
    return render(request, "brand.html", {'brand': brand})

#==================================================ORDER TABLE====================================================================================
def ord_show(request):
    order = ORDER.objects.all()
    return render(request, "order.html", {'order': order})


def order_destroy(request, id):
    order = ORDER.objects.get(ord_id=id)
    order.delete()
    return redirect("/ord_show")


def ord_index(request):
    order = ORDER.objects.all()
    return render(request, "order.html", {'order': order})


def order_report1(request):
    sql = "SELECT 1 as ord_item_id, p.pd_name as name, sum(oi_amt) as total FROM order_item i JOIN product p where p.pd_id = i.pd_id_id GROUP by pd_id_id;"
    d = ORDER_ITEM.objects.raw(sql)
    return render(request, "product_report.html", {"order": d})

def order_report3(request):
    sc = SUBCATEGORY.objects.all()
    if request.method == "POST":
        pr1 = request.POST.get('scat_id')
        print("-------------------", pr1)
        pr = PRODUCT.objects.filter(scat_id=pr1)


    else:
        pr = PRODUCT.objects.all()

    return render(request, 'report3.html', {'product': pr, 'subcategory': sc})



from django.utils.dateparse import parse_date

def order_report2(request):
    if request.method == "POST":
        s_d = request.POST.get('start_date')
        e_d = request.POST.get('end_date')
        start = parse_date(s_d)
        end = parse_date(e_d)
        ord = ORDER.objects.filter(ord_date__range=[start, end])
        #sql = "SELECT * FROM order_table o JOIN order_item i where o.ord_id = i.ord_id_id and o.ord_date >= %s and o.ord_date <= %s;"
        #ord = ORDER_ITEM.objects.raw(sql,[s_d,e_d])
    else:
        ord = ORDER.objects.all()
    return render(request, "total_report.html", {"order": ord})


def accept_order(request, id):
    o = ORDER.objects.get(ord_id=id)
    o.ord_status = '1'
    o.save()
    e = o.u_id.email
    print("--------------------------------", e)
    subject = 'Order Status'
    message = f'Dear {o.u_id.u_name} , We have accepted your order, Order will reach you soon.' \
              f'your order id is {o.ord_id}'

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [e, ]
    send_mail(subject, message, email_from, recipient_list)
    return redirect('/ord_show')


def reject_order(request, id):
    o = ORDER.objects.get(ord_id=id)
    o.ord_status = '2'
    o.save()
    if o.payment_status == 1:
        e = o.u_id.email
        print("--------------------------------", e)
        subject = 'Order Status'
        message = f'Dear {o.u_id.u_name} {o.u_id.u_name}, We have regret to inform you, your order has been rejected  due to some technical issue.'

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject, message, email_from, recipient_list)
    else:
        e = o.u_id.email
        print("--------------------------------", e)
        subject = 'Order Status'
        message = f'Dear {o.u_id.u_name} {o.u_id.u_name}, We have regret to inform you, your order has been rejected  due to some technical issue. ' \
                  f'We will refund your amount in 2/3 days '


        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        send_mail(subject, message, email_from, recipient_list)
    return redirect('/ord_show')

#=======================================================ORDER ITEM TABLE==========================================================================
def ord_item_show(request, id):
    o = ORDER.objects.get(ord_id=id)
    oi = ORDER_ITEM.objects.filter(ord_id=o)
    print("00000000000000000000000000000000000", oi)
    return render(request, "order_item.html", {"order_items": oi})


def ord_item_destroy(request, id):
    order_item = ORDER_ITEM.objects.get(ord_item_id=id)
    order_item.delete()
    return redirect("/ord_item_show")

def ord_item_index(request):
    order_item = ORDER_ITEM.objects.all()
    return render(request, "order_item.html", {'order_item': order_item})

#======================================================FEEDBACK TABLE============================================================================

def feed_show(request):
    feedback = FEEDBACK.objects.all()
    return render(request, "feedback.html", {'feedback': feedback})




def feed_index(request):
    feedback = FEEDBACK.objects.all()
    return render(request, "feedback.html", {'feedback': feedback})

def feed_upload_images(request):
    if request.method == 'POST':
        g = imageForm(request.POST, request.FILES)
        print("----------", g.errors)

        if g.is_valid():
            try:
                handle_uploaded_file(request.FILES['g_path'])
                g.save()
                return HttpResponse("File uploaded successfully")
            except:
                print("----------", sys.exc_info())
    else:
        g = imageForm()
        return render(request, "image.html", {'form': g })


#=====================================================IMAGE TABLE================================================================================


def img_show(request):
    image = IMAGE.objects.all()
    return render(request, "image.html", {'image': image})


def img_destroy(request, id):
    image = IMAGE.objects.get(img_id=id)
    image.delete()
    return redirect("/img_show")


def img_insert(request):
    if request.method == "POST":
        form = imageForm(request.POST)
        print("----------------", form.errors)

        if form.is_valid():
            try:
                form.save()
                return redirect('/img_show')
            except:
                print("-----------", sys.exc_info())
    else:
        form = imageForm()

    return render(request, 'image_insert.html', {'form': form})


def pd_upload_images(request):
    if request.method == 'POST':
        g = imageForm(request.POST, request.FILES)
        print("----------", g.errors)

        if g.is_valid():
            try:
                handle_uploaded_file(request.FILES['g_path'])
                g.save()
                return HttpResponse("File uploaded successfully")
            except:
                print("----------", sys.exc_info())
    else:
        g = imageForm()
        return render(request, "image.html", {'form': g})


def pd_select_data(request, id):
    image = IMAGE.objects.get(img_id=id)
    return render(request, 'image_edit.html', {'image': image})


def img_update(request, id):
    image = IMAGE.objects.get(img_id=id)
    form = imageForm(request.POST, instance=image)
    if form.is_valid():
        form.save()
        return redirect("/img_show")
    return render(request, 'image_edit.html', {'image': image})


def img_index(request):
    image = IMAGE.objects.all()
    return render(request, "image.html", {'image': image})

#================================================PRODUCT TBALE=========================================================================================

def pd_show(request):
    product = PRODUCT.objects.all()
    return render(request, "product.html", {'product': product})


def pd_destroy(request, id):
    product = PRODUCT.objects.get(pd_id=id)
    product.delete()
    return redirect("/pd_show")


def pd_insert(request):
    if request.method == "POST":
        form = productForm(request.POST)
        print("----------------", form.errors)

        if form.is_valid():
            try:
                form.save()
                return redirect('/pd_show')
            except:
                print("-----------", sys.exc_info())
    else:
        form = productForm()

    return render(request, 'product_insert.html', {'form': form})




def pd_upload_images(request):
    if request.method == 'POST':
        g = imageForm(request.POST, request.FILES)
        print("----------", g.errors)

        if g.is_valid():
            try:
                handle_uploaded_file(request.FILES['g_path'])
                g.save()
                return HttpResponse("File uploaded successfully")
            except:
                print("----------", sys.exc_info())
    else:
        g = imageForm()
        return render(request, "gallery.html", {'form': g})


def pd_select_data(request, id):
    employee = PRODUCT.objects.get(pd_id=id)
    return render(request, 'product_edit.html', {'product': employee})


def pd_update(request, id):
    product = PRODUCT.objects.get(pd_id=id)
    form = productForm(request.POST, instance=product)
    if form.is_valid():
        form.save()
        return redirect("/pd_show/")
    return render(request, 'product_edit.html', {'product': product})


def pd_index(request):
    product = PRODUCT.objects.all()
    return render(request, "product.html", {'product': product})

#===========================================================ADDRRESS TABLE========================================================================

def add_show(request):
    address = ADDRESSES.objects.all()
    return render(request, "address.html", {'address': address})



def add_index(request):
    address = ADDRESSES.objects.all()
    return render(request, "address.html", {'address': address})




def dashboard(request):
    o = ORDER.objects.all().count()
    u = USERS.objects.all().count()
    #p = PRODUCT.objects.all().count()
    p = ORDER_ITEM.objects.aggregate(total=Sum('oi_amt'))['total']
    pr = ORDER_ITEM.objects.aggregate(profit=Sum('oi_amt'))['profit'] * 20 / 100
    return render(request,"dashboard.html",{"users":u , "orders":o, "order_item":p,"profit":pr})

from django.contrib.auth import get_user_model
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response

#from company.models import Company



#User = get_user_model()

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard.html', {"customers": 10})


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):


        #qs = Company.objects.all()


        cursor=connection.cursor()
        cursor.execute('''SELECT  c.cat_name as name, sum(oi_amt) as total FROM order_item o JOIN product p JOIN subcategory s JOIN category c 
where o.pd_id_id = p.pd_id and p.scat_id_id = s.scat_id and s.cat_id_id = c.cat_id
GROUP by c.cat_id;''')
        qs=cursor.fetchall()



        labels = []
        default_items = []

        for item in qs:
            labels.append(item[0])
            default_items.append(item[1])

        data = {
            "labels": labels,
            "default": default_items,
        }
        return Response(data)







def basic_form(request):


    u = USERS.objects.all().count()
    return render(request,"basic_form.html",{"users":u})


from django.core.mail import send_mail
import random


def send_otp(request):

    otp1 = random.randint(10000, 99999)
    e = request.POST['email']

    request.session['temail']=e

    obj = USERS.objects.filter(email=e).count()

    if obj == 1:

        val = USERS.objects.filter(email=e).update(otp=otp1 , otp_used=0)

        subject = 'OTP Verification'
        message = str(otp1)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [e, ]

        send_mail(subject, message, email_from, recipient_list)

        return render(request, 'set_password.html')

def forgot_password(request):
    return render(request,"forgot_password.html")

def set_password(request):

    if request.method == "POST":

        T_otp = request.POST['otp']
        T_pass = request.POST['password']
        T_cpass = request.POST['cpassword']

        if T_pass == T_cpass:

            e = request.session['temail']
            val = USERS.objects.filter(email=e,otp = T_otp,otp_used = 0).count()

            if val == 1:
                USERS.objects.filter(email = e).update(otp_used = 1,password = T_pass)
                return redirect("/login")
            else:
                messages.error(request,"Invalid OTP")
                return render(request,"forgot_password.html")

        else:
            messages.error(request,"New password and Confirm password does not match ")
            return render(request,"set_password.html")

    else:
        return redirect("/forgot_password")


def Password_update(request):
    # User_lemail = request.POST.get('admin_email')
    passw = request.session['admin_pass']
    User_lemail = request.session['admin_email']
    id1 = request.session['admin_id']
    T_pass = request.POST['password']
    T_cpass = request.POST['cpassword']

    print("-----------------------",User_lemail,passw,id1)

    val = USERS.objects.filter(email=User_lemail, password=passw, u_id=id1).count()
    user = USERS.objects.get(u_id=id1)
    print("------------------------------", val)

    if T_pass == T_cpass:
        val = USERS.objects.filter(email=User_lemail).count()
        if val == 1:
            USERS.objects.filter(email=User_lemail).update(password=T_pass)
            return redirect("/profile/")
        else:
            messages.error(request, "Something went Wrong")
            return render(request, "profile.html")
    else:
        messages.error(request, "New password and Confirm password does not match ")
        return render(request, 'profile.html', {'uid': user})


def dropdown_report(request):
    s = SUBCATEGORY.objects.all()
    if request.method == "POST":
        id = request.POST.get("scat")
        pr = PRODUCT.objects.filter(scat_id=id)
    else:
        pr = PRODUCT.objects.all()
    return render(request, "dropdown_report.html",{"scat":s,"prd":pr})


def brand_report(request):
    b = BRAND.objects.all()
    if request.method == "POST":
        id = request.POST.get("brand")
        br = BRAND.objects.filter(brd_id=id)
    else:
        br = BRAND.objects.all()
    return render(request, "brand_report.html",{"brand":b,"brd":br})