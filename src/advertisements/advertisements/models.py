from django.db import models



class Category(models.Model):
    title = models.CharField(max_length=255,unique=True)
    description = models.CharField(blank=True, max_length=1024)

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank = True, null=True)
    title = models.CharField(max_length=255, unique=True)
    description = models.CharField(blank=True, max_length=1024)


class Advertisement(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE, blank = True, null=True)

    author_id = models.PositiveIntegerField(blank=True,null=True)
    title = models.CharField(max_length=255)
    description = models.CharField(blank=True, max_length=1024)
    price = models.DecimalField(max_digits=6, decimal_places=2)
