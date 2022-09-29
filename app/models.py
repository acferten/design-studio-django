from django.contrib.auth.models import User
from django.core.validators import validate_image_file_extension, FileExtensionValidator
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, help_text="Введите категорию заявки", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ('can_delete_category', 'Может удалять категории'), ('can_create_category', 'Может добавлять категории'),)


class Order(models.Model):
    name = models.CharField(max_length=20, help_text="Название заявки", blank=False)
    description = models.TextField(max_length=1000, help_text="Описание заявки", blank=False)

    category = models.ForeignKey(Category, to_field='name', help_text='Категория заявки', blank=False,
                                 on_delete=models.CASCADE)
    plan = models.ImageField(upload_to='app/files/plans', blank=False,
                             validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp'])])

    LOAN_STATUS = (
        ('н', 'Новая'),
        ('п', 'Принято в работу'),
        ('в', 'Выполнено'),
    )

    date = models.DateField(auto_now=True, blank=False)
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=False, default='н', help_text='Статус заявки')

    class Meta:
        ordering = ["date"]
        permissions = (('can_change_status', 'Менять статус заявки'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.id)])

    def display_category(self):
        return ', '.join([category.name for category in self.category.all()[:3]])

    design = models.ImageField(upload_to='app/files/designs', blank=True)
    orderer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    comment = models.TextField(max_length=1000, help_text="Комментарий исполнителя", blank=True)
