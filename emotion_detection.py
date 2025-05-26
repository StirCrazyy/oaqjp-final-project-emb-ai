import requests
import json

def emotion_detector(text_to_analyse):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = { "raw_document": { "text": text_to_analyse } }
    
    try:
        response = requests.post(url, json=myobj, headers=headers)
        response.raise_for_status()  # Raise an error if the request fails
        
        # Convert response text to dictionary
        data = response.json()  # Parses JSON response
        
        # Extract emotion scores
        emotions = data.get("emotion", {})  # Assuming emotions are under "emotion"
        relevant_emotions = {key: emotions.get(key, 0) for key in ['anger', 'disgust', 'fear', 'joy', 'sadness']}
        
        # Find the dominant emotion
        dominant_emotion = max(relevant_emotions, key=relevant_emotions.get)

        # Ensure the `"dominant_emotion"` is included in the final result
        relevant_emotions["dominant_emotion"] = dominant_emotion
        
        return relevant_emotions
    
    except requests.exceptions.RequestException as e:
        return {"error": f"API Request failed: {e}"}
