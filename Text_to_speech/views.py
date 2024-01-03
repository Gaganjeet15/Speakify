from django.shortcuts import render
from django.http import HttpResponse
import elevenlabs
from django.http import JsonResponse
from PyPDF2 import PdfReader
elevenlabs.set_api_key('6f74a30fefe9236f5b558cba1c98811e')

# Create your views here.


# Render the initial page for text-to-speech conversion
def speakify(request):
    return render(request, 'code.html', {})

# Handle the form submission for generating and playing audio
def generate_and_play_audio(request):
    if request.method == 'POST':
         # Get input from the form       
        voice_input = request.POST.get('voice_input')
        text_input = request.POST.get('text_input')

        # Map voices to their corresponding generate function
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
        # Check if the entered voice is valid
        if voice_input not in voice_mapping:
            return HttpResponse(f"Voice '{voice_input}' not recognized.")

        # Get the corresponding function and generate audio
        generate_function = voice_mapping[voice_input]
        audio = generate_function(text=text_input, voice=voice_input, model="eleven_multilingual_v2")  # Pass the model parameter here
       
        # Play the generated audio
        elevenlabs.play(audio)
        
        
        # Check if the generate function is not available
        if not generate_function:
            return HttpResponse(f"Error: Unable to find generate function for voice '{voice_input}'.")

        try:
            # Attempt to generate audio again for validation
            audio = generate_function(text=text_input, voice=voice_input, model="eleven_multilingual_v2")  # Pass the model parameter here
        except Exception as e:
            return HttpResponse(f"Error generating audio: {str(e)}")

        # Check if the generated audio is valid
        if not audio or not isinstance(audio, bytes):
            return HttpResponse("Error: Invalid audio data.")

        # Check if the generated audio is in the expected MP3 format
        if not audio.startswith(b'\xFF\xFB'):
            return HttpResponse("Error: Invalid audio format. Expected MP3 data.")

        # Set the Content-Disposition header to force download prompt
        response = HttpResponse(audio, content_type='audio/mpeg')
        response['Content-Disposition'] = 'attachment; filename="output.mp3"'
        return response

    else:
        # Render the initial form page if the request method is not POST
        return render(request, 'Text_to_speech/code.html')
    
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