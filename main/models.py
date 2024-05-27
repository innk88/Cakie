from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Create your models here.


class Person(User):
    address = models.CharField("Адрес", max_length=100)
    number = models.CharField("Номер телефона", max_length=20)

    class Meta:
        verbose_name = "Сlient"
        verbose_name_plural = "Clients"


class Chief(Person):
    logo = models.ImageField("Логотип", upload_to='chiefs/', blank=True, null=True)

    class Meta:
        verbose_name = "Chief"
        verbose_name_plural = "Chiefs"
        permissions = [
            ("can_add_cake", "Can add cake"),
        ]


class Cake(models.Model):
    name = models.CharField("Наименование", max_length=100)
    filling = models.CharField("Начинка", max_length=100)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    weight = models.DecimalField("Вес", max_digits=10, decimal_places=2)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to='static/main/media/cakes/', blank=True, null=True)
    tags = models.ManyToManyField('Tag', verbose_name="Теги", related_name="cakes")
    order_count = models.PositiveIntegerField("Количество заказов", default=0)
    chief = models.ForeignKey(Chief, verbose_name="Кондитер", related_name="cakes", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    count = models.PositiveIntegerField("Количество")
    description = models.TextField("Описание")
    design = models.CharField("Дизайн", max_length=100)
    create_date = models.DateField("Дата добавления", auto_now_add=True)
    due_date = models.DateField("Срок заказа")
    image = models.ImageField("Фото дизайна", upload_to='orders/', blank=True, null=True)
    chief = models.ForeignKey(Chief, verbose_name="Кондитер", related_name="chief_orders", db_index=True, on_delete=models.CASCADE)
    client = models.ForeignKey(Person, verbose_name="Клиент", related_name="client_orders", db_index=True, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Cake, verbose_name="Торт", db_index=True, null=True, on_delete=models.SET_NULL)


class Category(models.Model):
    name = models.CharField("Название категории", max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField("Название тега", max_length=100)
    category = models.ForeignKey(Category, verbose_name="Категория", related_name="tags", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
