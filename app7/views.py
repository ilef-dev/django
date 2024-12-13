from django.shortcuts import render
from math import sqrt

def main(request):
    try:
        if 'a' not in request.GET or 'b' not in request.GET or 'c' not in request.GET:
            return render(request, 'main.html', {'equation': "Ошибка!", 'result': "Параметры a, b и c обязательны!"})

        a = float(request.GET.get('a', 0))
        b = float(request.GET.get('b', 0))
        c = float(request.GET.get('c', 0))

        if a == 0 and b == 0:
            if c == 0:
                result = "Бесконечное количество решений."
            else:
                result = "Нет решений."
        elif a == 0:
            x = -c / b
            x = 0 if x == 0 else x
            result = f"x = {x:.2f}"
        else:
            discriminant = b**2 - 4*a*c
            if discriminant < 0:
                result = "Нет действительных корней."
            elif discriminant == 0:
                x = -b / (2*a)
                x = 0 if x == 0 else x
                result = f"Один корень: x = {x:.2f}"
            else:
                x1 = (-b + sqrt(discriminant)) / (2*a)
                x2 = (-b - sqrt(discriminant)) / (2*a)
                result = f"Два корня: x₁ = {x1:.2f}, x₂ = {x2:.2f}"
    except ValueError:
        result = "Ошибка: все коэффициенты должны быть числами."

    equation = f"{a}x² + {b}x + {c} = 0"
    return render(request, 'main.html', {'equation': equation, 'result': result})
