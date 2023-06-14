import os
import openai
from pytube import YouTube
from flask import Flask, request

app = Flask(__name__)

api_key = os.getenv('API_KEY')

def downloadAudio(url):
    yt = YouTube(url) 
    title = yt.title
    # extract only audio
    video = yt.streams.filter(only_audio=True).first()
    
    # check for destination to save file
    destination = '.'
    
    # download the file
    out_file = video.download(output_path=destination)
    
    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return {"file":new_file, "title":title}

@app.route('/api', methods=['POST'])
def api_endpoint():
    # Load your API key from an environment variable or secret management service
    openai.api_key = api_key
    file_info = downloadAudio(request.get_data().decode('ISO-8859-1'))
    audio_file= open(file_info['file'], "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return {"transcript":transcript, "title":file_info['title']}  # Replace this with your desired response

if __name__ == '__main__':
    app.run()


