from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from cart.models import CartUser
from products.models import Product, Review
from users.models import User
from order.models import Order
from .service import CartService, UserService

class HomeView(View):
    template_name = 'home/index.html'
    
    def get(self, request):
        products = Product.objects.all()[:8]
    
    
        return render(request, self.template_name, {
            'products':products,
        })


class UserRegisterView(View):
    template_name = 'home/register.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        if password1 != password2:
            return render(request, self.template_name, {'error': "Passwords don't match"})
        try:
            user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
            user.save()
            UserService.create_cart_user(user)
            login(request, user)
            return redirect('home:index')
        except Exception as e:
            return render(request, self.template_name, {'error':str(e)})

            

class UserLoginView(View):
    template_name = 'home/login.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, self.template_name, {'error': "Username and password are required"})
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home:index')
        else:
            return render(request, self.template_name, {'error': 'Invalid credentials'})


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home:index')
    
        
@method_decorator(login_required(login_url='home:login'), name='dispatch')
class CartView(View):
    template_name =  'home/cart.html'
    def get(self, request):
        user = request.user
        my_cart = CartUser.objects.get(user=user)
        products = my_cart.products.all()
        
        return render(request, self.template_name,{
            'products':products,
            'cart': my_cart,
        })
    
    def post(self, request, product_id):
        user = request.user
        my_cart = CartUser.objects.get(user=user)
        CartService.remove_product(my_cart, product_id)
        return redirect('home:cart')
    


class BuyView(View):
    template_name = 'home/order.html'

    @method_decorator(login_required(login_url='home:login'))
    def post(self, request):
        user = request.user
        my_cart = CartUser.objects.get(user=user)
        if my_cart.total == 0:
            return redirect('home:cart')
        else:
            order = CartService.buy(my_cart)
            try:
                order_items = order.item.all()
            except:
                messages.add_message(request, 50, order)
                return redirect('home:cart')
            
 

            return render(request, self.template_name,{
                'order':order,
                'items':order_items,
            })

class AllProductsView(View):
    template_name = 'home/allproducts.html'
    def get(self, request):
        products = Product.objects.all()
        return render(request, self.template_name,{
            'products':products
        })

class ProductView(View):
    template_name = 'home/product.html'
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        sizes = product.sizes.all()
        reviews = Review.objects.filter(product=product_id).order_by('-id')
        print(reviews)
        return render(request, 'home/product.html',{
            'product':product,
            'sizes':sizes,
            'reviews':reviews
        })
    
    @method_decorator(login_required(login_url='home:login'))
    def post(self, request, product_id):
        user = request.user
        size_id = request.POST.get('size') 
        my_cart = CartUser.objects.get(user=user)
        CartService.add_product(my_cart, size_id)

        
        return redirect('home:product', product_id=product_id)
    
class ReviewView(View):
    @method_decorator(login_required(login_url='home:login'))
    def post(self, request, product_id):
        user = request.user
        created_by = user
        comments = request.POST.get('comment')
        score = int(request.POST.get('score'))
        
        product = Product.objects.get(id=product_id)
        
        Review.objects.create(created_by=created_by, product=product, comments=comments, score=score)
        
        
        return redirect('home:product', product_id=product_id)
   
class ReviewDeleteView(View):
    def post(self, request, review_id):
        review = Review.objects.get(id = review_id)
        product_id = review.product.id
        review.delete()
        
        return redirect('home:product', product_id=product_id)
    
class UserView(View):
    template_name = 'home/user.html'
    
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        orders = Order.objects.filter(user=user_id)
        return render(request, self.template_name,{
            'user':user,
            'orders':orders,
        })