from django.shortcuts import render, redirect
from django.http import HttpResponse
import elevenlabs
import PyPDF2
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

    #     if voice_input not in voice_mapping:
    #         return HttpResponse(f"Voice '{voice_input}' not recognized.")

    #     # Get the corresponding function and generate audio
    #     generate_function = voice_mapping[voice_input]
    #     audio = generate_function(text=text_input, voice=voice_input)
    #     elevenlabs.play(audio)
    #     elevenlabs.save(audio, "output.mp3")  
    #     return render(request, 'generate_audio.html' )
    # else:
    #     return render(request, 'Text_to_speech/code.html')
        if voice_input not in voice_mapping:
            return HttpResponse(f"Voice '{voice_input}' not recognized.")

        # Get the corresponding function and generate audio
        generate_function = voice_mapping[voice_input]
        audio = generate_function(text=text_input, voice=voice_input)
        elevenlabs.play(audio)
        elevenlabs.save(audio, "output.mp3")

        # Set the Content-Disposition header to force download prompt
        response = HttpResponse(audio, content_type='audio/mpeg')
        response['Content-Disposition'] = 'attachment; filename="output.mp3"'
        return response

    else:
        return render(request, 'Text_to_speech/code.html')
    
    
    
def extract_text(pdf_file):
    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        text = ''
        for page_num in range(pdf_reader.numPages):
            text += pdf_reader.getPage(page_num).extractText()
    return text

def upload_and_extract(request):
    if request.method == 'POST' and 'pdf_file' in request.FILES:
        pdf_file = request.FILES['pdf_file']
        
        # Check if the uploaded file is a PDF
        if pdf_file.name.endswith('.pdf'):
            # Extract text from the PDF
            pdf_text = extract_text(pdf_file)

            # Render the result on the same page
            return render(request, 'code.html', {'pdf_text': pdf_text})
        else:
            return render(request, 'code.html', {'error': 'Please upload a PDF file.'})

    return render(request, 'code.html')