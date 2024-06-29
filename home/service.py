from cart.models import CartItem, CartUser
from products.models import ProductSize
from order.models import Order, OrderItem


class CartService:
    @staticmethod
    def calculate_total(cart_user):
        total = 0
        cart_items = CartItem.objects.filter(cart=cart_user)
        for cart_item in cart_items:
            total += cart_item.product.product.price * cart_item.quantity
        cart_user.total = total
        cart_user.save()
    
    @staticmethod
    def add_product(cart_user ,product_id):
        product = ProductSize.objects.get(id=product_id)
        cart_user.products.add(product)
        cart_item, created= CartItem.objects.get_or_create(cart=cart_user, product=product)
        if not created:
            cart_item.quantity +=1
            cart_item.save()
        CartService.calculate_total(cart_user)
       

    @staticmethod
    def remove_product(cart_user, product_id):
        product = ProductSize.objects.get(id=product_id)
        try: 
            cart_item = CartItem.objects.get(cart=cart_user, product=product)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
                cart_user.products.remove(product)
        except CartItem.DoesNotExist:
            pass
        CartService.calculate_total(cart_user)
        
        
    @staticmethod
    def buy(cart_user):
        order = Order.objects.create(user=cart_user.user, total=cart_user.total)
        for cart_item in CartItem.objects.filter(cart=cart_user):
            if cart_item.quantity <= cart_item.product.quantity:
                OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
                cart_item.product.quantity = cart_item.product.quantity - cart_item.quantity
                cart_item.product.save()
                cart_item.delete()
            else:
                message = f"We only have {cart_item.product.quantity} units available for {cart_item.product.product.name}, size: {cart_item.product.size} and you have {cart_item.quantity} on the cart"
                return message
        
        cart_user.products.clear()
        cart_user.total = 0
        cart_user.save()
        return order
    
class UserService:
    def create_cart_user(user):
        CartUser.objects.create(user=user)