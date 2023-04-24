from django.db import models

# Create your models here.


#TODO создать модель


class Shipments(models.Model):
    number_of_shipment = models.IntegerField(default=1, primary_key=True)
    time = models.DateTimeField(auto_now_add=False)
    img = models.ImageField(upload_to='images/')

    def __str__(self):
        tm = self.time.strftime("%d.%m.%Y %H:%M:%S")
        return tm

    class Meta:
        verbose_name_plural = 'Погрузки'
        verbose_name = 'Погрузка'