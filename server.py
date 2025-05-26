"""
Flask server for emotion detection API.
Handles text input validation and emotion analysis.
"""

from flask import Flask, request, jsonify, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route('/emotionDetector', methods=['GET', 'POST'])
def analyze_emotion():
    """
    Endpoint to analyze emotions from text.
    Handles both GET and POST requests.
    """
    if request.method == 'GET':
        text_to_analyze = request.args.get('textToAnalyze')
    else:
        data = request.get_json()
        text_to_analyze = data.get('text') if data else None

    if not text_to_analyze:
        return jsonify({"error": "Invalid text! Please try again!"}), 400

    emotions = emotion_detector(text_to_analyze)

    if emotions.get("dominant_emotion") is None:
        return jsonify({"error": "Invalid text! Please try again!"}), 400

    formatted_response = (
        f"For the given statement, the system response is 'anger': {emotions['anger']}, "
        f"'disgust': {emotions['disgust']}, 'fear': {emotions['fear']}, "
        f"'joy': {emotions['joy']} and 'sadness': {emotions['sadness']}. "
        f"The dominant emotion is {emotions['dominant_emotion']}."
    )

    return formatted_response

@app.route("/")
def render_index_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)