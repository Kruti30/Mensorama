from parsley.decorators import parsleyfy
from django import forms
from igadmin.models import Employee, USERS, CATEGORY, SUBCATEGORY, BRAND, PRODUCT, ORDER, ORDER_ITEM, FEEDBACK, IMAGE, \
    ADDRESSES, CART, CONTACT


class EmpForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["ename", "eemail", "econtact"]

@parsleyfy
class userForm(forms.ModelForm):
    class Meta:
        model = USERS
        fields = ["u_id", "u_name", "email", "password", "dob", "phone_no", "address", "is_admin"]

class categoryForm(forms.ModelForm):
    class Meta:
        model = CATEGORY
        fields = ["cat_id", "cat_name", "cat_description"]

class subcategoryForm(forms.ModelForm):
    class Meta:
        model = SUBCATEGORY
        fields = ["cat_id", "scat_name", "scat_description"]

class brandForm(forms.ModelForm):
    class Meta:
        model = BRAND
        fields = ["brd_id",  "brd_name", "brd_description"]

class productForm(forms.ModelForm):
    class Meta:
        model = PRODUCT
        fields = ["pd_name", "pd_description", "scat_id", "brd_id", "pd_price", "pd_qty","pd_img"]


class orderForm(forms.ModelForm):
    class Meta:
        model = ORDER
        fields = ["ord_id", "u_id", "ord_date", "ord_status", "add_id", "total", "payment_status"]


class order_itemForm(forms.ModelForm):
    class Meta:
        model = ORDER_ITEM
        fields = ["ord_item_id", "ord_id", "pd_id", "price", "quantity", "oi_amt"]


class feedbackForm(forms.ModelForm):
    class Meta:
        model = FEEDBACK
        fields = ["feed_id", "u_id", "pd_id", "feed_description", "feed_date"]


class imageForm(forms.ModelForm):
    class Meta:
        model = IMAGE
        fields = ["img_id", "pd_id", "image"]


class addressForm(forms.ModelForm):
    class Meta:
        model = ADDRESSES
        fields = ["add_id", "u_id", "state", "city", "pincode"]

class cartForm(forms.ModelForm):
    class Meta:
        model = CART
        fields = ["cart_id", "u_id", "pd_id", "pd_qty", "amount", "added_date"]

class contactForm(forms.ModelForm):
    class Meta:
        model = CONTACT
        fields = [ "user_name", "user_email", "message"]
