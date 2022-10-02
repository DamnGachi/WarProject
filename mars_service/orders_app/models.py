from django.db import models
from datetime import datetime


class Device(models.Model):
    class Meta:
        db_table = 'devices'
        verbose_name = 'Allow equipment'
        verbose_name_plural = 'Allow equipment'

    manufacturer = models.TextField(verbose_name='manufacturer')
    model = models.TextField(verbose_name='Model')

    def __str__(self):
        return f'{self.manufacturer}{self.model}'


class Customer(models.Model):
    class Meta:
        db_table = "customers"
        verbose_name = "Description contragent"
        verbose_name_plural = "Description contragents"

    customer_name = models.TextField(verbose_name="Name organization")
    customer_address = models.TextField(verbose_name="address")
    customer_city = models.TextField(verbose_name="City")

    def __str__(self):
        return f"{self.customer_name} address: {self.customer_address}"


class DeviceInField(models.Model):
    class Meta:
        db_table = "devices_in_fields"
        verbose_name = "Equipment in fields"
        verbose_name_plural = "Equipment in fields"

    serial_number = models.TextField(verbose_name="S/N")
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, verbose_name="Users")
    analyzer = models.ForeignKey(Device, on_delete=models.RESTRICT, verbose_name="Equipment")
    owner_status = models.TextField(verbose_name="Owner status")

    def __str__(self):
        return f"{self.analyzer} s/n {self.serial_number} in {self.customer}"


class Order(models.Model):
    class Meta:
        db_table = "orders"
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    statuses = (("open", "open"),
                ("closed", "closed"),
                ("in progress", "working"),
                ("need info", "need info"))

    device = models.ForeignKey(DeviceInField, verbose_name="equipment", on_delete=models.RESTRICT)
    order_description = models.TextField(verbose_name="description")
    created_dt = models.DateTimeField(verbose_name="Created", auto_now_add=True)
    last_update_data = models.DateTimeField(verbose_name="last update", blank=True, null=True)
    order_status = models.TextField(verbose_name="Order status", choices=statuses)

    def __str__(self):
        return f"Order №{self.id} for {self.device}"

    def save(self, *args, **kwargs):
        self.last_updated_dt = datetime.now()
        super().save(*args, **kwargs)
