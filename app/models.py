from django.contrib.auth.models import User
from django.db import models


class Order(models.Model):
    name = models.CharField(max_length=20, help_text="Название заявки", blank=False)
    description = models.TextField(max_length=1000, help_text="Описание заявки", blank=False)

    CATEGORIES = (
        ('3d', '3D-дизайн'),
        ('2d', '2D-дизайн'),
        ('эс', 'Эскиз')
    )

    category = models.CharField(max_length=2, choices=CATEGORIES, blank=False, default=None,
                                help_text='Категория заявки')
    plan = models.ImageField(upload_to='uploads/% Y/% m/% d/', blank=False)

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
