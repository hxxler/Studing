from django.db import models

class Library(models.Model):
    library_number = models.AutoField(primary_key=True, verbose_name='№БИБЛИОТЕКИ')
    address = models.CharField(max_length=255, verbose_name='АДРЕС')
    phone = models.CharField(max_length=15, verbose_name='ТЕЛЕФОН')

    def __str__(self):
        return f'Библиотека {self.library_number}'

    class Meta:
        verbose_name = 'БИБЛИОТЕКА'
        verbose_name_plural = 'БИБЛИОТЕКИ'
