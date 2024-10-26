from django.shortcuts import render
from django.http import HttpResponse

def input_form(request):
    return render(request, 'quadratic/input_form.html')

def solve_quadratic(request):
    a = float(request.GET.get('a', 0))
    b = float(request.GET.get('b', 0))
    c = float(request.GET.get('c', 0))

    discriminant = b**2 - 4*a*c
    if discriminant > 0:
        x1 = (-b + discriminant**0.5) / (2 * a)
        x2 = (-b - discriminant**0.5) / (2 * a)
        result = f'Корни уравнения: x1 = {round(x1, 2)}, x2 = {round(x2, 2)}'
    elif discriminant == 0:
        x = -b / (2 * a)
        result = f'Уравнение имеет один корень: x = {x}'
    else:
        result = 'Уравнение не имеет вещественных корней.'

    return render(request, 'quadratic/result.html', {'result': result})
