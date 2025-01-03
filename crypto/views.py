import base64
import io
import logging
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.cache import cache
from django.shortcuts import redirect, render

from .models import CryptoRequest

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

BINANCE_API_URL = "https://api.binance.com/api/v3"



def get_crypto_price(symbol):
    try:
        logger.debug("Запрос текущей цены для символа: %s", symbol)
        response = requests.get(
            f"{BINANCE_API_URL}/ticker/price", params={"symbol": symbol}
        )
        logger.debug("Ответ API: %s", response.text)

        if response.status_code == 200:
            data = response.json()
            return float(data["price"])
        else:
            logger.error("Ошибка API Binance: %s", response.status_code)
            return None
    except Exception as e:
        logger.exception("Ошибка при взаимодействии с API Binance")
        return None


def get_historical_data(symbol):
    try:
        logger.debug("Запрос исторических данных для символа: %s", symbol)
        response = requests.get(
            f"{BINANCE_API_URL}/klines",
            params={"symbol": symbol, "interval": "1h", "limit": 10},
        )
        logger.debug("Ответ API: %s", response.text)

        if response.status_code == 200:
            data = response.json()
            timestamps = [datetime.fromtimestamp(entry[0] / 1000) for entry in data]
            prices = [float(entry[4]) for entry in data]
            return timestamps, prices
        else:
            logger.error("Ошибка API Binance: %s", response.status_code)
            return None, None
    except Exception as e:
        logger.exception("Ошибка при получении исторических данных")
        return None, None


def validate_symbol(symbol):
    return symbol.upper() + "USDT"


def is_valid_symbol(symbol):
    try:
        logger.debug("Проверка доступного символа: %s", symbol)
        response = requests.get(f"{BINANCE_API_URL}/exchangeInfo")
        if response.status_code == 200:
            symbols = [item["symbol"] for item in response.json()["symbols"]]
            return symbol in symbols
        logger.error(
            "Ошибка при получении информации о символах: %s", response.status_code
        )
        return False
    except Exception as e:
        logger.exception("Ошибка проверки символа")
        return False


@login_required
def crypto_request_view(request):
    if request.method == "POST":
        crypto_name = request.POST.get("crypto_name", "").strip().upper()
        if not crypto_name:
            logger.error("Поле crypto_name отсутствует в запросе.")
            return render(
                request,
                "crypto_result.html",
                {
                    "crypto_name": None,
                    "data": {"error": "Не указано имя криптовалюты."},
                },
            )

        symbol = validate_symbol(crypto_name)

        if not is_valid_symbol(symbol):
            logger.warning("Символ %s не поддерживается Binance", symbol)
            return render(
                request,
                "crypto_result.html",
                {
                    "crypto_name": crypto_name,
                    "data": {"error": "Символ не поддерживается Binance."},
                },
            )

        cache_key = f"crypto_{crypto_name}_price"

        price = cache.get(cache_key)
        if not price:
            price = get_crypto_price(symbol)
            if price is not None:
                cache.set(cache_key, price, timeout=3600)

        if price is None:
            logger.warning("Не удалось получить цену для символа: %s", crypto_name)
            return render(
                request,
                "crypto_result.html",
                {
                    "crypto_name": crypto_name,
                    "data": {"error": "Не удалось получить данные."},
                },
            )

        CryptoRequest.objects.create(
            user=request.user,
            cryptocurrency=crypto_name,
            response_data={"price": price},
        )

        return render(
            request,
            "crypto_result.html",
            {"crypto_name": crypto_name, "data": {"price": price}},
        )

    return render(request, "crypto_form.html")


@login_required
def crypto_graph_view(request):
    crypto_name = request.GET.get("crypto_name", "BTC").strip().upper()
    symbol = validate_symbol(crypto_name)

    if not is_valid_symbol(symbol):
        logger.warning("Символ %s не поддерживается Binance", symbol)
        return render(
            request,
            "crypto_graph_error.html",
            {"error": "Символ не поддерживается Binance."},
        )

    cache_key = f"crypto_{crypto_name}_graph"

    graph_data = cache.get(cache_key)
    if not graph_data:
        timestamps, values = get_historical_data(symbol)
        if timestamps is None or values is None:
            return render(
                request,
                "crypto_graph_error.html",
                {"error": "Не удалось получить данные для графика."},
            )

        graph_data = {"timestamps": timestamps, "values": values}
        cache.set(cache_key, graph_data, timeout=3600)
    else:
        timestamps = graph_data["timestamps"]
        values = graph_data["values"]

    plt.figure(figsize=(10, 5))
    plt.plot(
        timestamps,
        values,
        label=f"Цена {crypto_name} в USD",
        color="#f3ba2f",
        marker="o",
        linewidth=2,
    )
    plt.xlabel("Время", fontsize=12, color="#333")
    plt.ylabel("Цена (USD)", fontsize=12, color="#333")
    plt.title(f"График изменения цены {crypto_name}", fontsize=14, color="#f3ba2f")
    plt.legend(loc="upper left", fontsize=10, frameon=False)
    plt.grid(color="#e0e0e0", linestyle="--", linewidth=0.5)

    ax = plt.gca()
    ax.xaxis.set_major_locator(MaxNLocator(6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    plt.gcf().autofmt_xdate(rotation=0)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color("#f3ba2f")
    ax.spines["left"].set_color("#f3ba2f")
    ax.tick_params(axis="x", colors="#333")
    ax.tick_params(axis="y", colors="#333")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    buf.close()

    logger.debug("График успешно построен для символа: %s", symbol)

    return render(request, "crypto_graph.html", {"image_base64": image_base64})


@login_required
def crypto_about_view(request):
    return render(request, "crypto_about.html")


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
