import sys
from flask import Flask, redirect, render_template, request, flash, url_for, send_from_directory, jsonify
from pytube import YouTube
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management, such as flash messages

# Directory where videos will be stored
DOWNLOAD_DIRECTORY = 'downloads'

if not os.path.exists(DOWNLOAD_DIRECTORY):
    os.makedirs(DOWNLOAD_DIRECTORY)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/fetch_video_details', methods=['POST'])
def fetch_video_details():
    url = request.json.get('url')
    try:
        youtube_object = YouTube(url)
        video_details = {
            'title': youtube_object.title,
            'thumbnail_url': youtube_object.thumbnail_url,
            'length': youtube_object.length
        }
        return jsonify(video_details)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def progress_function(stream, chunk, bytes_remaining):
    current = ((stream.filesize - bytes_remaining)/stream.filesize)
    percent = ('{0:.1f}').format(current*100)
    progress = int(50*current)
    sys.stdout.write('\r')
    sys.stdout.write("[%-50s] %s%%" % ('='*progress, percent))
    sys.stdout.flush()

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    try:
        youtube_object = YouTube(url, on_progress_callback=progress_function)
        youtube_stream = youtube_object.streams.get_highest_resolution()
        video_title = youtube_stream.default_filename
        youtube_stream.download(DOWNLOAD_DIRECTORY)
        return send_from_directory(DOWNLOAD_DIRECTORY, video_title, as_attachment=True)
    except Exception as e:
        flash(f'An error has occurred: {str(e)}', 'error')
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
