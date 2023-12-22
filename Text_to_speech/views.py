from django.shortcuts import render
from django.http import HttpResponse
import elevenlabs
elevenlabs.set_api_key("c874cb0113399e1d4d26bd0a0947a761")
# Create your views here.

def todolist(request):
    return render(request, 'code.html', {})


def generate_and_play_audio(request):
    if request.method == 'POST':
        voice_input = request.POST.get('voice_input')
        text_input = request.POST.get('text_input')

        # Check if the entered voice is valid
        voice_mapping = {
            "Adam": elevenlabs.generate,
            # ... (other voices)
        }

        if voice_input not in voice_mapping:
            return HttpResponse(f"Voice '{voice_input}' not recognized.")

        # Get the corresponding function and generate audio
        generate_function = voice_mapping[voice_input]
        audio = generate_function(text=text_input, voice=voice_input)
        elevenlabs.play(audio)
 
        return HttpResponse("Audio generated and played successfully.")
    else:
        return render(request, 'Text_to_speech/generate_audio.html')