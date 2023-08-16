from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse   
from django.template.loader import render_to_string   
from django.db.models import Max, Min, Avg, Count
from django.db.models.functions import ExtractMonth
from django.core.paginator import Paginator
from django.core import paginator
from django.views.generic.base import RedirectView
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import SignupForm, ProductReviewForm, AddressForm, ProfileEdit, PasswordChangingForm
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
import calendar
from django.contrib.auth.views import PasswordChangeView
# Create your views here.

# def convert_url_to_hash(view_func):
#     def wrapped_view_func(request, *args, **kwargs):
#         old_url = request.path
#         new_url = old_url.replace('_', '#')
#         if new_url != old_url:
#             return RedirectView.as_view(url=new_url, permanent=True)(request, *args, **kwargs)
#         else:
#             return view_func(request, *args, **kwargs)
#     return wrapped_view_func

def home(request):
    data=Product.objects.filter(is_featured=True)
    return render(request,'home.html',{'data':data})



def category_list(request):
    data= Category.objects.all()
    return render(request,'category_list.html',{'data':data})

def brand_list(request):
    data= Brand.objects.all()
    return render(request,'brand_list.html',{'data':data})

# def get_context_data(self,*args, **kwargs):
#     brand_cat= Brand.objects.all()
#     context= super(brand_list, self).get_context_data(*args, **kwargs)
#     context["brand_cat"]= brand_cat
#     return context

def smartphone_list(request):
    data= Smartphone.objects.all()
    cats= Product.objects.distinct().values('category__title','category__id')
    brands= Smartphone.objects.distinct().values('brand__title','brand__id')
    colors= Smartphone.objects.distinct().values('color__title','color__id','color__color_code')
    return render(request,'smartphone_list.html',{'data':data,   'cats':cats,
                  'brands':brands,
                  'colors':colors,})

def smartwatch_list(request):
   data= ProductAttribute.objects.all()
   cats= Product.objects.distinct().values('category__title','category__id')
   brands= Smartphone.objects.distinct().values('brand__title','brand__id')
   colors= Smartphone.objects.distinct().values('color__title','color__id','color__color_code')
   return render(request,'smartphone_list.html',
                 {'data':data,
                  'cats':cats,
                  'brands':brands,
                  'colors':colors,
                        })
   

def product_list(request):
   data= ProductAttribute.objects.all()[:3]
   total_data=ProductAttribute.objects.count()
   cats= Product.objects.distinct().values('category__title','category__id')
   brands= Smartphone.objects.distinct().values('brand__title','brand__id')
   colors= Smartphone.objects.distinct().values('color__title','color__id','color__color_code')
   minmax_price= ProductAttribute.objects.aggregate(Min('price'),Max('price'))
   return render(request,'product_list.html',
                 {'data':data,
                  'cats':cats,
                  'brands':brands,
                  'colors':colors,
                  'minmax_price':minmax_price,
                  'total_data':total_data
                        })


def single_brand_list(request,cat):
    cat_str=str(cat)
    single_brand_list=Smartphone.objects.filter(brand=cat)
    cats= Product.objects.distinct().values('category__title','category__id')
    brands= Smartphone.objects.distinct().values('brand__title','brand__id')
    colors= Smartphone.objects.distinct().values('color__title','color__id','color__color_code')
    return render(request,'single_brand_list.html',{'cat':cat_str,'single_brand_list':single_brand_list, 'cats':cats,
                  'brands':brands,
                  'colors':colors,})


def single_product_detail(request,id):
    product=Product.objects.get(id=id)
    related_product=Product.objects.filter(smartphone__brand=product.smartphone.brand).exclude(id=id)[:2]
    colors=ProductAttribute.objects.filter(product=product).values('color__id','color__title','color__color_code').distinct()
    storages=ProductAttribute.objects.filter(product=product).values('price','color__id','smartphone_ram__id','smartphone_ram__title','smartphone_storage__title','smartphone_storage__id').distinct()
    form=ProductReviewForm()
    canAdd= True
    reviewCheck=Review.objects.filter(user=request.user,product=product).count()
    if request.user.is_authenticated:
        if reviewCheck > 0:
            canAdd= False
    #Avg rating
    avg_rating=Review.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))


    reviews=Review.objects.filter(product=product)
    return render(request,'single_product_detail.html',{'data':product,'related_product':related_product,'avg_rating':avg_rating,'colors':colors,'storages':storages,'form':form,'canAdd':canAdd,'reviews':reviews})


