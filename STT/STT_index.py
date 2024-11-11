import os 
from flask import Flask, jsonify, request
from pydub import AudioSegment
import speech_recognition as sr 

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)

# We start the recogniser function
r = sr.Recognizer()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST']) # GET & POST methods because only post would return an error
def upload_file():
    # Small HTML code to input an audio file 
    return '''
    <!doctype html> 
    <head>   
        <title>upload file : </title>   
    </head>   
    <body>   
        <form action = "/transcription" method = "post" enctype="multipart/form-data">   
            <input type="file" name="file" />   
            <input type = "submit" value="Upload">   
        </form>   
    </body>   
    </html>
    '''

def audio_to_text(audio):
# Function to listen and put to text the audio file
    with sr.AudioFile(audio) as source:
        
        audio_listened = r.record(source) # We listen to the audio file 

        text = r.recognize_google(audio_listened) # We recognise speech using the Google Speech Recognition API 
        
    return text
# Main Endpoint

@app.route('/transcription', methods=['POST']) # POST method for transcript of the .wav file
def transcription():
    if request.method == 'POST':
        file = request.files['file'] # Checking the right method
    
    if file and allowed_file(file.filename): # Checking if the file is the right format
        audio_file = file
        #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    try:
        audio = audio_to_text(audio_file) # FUnction called 
        return jsonify({'Text' : audio}), 200 # We show the translated text on the web page
    except sr.UnknownValueError:
        return jsonify({'Error' : 'Could not understand audio'}), 200 
    except sr.RequestError as e:
        return jsonify({'Error' : 'Error Google Cloud Service'}), 200  

# Entry point
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))

    # Start server
    print("REST API Starting" )

    app.run(host='0.0.0.0', port=5000)