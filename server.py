from flask import Flask, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector  # Import function

app = Flask(__name__)

@app.route('/emotionDetector', methods=['POST'])
def analyze_emotion():
    # Get JSON request data
    data = request.get_json()
    
    # Ensure text input is provided
    if not data or "text" not in data:
        return jsonify({"error": "Invalid text! Please try again!"}), 400
    
    text_to_analyze = data["text"]
    
    # Run emotion detection function
    emotions = emotion_detector(text_to_analyze)

    # Check if the dominant emotion is None (invalid text)
    if emotions["dominant_emotion"] is None:
        return jsonify({"error": "Invalid text! Please try again!"}), 400

    # Format response
    formatted_response = (
        f"For the given statement, the system response is 'anger': {emotions['anger']}, "
        f"'disgust': {emotions['disgust']}, 'fear': {emotions['fear']}, "
        f"'joy': {emotions['joy']} and 'sadness': {emotions['sadness']}. "
        f"The dominant emotion is {emotions['dominant_emotion']}."
    )
    
    return jsonify({"response": formatted_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)