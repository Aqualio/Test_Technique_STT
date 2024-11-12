Test Technique
Création d'une API REST permettant de transcrire un fichier audio au format .wav en texte. 
L'API étant countenerisé sur Docker

Etapes pour lancer l'application:

'''
git clone https://github.com/Aqualio/Test_Technique_STT
'''
'''
cd Test_Technique_STT
'''
'''
docker build -t stt_api_rest .
'''
On récupère le nom de l'image si besoin:
'''
docker images
'''
Run:
'''
docker run -i -t stt_api_rest:latest
'''
Ouvrir une page web sur http://127.0.0.1:5000 ou http://172.17.0.2:5000

Upload un ficher .wav 
