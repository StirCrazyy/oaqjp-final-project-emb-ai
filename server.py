"""
Flask server for emotion detection API.
Handles text input validation and emotion analysis.
"""

from flask import Flask, request, jsonify, render_template
from EmotionDetection.emotion_detection import emotion_detector  # Import function

app = Flask(__name__)

@app.route('/emotionDetector', methods=['GET','POST'])
def analyze_emotion():
    """
    Endpoint to analyze emotions from a given text.
    
    Request format:
    {
        "text": "<user_input_text>"
    }
    
    Returns:
    {
        "response": "Formatted emotion analysis result"
    }
    
    Handles missing text input with proper error messages.
    """
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Invalid text! Please try again!"}), 400

    text_to_analyze = data["text"]
    emotions = emotion_detector(text_to_analyze)

    if emotions["dominant_emotion"] is None:
        return jsonify({"error": "Invalid text! Please try again!"}), 400

    formatted_response = (
        f"For the given statement, the system response is 'anger': {emotions['anger']}, "
        f"'disgust': {emotions['disgust']}, 'fear': {emotions['fear']}, "
        f"'joy': {emotions['joy']} and 'sadness': {emotions['sadness']}. "
        f"The dominant emotion is {emotions['dominant_emotion']}."
    )

    return jsonify({"response": formatted_response})

@app.route("/")
def render_index_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