def search(request):
    q=request.GET['q']
    data=ProductAttribute.objects.filter(product__title__icontains=q)
    cats= Product.objects.distinct().values('category__title','category__id')
    brands= Smartphone.objects.distinct().values('brand__title','brand__id')
    colors= Smartphone.objects.distinct().values('color__title','color__id','color__color_code')
    return render(request,'search.html',{'data':data,
                                          'cats':cats,
                                          'brands':brands,
                                          'colors':colors,})

def filter_data(request):
    colors=request.GET.getlist('color[]')
    categories=request.GET.getlist('category[]')
    brands=request.GET.getlist('brand[]')
    minPrice=request.GET['minPrice']
    maxPrice=request.GET['maxPrice']
    allproducts=ProductAttribute.objects.all().distinct()
    allproducts=allproducts.filter(price__gte=minPrice)
    allproducts=allproducts.filter(price__lte=maxPrice)
    if len(colors)>0:
        allproducts=allproducts.filter(color__id__in=colors).distinct()
    if len(brands)>0:
        allproducts=allproducts.filter(smartphone__brand__id__in=brands).distinct()
    if len(categories)>0:
        allproducts=allproducts.filter(product__category__id__in=categories).distinct()
    temp= render_to_string('ajax/product_list.html',({'data':allproducts}))
    return JsonResponse({'data':temp})


def load_more_data(request):
   offset=int(request.GET['offset'])
   limit=int(request.GET['limit'])
   data= ProductAttribute.objects.all()[offset:offset+limit]
   temp= render_to_string('ajax/product_list.html',({'data':data}))
   return JsonResponse({'data':temp})

 
def add_to_cart(request):
    cart_product={}
    cart_product[str(request.GET['id'])]={
        'title':request.GET['title'],
        'image':request.GET['image'],
        'qty':request.GET['qty'],
        'price':request.GET['price'],
    }
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data=request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty']=int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata']=cart_data
        else:
            cart_data=request.session['cartdata']
            cart_data.update(cart_product)
            request.session['cartdata']=cart_data
    else:
        request.session['cartdata']=cart_product
    return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

