from django.db import models

class Solution(models.Model):
    a = models.FloatField()
    b = models.FloatField()
    c = models.FloatField()
    solution = models.CharField(max_length=255)
    user_solution = models.CharField(max_length=255, default="Нет ответа")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Уравнение: {self.a}x² + {self.b}x + {self.c} = 0, Решение: {self.solution}, Ответ: {self.user_solution}"

