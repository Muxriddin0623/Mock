from django.db import models

# Mahsulotlar
class Product(models.Model):
    name = models.CharField(max_length=255)
    product_code = models.IntegerField(unique=True)

    def __str__(self):
        return f"{self.name} ({self.product_code})"

# Xomashyolar
class Material(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Mahsulot-Xomashyo munosabati
class ProductMaterial(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='materials')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='product_materials')
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.product.name} - {self.material.name}"

# Omborxonadagi ma'lumotlar
class Warehouse(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='warehouses')
    remainder = models.FloatField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.material.name} - {self.remainder} units"