def cart_list(request):
    total_amt=0
    for p_id,item in request.session['cartdata'].items():
        total_amt+=int(item['qty'])*float(item['price'])
    return render(request,'cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})


# Delete from cart
def delete_from_cart(request):
    p_id=str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data=request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata']=cart_data 
    total_amt=0
    for p_id,item in request.session['cartdata'].items():
        total_amt+=int(item['qty'])*float(item['price'])
    temp= render_to_string('ajax/cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
    return JsonResponse({'data':temp,'totalitems':len(request.session['cartdata'])})


#Update from cart
def update_from_cart(request):
    p_id=str(request.GET['id'])
    p_qty=request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data=request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty']=p_qty
            request.session['cartdata']=cart_data 
    total_amt=0
    for p_id,item in request.session['cartdata'].items():
        total_amt+=int(item['qty'])*float(item['price'])
    temp= render_to_string('ajax/cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
    return JsonResponse({'data':temp,'totalitems':len(request.session['cartdata'])})


#Signup

# def signup(request):
#     if request.method=='POST':
#         form=SignupForm(request.POST)
#         if form.is_valid():
#             username=form.cleaned_data.get('username')
#             pwd=form.cleaned_data.get('password1')
#             user=authenticate(username=username,password1=pwd)
#             login(request,user)
#             return redirect('home')
#     form=SignupForm   
#     return render(request,'registration/signup.html',{'form':form})

class signup(generic.CreateView):
    form_class=SignupForm
    template_name='registration/signup.html'
    success_url= reverse_lazy('login')

@csrf_exempt
def payment_done(request):
    returnData=request.POST
    return render(request, 'payment_success.html',{'data':returnData})

@csrf_exempt
def payment_cancelled(request):
    return render(request, 'payment_fail.html')


@login_required
def checkout(request):
# Process Payment
    total_amt=0
    total_AMT=0
    if 'cartdata' in request.session:
        for p_id,item in request.session['cartdata'].items():
            total_AMT+=int(item['qty'])*float(item['price'])
        # Order
        order=CartOrder.objects.create(
                user=request.user,
                total_amt=total_AMT
    )
        # End
        for p_id,item in request.session['cartdata'].items():
            total_amt+=int(item['qty'])*float(item['price'])
       # Order Items
            items=CartOrderItems.objects.create(
                order=order,
                invoice_no='INV-'+str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty'])*float(item['price'])
            )
        # Process Payment
    host=request.get_host()
    paypal_dict={
        'business':settings.PAYPAL_RECEIVER_EMAIL,
        'amount':total_amt,
        'item_name':'OrderNo-'+str(order.id),
        'invoice':'INV-'+str(order.id),
        'currency_code':'USD',
        'notify_url':'http://{}{}'.format(host,reverse('paypal-ipn')),
        'return_url':'http://{}{}'.format(host,reverse('payment_done')),
        # 'cancel_return':'http://{}{}'.format(host,reverse('payment_cancelled')),
}
    form=PayPalPaymentsForm(initial=paypal_dict)
    select_address=Address.objects.filter(user=request.user,address_status=True).first()
    return render(request,'checkout.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt,'form':form,'select_address':select_address})



# Save Review
def save_review(request,pid):
    product=Product.objects.get(pk=pid)
    user=request.user
    review_form=Review.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        review_rating=request.POST['review_rating'],
     )
    data={
         'user':user.username,
         'review_text':request.POST['review'],
         'review_rating':request.POST['review_rating'],
     }
    avg_rating=Review.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))
    return JsonResponse({'bool':True,'data':data,'avg_rating':avg_rating})


#Dashboard
def dashboard(request):
    orders=CartOrder.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(count=Count('id')).values('month','count')
    month_number=[]
    total_orders=[]
    for d in orders:
        month_number.append(calendar.month_name[d['month']])
        total_orders.append(d['count'])
    
    return render(request,'users/dashboard.html',{'month_number':month_number,'total_orders':total_orders})



#Orders
def my_orders(request):
    orders=CartOrder.objects.filter(user=request.user).order_by('-id')
    return render(request,'users/my_orders.html',{'orders':orders})

def order_items(request,id):
    order=CartOrder.objects.get(pk=id)
    orders=CartOrderItems.objects.filter(order=order).order_by('-id')
    return render(request,'users/order_items.html',{'orders':orders})



#Wishlist
def add_wishlist(request):
    pid=request.GET['product']
    product=Product.objects.get(pk=pid)
    data={}
    check_list=Wishlist.objects.filter(product=product,user=request.user).count()
    if check_list > 0:
        data={
            'bool':False
        }
    else:
        wishlist=Wishlist.objects.create(
            product=product,
            user=request.user
        )
        data={
            'bool':True
        }
    return JsonResponse(data)


def my_wishlist(request):
    wlist=Wishlist.objects.filter(user=request.user).order_by('-id')
    return render(request,'users/my_wishlist.html',{'wlist':wlist})


def my_reviews(request):
    reviews=Review.objects.filter(user=request.user).order_by('-id')
    return render(request,'users/my_reviews.html',{'reviews':reviews})


#Address
def my_address(request):
    addbook=Address.objects.filter(user=request.user).order_by('-id')
    return render(request,'users/my_address.html',{'addbook':addbook})


def add_address(request):
    msg=None
    if request.method=='POST':
         form= AddressForm(request.POST)
         if form.is_valid():
            saveForm=form.save(commit=False)
            saveForm.user=request.user
            saveForm.save()
            if 'address_status' in request.POST:
                Address.objects.update(address_status=False)
            saveForm.save()
            msg='Your Data was saved'
    form=AddressForm
    return render(request,'users/add_address.html',{'form':form,'msg':msg})

def activate_address(request):
    a_id=str(request.GET['id'])
    Address.objects.update(address_status=False)
    Address.objects.filter(id=a_id).update(address_status=True)
    return JsonResponse({'bool':True})

 

def edit_profile(request):
    msg=None
    if request.method=='POST':
         form= ProfileEdit(request.POST,instance=request.user)
         if form.is_valid():
            form.save()
            msg='Your Data was saved'
    form=ProfileEdit(instance=request.user)
    return render(request,'users/edit_profile.html',{'form':form,'msg':msg})

def update_address(request,id):
    address=Address.objects.get(pk=id)
    msg=None
    if request.method=='POST':
         form= AddressForm(request.POST,instance=address)
         if form.is_valid():
            saveForm=form.save(commit=False)
            saveForm.user=request.user
            saveForm.save()
            if 'address_status' in request.POST:
                Address.objects.update(address_status=False)
            saveForm.save()
            msg='Your Data was saved'
    form=AddressForm(instance=address)
    return render(request,'users/update_address.html',{'form':form,'msg':msg})


class PasswordEditView(PasswordChangeView):
    form_class= PasswordChangingForm
    template_name='registration/change_password.html'
    success_url= reverse_lazy('password_changed')

def PasswordChanged(request):
    return render(request,'registration/password_changed.html')


