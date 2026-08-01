import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from command_handler import process_command
from speech_engine import clear_speech_buffer, get_speech_buffer, speak


def index(request):
    return render(request, 'assistant/index.html')


@csrf_exempt
def process_command_api(request):
    if request.method == 'POST':
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
            'should_continue': should_continue
        })

    return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=405)
