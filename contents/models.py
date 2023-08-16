from django.db import models
from django.utils.html import mark_safe 
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

#----------------Brand-------------------------
class Brand(models.Model):
    title=models.CharField(max_length=255)
    images=models.ImageField(upload_to='brand_image/')

    class Meta:
        verbose_name_plural='3) Brands'

    def image_tag(self):
        return mark_safe('<img src="%s" width=auto height=50px />'%(self.images.url))

    def __str__(self):
        return self.title

class Color(models.Model):
    title=models.CharField(max_length=255)
    color_code=models.CharField(max_length=10)

    class Meta:
        verbose_name_plural='4) Colors'

    def color_bg(self):
        return mark_safe('<div style="width:50px; height:10px; background-color:%s;"/>'%(self.color_code))

    def __str__(self):
        return self.title


#------------Smartphone-------------------------
class Smartphone_Storage(models.Model):
    title=models.CharField(max_length=255)

    class Meta:
        verbose_name_plural='7) Smartphone Storage'

    def __str__(self):
        return self.title
    
class Smartphone_RAM(models.Model):
    title=models.CharField(max_length=255)
    type=models.CharField(max_length=255,null=True,blank=True)

    class Meta:
        verbose_name_plural='6) Smartphone RAM'

    def __str__(self):
        return self.title + ' | ' + str(self.type)
   
    
class Smartphone(models.Model):
    title=models.CharField(max_length=255)
    images=models.ImageField(upload_to='smartphone_image/')
    specification=RichTextField(blank=True,null=True)
    model_name=models.CharField(max_length=255)
    screen_size=models.CharField(max_length=255)
    storage=models.ForeignKey(Smartphone_Storage,on_delete=models.CASCADE)
    ram=models.ForeignKey(Smartphone_RAM,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    brand= models.ForeignKey(Brand, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='5) Smartphones'

    def __str__(self):
        return str(self.id) +  ' | '  + self.model_name + ' | '  + str(self.ram) + ' | '  + str(self.storage)  + ' | '  + str(self.color)
#----------------------Smartphone----------------------------    



#----------------------Smartwatch-------------------------------

class Smartwatch(models.Model):
    title=models.CharField(max_length=255)
    images=models.ImageField(upload_to='smartwatch_image/')
    specification=models.TextField()
    model_name=models.CharField(max_length=255)
    screen_size=models.CharField(max_length=255)
    band_material=models.CharField(max_length=255)
    style=models.CharField(max_length=255)
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    brand= models.ForeignKey(Brand, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='9) Smartwatches'

    def __str__(self):
        return str(self.id) +  ' | '  + self.model_name + ' | '  + str(self.brand.title) + ' | '   + str(self.color)







#---------------------Category-------------------------------
class Category(models.Model):
    title=models.CharField(max_length=255)
    images=models.ImageField(upload_to= 'category_image/')

    class Meta:
        verbose_name_plural='2) Categories'

    def image_tag(self):
        return mark_safe('<img src="%s" width=auto height=100px />'%(self.images.url))
    
    def __str__(self):
        return self.title
#-------------------------Category---------------------------



#-------------------------Product-----------------------------
class Product(models.Model):
    title=models.CharField(max_length=255)
    images=models.ImageField(upload_to='products_image/')
    smartphone=models.ForeignKey(Smartphone,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    status=models.BooleanField(default=True)
    is_featured=models.BooleanField(default=False)

    class Meta:
        verbose_name_plural='1) Products'
    
    def __str__(self):
        return self.title
    


#------------------------Product Attribute----------------------------

class ProductAttribute(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    smartphone_storage=models.ForeignKey(Smartphone_Storage,on_delete=models.CASCADE)
    smartphone_ram=models.ForeignKey(Smartphone_RAM,on_delete=models.CASCADE)
    smartphone=models.ForeignKey(Smartphone,on_delete=models.CASCADE)
    price=models.PositiveIntegerField()

    class Meta:
        verbose_name_plural='8) Product Attribute'
    
    def __str__(self):
        return str(self.id) +  ' | '  +  self.product.title + ' | ' +  str(self.smartphone_ram) + ' | ' +  str(self.price)
 

#-----------------------Cart Order-----------------------------------------

select_process=(
    ('process','In Process'),
    ('shipped','Shipped'),
    ('delivered','Delivered')


)
class CartOrder(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    total_amt=models.FloatField()
    paid_status=models.BooleanField(default=False)
    order_date=models.DateTimeField(auto_now_add=True)
    order_status=models.CharField(choices=select_process,default='In Process',max_length=150)
    
    class Meta:
        verbose_name_plural='Cart Orders'
    

#-------------------------Order Items---------------------------------------

class CartOrderItems(models.Model):
    order=models.ForeignKey(CartOrder,on_delete=models.CASCADE)
    invoice_no=models.CharField(max_length=100)
    item=models.CharField(max_length=100)
    image=models.CharField(max_length=100)
    qty=models.IntegerField()
    price=models.FloatField()
    total=models.FloatField()

    class Meta:
        verbose_name_plural='Cart Items (details)'

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width=auto height=100px />'%(self.image))
    
#------------------------Product Review-------------------------------------
RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    review=models.TextField()
    review_rating=models.CharField(choices=RATING,max_length=100)

    def get_review_rating(self):
        return self.review_rating
    

class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)

# Address Book
class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    contact=models.CharField(max_length=10,null=True)
    address=models.TextField()
    address_status=models.BooleanField(default=False)

