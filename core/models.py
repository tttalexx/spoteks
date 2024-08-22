from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    user_sname = models.CharField(max_length=100)
    user_tel = models.CharField(max_length=20)
    user_email = models.EmailField(max_length=100, unique=True)
    user_role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user_name} {self.user_sname}"

class Seller(models.Model):
    seller_id = models.AutoField(primary_key=True)
    seller_name = models.CharField(max_length=100)
    seller_edrpou = models.CharField(max_length=10)
    seller_address = models.CharField(max_length=200, blank=True)
    seller_address_mail = models.CharField(max_length=200, blank=True)
    seller_req = models.TextField(blank=True)

    def __str__(self):
        return self.seller_name

class Buyer(models.Model):
    buyer_id = models.AutoField(primary_key=True)
    buyer_name = models.CharField(max_length=100)
    buyer_edrpou = models.CharField(max_length=10)
    buyer_address = models.CharField(max_length=200, blank=True)
    buyer_address_mail = models.CharField(max_length=200, blank=True)
    buyer_req = models.TextField(blank=True)

    def __str__(self):
        return self.buyer_name

class CultureName(models.Model):
    culture_name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.culture_name

class CultureActualPrice(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    culture_name = models.ForeignKey(CultureName, on_delete=models.CASCADE)
    culture_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.culture_name} - {self.culture_price}"

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True)
    bd_culture_name = models.ForeignKey(CultureName, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    dterms = models.CharField(max_length=100, blank=True)
    quality = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_auto_dterms = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_train_dterms = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_dterms = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=50, blank=True)
    load_region = models.CharField(max_length=100, blank=True)
    load_place = models.CharField(max_length=100, blank=True)
    unload_region = models.CharField(max_length=100, blank=True)
    unload_place = models.CharField(max_length=100, blank=True)
    comment_user = models.TextField(blank=True)
    comment_spoteks = models.TextField(blank=True)
    sb = models.BooleanField(default=False)
    docks = models.BooleanField(default=False)
    dog = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.user}"
