from django.db import models

class Клиент(models.Model):
    Имя = models.CharField(max_length=255)
    Адрес = models.CharField(max_length=255)
    Телефон = models.CharField(max_length=15)

    def __str__(self):
        return self.Имя

class Выпечка(models.Model):
    Название = models.CharField(max_length=255)
    Тип = models.CharField(max_length=50)
    Стоимость = models.IntegerField()
    Описание = models.CharField(max_length=255)

    def __str__(self):
        return self.Название

class Доставка(models.Model):
    Заказ_id = models.ForeignKey('Заказ', on_delete=models.CASCADE)
    Адрес_Доставки = models.CharField(max_length=255)
    Дата_Доставки = models.DateField()
    Статус_Доставки = models.CharField(max_length=50)

    def __str__(self):
        return f"Доставка для заказа {self.Заказ_id}"

class Пекарь(models.Model):
    Имя = models.CharField(max_length=255)
    Фамилия = models.CharField(max_length=255)
    Контактный_Телефон = models.IntegerField()

    def __str__(self):
        return f"{self.Имя} {self.Фамилия}"

class Заказ(models.Model):
    Клиент_id = models.ForeignKey('Клиент', on_delete=models.CASCADE)
    Выпечка_id = models.ForeignKey('Выпечка', on_delete=models.CASCADE)
    Пекарь_id = models.ForeignKey('Пекарь', on_delete=models.CASCADE)
    Количество = models.IntegerField()
    Сумма_Заказа = models.IntegerField()
    Дата_Заказа = models.DateField()

    def __str__(self):
        return f"Заказ от {self.Клиент_id} на {self.Выпечка_id}"

