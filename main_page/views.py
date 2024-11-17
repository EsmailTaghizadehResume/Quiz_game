import hashlib
import hmac
import json
from urllib.parse import unquote

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def validate_init_data(init_data: str, bot_token: str):
    vals = {k: unquote(v) for k, v in [s.split('=', 1) for s in init_data.split('&')]}
    data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted(vals.items()) if k != 'hash')

    secret_key = hmac.new("WebAppData".encode(), bot_token.encode(), hashlib.sha256).digest()
    h = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256)
    return h.hexdigest() == vals['hash']


def main_page(request):
    return render(request, "main_page/index.html")


@csrf_exempt  # Only use this for testing, ideally handle CSRF tokens in production
def initial_user(request):
    if request.method == "OPTIONS":
        # Respond to preflight OPTIONS request
        return JsonResponse({'status': 'ok'}, status=200)

    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON payload
            telegram_data = data.get('data')  # Access 'data' key from AJAX request
            # print(telegram_data.get("initData"))
            if telegram_data.get("initData"):
                is_authorized_user = validate_init_data(telegram_data.get("initData"),
                                                        "your bot token")
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

            # Process the `telegram_data` as needed

            # Return a success response
            return JsonResponse({'status': 'success', 'received_data': telegram_data})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    # Handle non-POST requests
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
