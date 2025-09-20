from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class City(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название города')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

class Advertisement(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Цена'
    )
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

class Response(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонён'),
    ]
    
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, verbose_name='Объявление')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_responses', verbose_name='Отправитель')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_responses', verbose_name='Получатель')
    message = models.TextField(verbose_name='Сообщение', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    def __str__(self):
        return f"Отклик от {self.sender} на {self.advertisement}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'