from django.db import models
from django.conf import settings


class Directory(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.type})"


class Client(models.Model):
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.second_name} {self.telephone}"


class Order(models.Model):
    description = models.CharField(max_length=255)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    serial_number = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Progress(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Принят в работу', 'Принят в работу'),
        ('Готов к выдаче', 'Готов к выдаче'),
        ('Завершен', 'Завершен'),
    ]

    status = models.CharField(max_length=255, choices=ORDER_STATUS_CHOICES)
    notes = models.CharField(max_length=255)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        existing_statuses = Progress.objects.filter(order=self.order).values_list('status', flat=True)

        if self.status in existing_statuses:
            raise ValueError('Статус уже существует для этого заказа.')

        # Если заказ уже имеет статус "Готов к выдаче", мы не позволяем установить более ранние статусы
        if 'Готов к выдаче' in existing_statuses and self.status != 'Завершен':
            raise ValueError('Заказ уже готов к выдаче. Можно установить только статус "Завершен".')

        super().save(*args, **kwargs)