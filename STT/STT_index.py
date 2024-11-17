import os 
from flask import Flask, jsonify, request, render_template
from pydub import AudioSegment
import speech_recognition as sr 

ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)

# We start the recogniser function
r = sr.Recognizer()
#GOOGLE_CLOUD_SPEECH_CREDENTIALS = r""" """
#WIT_AI_KEY = "QORIUELG7IUQMICNRT45J5P7NQZ3ZNTW"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST']) # GET & POST methods because only post would return an error
def upload_file():
    # Small HTML code to input an audio file 
    return '''
    <!doctype html> 
    <head>   
        <title> File Upload </title>
    </head>   
    <body>   
        <h1>Speech to text transcription</h1> 
        <h>Upload Audio file: </h>
        <form action = "/transcription" method = "post" enctype = "multipart/form-data">   
            <input type = "file" name = "file" />   
            <input type = "submit" value = "Upload">   
        </form>   
    </body>   
    </html>
    '''

def audio_to_text(audio):
# Function to listen and put to text the audio file
    with sr.AudioFile(audio) as source:
        
        audio_listened = r.record(source) # We listen to the audio file 

        #text = r.recognize_google(audio_listened) # We recognise speech using the Google Speech Recognition API # Error with flac library using docker, works on local, installing it doesn't fix the problem
        #text = r.recognize_google_cloud(audio_listened, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS) # Error Google CLoud Service
        text = r.recognize_sphinx(audio_listened) # It is not as good as the other but it works.
        #text = r.recognize_wit(audio_listened, key=WIT_AI_KEY)
        
    return text
# Main Endpoint

@app.route('/transcription', methods=['POST']) # POST method for transcript of the .wav file
def transcription():
    if request.method == 'POST':
        file = request.files['file'] # Checking the right method
    
    if file and allowed_file(file.filename): # Checking if the file is the right format
        audio_file = file
    
    try:
        audio = audio_to_text(audio_file) # Function called 
        return render_template('Result.html', audio=audio)
    #jsonify({'Text' : audio}), 200 # We show the translated text on the web page
    except sr.UnknownValueError:
        return render_template('Result.html')
    except sr.RequestError as e:
        return render_template('Result_Cloud.html')

# Entry point
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    # Start server
    print("REST API Starting" )

    app.run(host='0.0.0.0', port=5000)