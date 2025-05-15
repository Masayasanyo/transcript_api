from flask import Flask, jsonify, request
from youtube_transcript_api import YouTubeTranscriptApi, VideoUnavailable
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/subtitles', methods=['GET'])
def get_subtitles():
    video_id = request.args.get('video_id')
    lang = request.args.get('language')

    if not video_id:
        return jsonify({'error': 'Video id required.'}), 400
    if not lang:
        return jsonify({'error': 'Language is required.'}), 400
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
    except VideoUnavailable:
        return jsonify({'error': 'The video is unavailable or does not exist.'}), 404
    except Exception:
        return jsonify({'error': 'Internal server error'}), 500
    
    wordList = []
    for segment in transcript:
        words = segment["text"].replace("-", " ").split()
        wordList.extend(words)

    return jsonify({
        'video_id': video_id, 
        'transcript': wordList
    }), 200

if __name__ == '__main__':
    app.run(port=5000)