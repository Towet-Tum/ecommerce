from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='customer/avatar', null=True, blank=True)
    def __str__(self):
	    return self.user.username

class Product(models.Model):
	make = models.CharField(max_length=100)
	model = models.CharField(max_length=100)
	image = models.ImageField(upload_to='media/product')
	year = models.PositiveIntegerField()
	maintance = models.CharField(max_length=50, null=True, blank=True)
	fuel_consumption = models.CharField(max_length=100, null=True, blank=True)
	mileage = models.DecimalField(max_digits=10, decimal_places=2)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	condition = models.CharField(max_length=50)
	vin = models.CharField(max_length=100)
	description = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	digital = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.make}  {self.model}"

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url
class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    feature_name = models.CharField(max_length=100)
    feature_value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.vehicle} - {self.feature_name}: {self.feature_value}"
    
class ProductAlbum(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to='album')
    image_view = models.CharField(blank=True, max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.make} - Image {self.id}"
    
class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.product.make} - {self.variation_name}"

class ProductInventory(models.Model):
    variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.variation} - Quantity: {self.quantity}"

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address
	
class Contact(models.Model):
	full_name = models.CharField(max_length=200)
	email = models.EmailField()
	subject = models.CharField(max_length=300)
	message = models.TextField()
	def __str__(self):
		return self.name
	
class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.vehicle} - {self.rating}/5"
