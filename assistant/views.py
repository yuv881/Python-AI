import json
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from command_handler import process_command
from speech_engine import clear_speech_buffer, get_speech_buffer, speak


def index(request):
    return render(request, 'assistant/index.html')


def google_verification(request):
    return HttpResponse("google-site-verification: google2f83435a64a9c20c.html", content_type="text/plain")


def get_client_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


def is_rate_limited(request):
    limit = settings.COMMAND_RATE_LIMIT
    window = settings.COMMAND_RATE_LIMIT_WINDOW
    cache_key = f"rate-limit:command:{get_client_ip(request)}"

    added = cache.add(cache_key, 1, window)
    if added:
        return False, max(limit - 1, 0)

    try:
        count = cache.incr(cache_key)
    except ValueError:
        cache.set(cache_key, 1, window)
        return False, limit

    remaining = max(limit - count, 0)
    return count > limit, remaining


@csrf_exempt
def process_command_api(request):
    if request.method == 'POST':
        limited, remaining = is_rate_limited(request)
        if limited:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Rate limit exceeded. Please try again later.',
                },
                status=429,
                headers={'Retry-After': str(settings.COMMAND_RATE_LIMIT_WINDOW)},
            )

        try:
            data = json.loads(request.body.decode('utf-8'))
            command = data.get('command', '').strip()
        except Exception:
            command = request.POST.get('command', '').strip()

        if not command:
            return JsonResponse({'status': 'error', 'message': 'No command provided.'}, status=400)

        clear_speech_buffer()
        should_continue = process_command(command)
        responses = get_speech_buffer()

        return JsonResponse({
            'status': 'success',
            'command': command,
            'responses': responses,
            'should_continue': should_continue,
            'rate_limit_remaining': remaining,
        })

    return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=405)
