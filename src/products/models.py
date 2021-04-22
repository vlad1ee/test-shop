from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import m2m_changed
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


class Category(MPTTModel):
    title = models.CharField(max_length=255, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, blank=True,
                            null=True, related_name='children')

    def __str__(self):
        return f'{self.title}'


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = TreeForeignKey(Category, on_delete=models.CASCADE,
                              related_name='products')

    def __str__(self):
        return f'{self.title}'


class Size(models.Model):
    size = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='sizes')

    def __str__(self):
        return f'{self.title}'


class Color(models.Model):
    color = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='colors')
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.title}'


class CartManager(models.Manager):
    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

    def get_or_new(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and not cart_obj.user:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            print(cart_obj)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
            print(request.session.keys())
            print(request.session.get('cart_id'))
        return cart_obj, new_obj


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='cart', blank=True, null=True)
    products = models.ManyToManyField(Product, related_name='carts',
                                      blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = CartManager()
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.user}'


def cart_receiver(sender, instance, action, *args, **kwargs):
    print(sender)
    print(instance)
    print(action)
    if action == 'post_add' or action == 'post_remove' or action == \
            'post_clear':
        total = 0
        for x in instance.products.all():
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()


m2m_changed.connect(
    cart_receiver,
    sender=Cart.products.through)
