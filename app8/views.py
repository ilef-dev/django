from django.shortcuts import render, redirect
from .models import Solution
from math import sqrt
import random

def generate_equation(request):
    random_a = random.randint(-15, 15)
    random_b = random.randint(-15, 15)
    random_c = random.randint(-15, 15)

    request.session['a'] = random_a
    request.session['b'] = random_b
    request.session['c'] = random_c

    return render(request, 'solve.html', {
        'random_a': random_a,
        'random_b': random_b,
        'random_c': random_c,
    })

def check_solution(request):
    user_feedback = None
    correct_solution = None
    user_solution = None

    a = request.session.get('a')
    b = request.session.get('b')
    c = request.session.get('c')

    if a is None or b is None or c is None:
        return redirect('generate_equation')

    discriminant = b**2 - 4 * a * c

    if discriminant < 0:
        correct_solution = "Нет решений"
    elif discriminant == 0:
        x = -b / (2 * a)
        correct_solution = f"x = {x:.2f}"
    else:
        x1 = (-b + sqrt(discriminant)) / (2 * a)
        x2 = (-b - sqrt(discriminant)) / (2 * a)
        correct_solution = f"x₁ = {x1:.2f}, x₂ = {x2:.2f}"

    if request.method == 'GET' and ('x1' in request.GET or 'bkr' in request.GET or 'nr' in request.GET):
        try:
            x1 = request.GET.get('x1')
            x2 = request.GET.get('x2')
            x = request.GET.get('x')
            bkr = request.GET.get('bkr')
            nr = request.GET.get('nr')

            if bkr:
                user_feedback = "правильно!" if a == 0 and b == 0 and c == 0 else "ответ неверный"
                user_solution = "Бесконечное количество решений"
            elif nr:
                user_solution = "Нет решений"
                user_feedback = "правильно!" if discriminant < 0 else "ответ неверный"
            elif x1 and x2:
                x1 = float(x1)  # Проверка преобразования
                x2 = float(x2)
                user_solution = f"x₁ = {x1:.2f}, x₂ = {x2:.2f}"
                if user_solution == correct_solution:
                    user_feedback = "правильно!"
                else:
                    user_feedback = "ответ неверный"
            elif x:
                x = float(x)  # Проверка преобразования
                user_solution = f"x = {x:.2f}"
                if user_solution == correct_solution:
                    user_feedback = "правильно!"
                else:
                    user_feedback = "ответ неверный"
            else:
                user_feedback = "выберите хотя бы один вариант ответа"
        except ValueError:
            user_feedback = "Введите числовые значения для x, x1 и x2."
    if user_solution:
        Solution.objects.create(a=a, b=b, c=c, solution=correct_solution, user_solution=user_solution)

    return render(request, 'solve.html', {
        'random_a': a,
        'random_b': b,
        'random_c': c,
        'user_feedback': user_feedback,
        'solution': correct_solution,
    })
