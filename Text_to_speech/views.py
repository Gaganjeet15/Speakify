from django.shortcuts import render
from django.http import HttpResponse
import elevenlabs
from django.http import JsonResponse
from PyPDF2 import PdfReader


# Create your views here.


# Render the initial page for text-to-speech conversion
def speakify(request):
    return render(request, 'code.html', {})

# Handle the form submission for generating and playing audio
def generate_and_play_audio(request):
    if request.method == 'POST':
        voice_input = request.POST.get('voice_input')
        text_input = request.POST.get('text_input')
        action = request.POST.get('action')

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
             "Ethan": elevenlabs.generate,
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
              "Sam": elevenlabs.generate,
              "Serena": elevenlabs.generate,
              "Thomas": elevenlabs.generate,  
        }

        if voice_input not in voice_mapping:
            return HttpResponse(f"Voice '{voice_input}' not recognized.")

        generate_function = voice_mapping[voice_input]
        audio = generate_function(text=text_input, voice=voice_input, model="eleven_multilingual_v2")

        if not generate_function:
            return HttpResponse(f"Error: Unable to find generate function for voice '{voice_input}'.")

        try:
            audio = generate_function(text=text_input, voice=voice_input, model="eleven_multilingual_v2")
        except Exception as e:
            return HttpResponse(f"Error generating audio: {str(e)}")

        if not audio or not isinstance(audio, bytes):
            return HttpResponse("Error: Invalid audio data.")

        if not audio.startswith(b'\xFF\xFB'):
            return HttpResponse("Error: Invalid audio format. Expected MP3 data.")

        if action == 'play':
            elevenlabs.play(audio)
            return HttpResponse("Audio played successfully.")
        elif action == 'download':
            response = HttpResponse(audio, content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename="output.mp3"'
            return response
        else:
            return HttpResponse("Error: Invalid action.")
    else:
        return render(request, 'Text_to_speech/generate_audio.html')
    
# Extract text from a PDF file
def extract_text(request):
    if request.method == 'POST' and request.FILES.get('pdfFile'):
        pdf_file = request.FILES['pdfFile']

        try:
            # Use PyPDF2 to extract text from each page of the PDF
            pdf_reader = PdfReader(pdf_file)
            extracted_text = ""

            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                extracted_text += page.extract_text()

            return render(request, 'code.html', {'extracted_text': extracted_text})
        except Exception as e:
            # Return an error response if there's an exception during text extraction
            return JsonResponse({'error': str(e)}, status=500)

    # Return an error response for invalid requests
    return JsonResponse({'error': 'Invalid request'}, status=400)