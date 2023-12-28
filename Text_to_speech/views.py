from django.shortcuts import render
from django.http import HttpResponse
import elevenlabs
from django.http import JsonResponse
from PyPDF2 import PdfReader


# Create your views here.

def speakify(request):
    return render(request, 'code.html', {})


def generate_and_play_audio(request):
    if request.method == 'POST':
        voice_input = request.POST.get('voice_input')
        text_input = request.POST.get('text_input')

        # Check if the entered voice is valid
        voice_mapping = {
            "Adam": elevenlabs.generate,
            "Antoni": elevenlabs.generate,
            "Arnold": elevenlabs.generate,
            "Callum": elevenlabs.generate,
            "Charlie": elevenlabs.generate,
            "Charlotte": elevenlabs.generate,
            "Clyde": elevenlabs.generate,
            "Daniel": elevenlabs.generate,
            "Dave": elevenlabs.generate,
            "Domi": elevenlabs.generate,
            "Dorothy": elevenlabs.generate,
            "Ell": elevenlabs.generate,
            "Emil": elevenlabs.generate,
            "Ethan": elevenlabs.generate,
            "Fin:": elevenlabs.generate,
            "Freya": elevenlabs.generate,
            "Gigi": elevenlabs.generate,
            "Giovanni": elevenlabs.generate,
            "Glinda": elevenlabs.generate,
            "Grace": elevenlabs.generate,
            "Harry": elevenlabs.generate,
            "James": elevenlabs.generate,
            "Jeremy": elevenlabs.generate,
            "Joseph": elevenlabs.generate,
            "Josh": elevenlabs.generate,
            "Liam": elevenlabs.generate,
            "Matilda": elevenlabs.generate,
            "Matthew": elevenlabs.generate,
            "Michael": elevenlabs.generate,
            "Mimi": elevenlabs.generate,
            "Nicole": elevenlabs.generate,
            "Patrick": elevenlabs.generate,
            "Rachel": elevenlabs.generate,
            "Ryan": elevenlabs.generate,
            "Sam": elevenlabs.generate,
            "Serena": elevenlabs.generate,
            "Thomas": elevenlabs.generate,  
        }

        if voice_input not in voice_mapping:
            return HttpResponse(f"Voice '{voice_input}' not recognized.")

        # Get the corresponding function and generate audio
        generate_function = voice_mapping[voice_input]
        audio = generate_function(text=text_input, voice=voice_input, model="eleven_multilingual_v2")  # Pass the model parameter here
        elevenlabs.play(audio)

        # Set the Content-Disposition header to force download prompt
        response = HttpResponse(audio, content_type='audio/mpeg')
        response['Content-Disposition'] = 'attachment; filename="output.mp3"'
        return response

    else:
        return render(request, 'Text_to_speech/code.html')
    
    
def extract_text(request):
    if request.method == 'POST' and request.FILES.get('pdfFile'):
        pdf_file = request.FILES['pdfFile']

        try:
            pdf_reader = PdfReader(pdf_file)
            extracted_text = ""

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                extracted_text += page.extract_text()

            return render(request, 'code.html', {'extracted_text': extracted_text})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)