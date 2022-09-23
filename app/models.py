from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, help_text="Введите категорию заявки")

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField(max_length=20, help_text="Название заявки", blank=False)
    description = models.TextField(max_length=1000, help_text="Описание заявки", blank=False)

    category = models.ForeignKey(Category, help_text="Выберите категорию заявки", on_delete=models.CASCADE)

    plan = models.ImageField(upload_to='app/files/plans', blank=False)

    LOAN_STATUS = (
        ('н', 'Новая'),
        ('п', 'Принято в работу'),
        ('в', 'Выполнено'),
    )

    date = models.DateField(auto_now=True, blank=False)
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=False, default='н', help_text='Статус заявки')

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.id)])

    def display_category(self):
        return ', '.join([category.name for category in self.category.all()[:3]])

    design = models.ImageField(upload_to='app/files/designs', blank=True)
    orderer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)


