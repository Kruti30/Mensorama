from django.db import models


# Create your models here.

class Employee(models.Model):
    eid = models.AutoField(primary_key=True)
    ename = models.CharField(max_length=100)
    eemail = models.EmailField(unique=True)
    econtact = models.CharField(max_length=15)
    password = models.CharField(max_length=15)

    class Meta:
        db_table = "employee"




class USERS(models.Model):
    u_id = models.AutoField(primary_key=True)
    u_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    dob = models.DateField()
    phone_no = models.CharField(max_length=13)
    address = models.CharField(max_length=200)
    is_admin = models.BooleanField()
    otp = models.CharField(max_length=10, null=True)
    otp_used = models.IntegerField()

    class Meta:
        db_table = "users"


class CATEGORY(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=100)
    cat_description = models.CharField(max_length=500)

    class Meta:
        db_table = "category"


class SUBCATEGORY(models.Model):
    scat_id = models.AutoField(primary_key=True)
    cat_id = models.ForeignKey(CATEGORY, on_delete=models.CASCADE)
    scat_name = models.CharField(max_length=30)
    scat_description = models.CharField(max_length=500)

    class Meta:
        db_table = "subcategory"


class BRAND(models.Model):
    brd_id = models.AutoField(primary_key=True)
    brd_name = models.CharField(max_length=100)
    brd_description = models.CharField(max_length=1000)

    class Meta:
        db_table = "brand"


class PRODUCT(models.Model):
    pd_id = models.AutoField(primary_key=True)
    pd_name = models.CharField(max_length=100)
    pd_img = models.CharField(max_length=100)
    pd_img1 = models.CharField(max_length=100,null=True)
    pd_img2 = models.CharField(max_length=100,null=True)
    pd_img3 = models.CharField(max_length=100,null=True)
    pd_img4 = models.CharField(max_length=100,null=True)
    pd_description = models.CharField(max_length=1000)

    scat_id = models.ForeignKey(SUBCATEGORY, on_delete=models.CASCADE)
    brd_id = models.ForeignKey(BRAND, on_delete=models.CASCADE)
    pd_price = models.FloatField(max_length=7)
    pd_qty = models.CharField(max_length=10)


    class Meta:
        db_table = "product"


class CART(models.Model):
    cart_id = models.AutoField(primary_key=True)
    u_id = models.ForeignKey(USERS, on_delete=models.PROTECT)
    pd_id = models.ForeignKey(PRODUCT, on_delete=models.PROTECT)
    pd_qty = models.IntegerField(null=False)
    amount = models.IntegerField(null=False)
    added_date = models.DateField(null=False)

    class Meta:
        db_table = "cart"


class ORDER(models.Model):
    ord_id = models.AutoField(primary_key=True)
    u_id = models.ForeignKey(USERS, on_delete=models.CASCADE)
    ord_date = models.DateField()
    ord_status = models.IntegerField()
    add_id = models.CharField(max_length=500)
    total = models.CharField(max_length=10)
    payment_status = models.IntegerField()

    class Meta:
        db_table = "order"


class ORDER_ITEM(models.Model):
    ord_item_id = models.AutoField(primary_key=True)
    ord_id = models.ForeignKey(ORDER, on_delete=models.CASCADE)

    pd_id = models.ForeignKey(PRODUCT, on_delete=models.CASCADE)
    price = models.CharField(max_length=10)
    quantity = models.CharField(max_length=500)
    oi_amt = models.CharField(max_length=100)


    class Meta:
        db_table = "order_item"

class FEEDBACK(models.Model):
    feed_id = models.AutoField(primary_key=True)
    u_id = models.ForeignKey(USERS, on_delete=models.CASCADE)
    pd_id = models.ForeignKey(PRODUCT, on_delete=models.CASCADE)
    feed_description = models.CharField(max_length=1000)
    feed_date = models.DateField()

    class Meta:
        db_table = "feedback"


class IMAGE(models.Model):
    img_id = models.AutoField(primary_key=True)
    pd_id = models.ForeignKey(PRODUCT, on_delete=models.CASCADE)
    image = models.CharField(max_length=100)

    class Meta:
        db_table = "image"


class ADDRESSES(models.Model):
    add_id = models.AutoField(primary_key=True)
    u_id = models.ForeignKey(USERS, on_delete=models.CASCADE)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    pincode = models.CharField(max_length=7)
    address = models.CharField(max_length=50)

    class Meta:
        db_table = "address"


class WISHLISTS(models.Model):
    w_id = models.AutoField(primary_key=True)
    pd_id = models.ForeignKey(PRODUCT, on_delete=models.CASCADE)
    u_id = models.ForeignKey(USERS, on_delete=models.CASCADE)
    w_date = models.DateField(max_length=10, null=False)

    class Meta:
        db_table = "wishlists"

class CONTACT(models.Model):
    contact_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=40)
    user_email = models.CharField(max_length=35)
    message = models.CharField(max_length=1000)

    class Meta:
        db_table = "contact"
