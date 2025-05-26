import requests
import json

def emotion_detector(text_to_analyse):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    
    # Handle blank entries
    if not text_to_analyse.strip():
        return {"anger": None, "disgust": None, "fear": None, "joy": None, "sadness": None, "dominant_emotion": None}
    
    myobj = {"raw_document": {"text": text_to_analyse}}

    try:
        response = requests.post(url, json=myobj, headers=headers)
        
        # Handle bad request (status_code 400)
        if response.status_code == 400:
            return {"anger": None, "disgust": None, "fear": None, "joy": None, "sadness": None, "dominant_emotion": None}

        response.raise_for_status()
        data = response.json()

        # Extract emotion scores properly
        emotions = data.get("emotionPredictions", [{}])[0].get("emotion", {})  
        relevant_emotions = {key: emotions.get(key, 0) for key in ['anger', 'disgust', 'fear', 'joy', 'sadness']}

        # Find the dominant emotion
        dominant_emotion = max(relevant_emotions, key=relevant_emotions.get) if relevant_emotions else None

        # Modify final output
        relevant_emotions["dominant_emotion"] = dominant_emotion

        return relevant_emotions

    except requests.exceptions.RequestException as e:
        return {"error": f"API Request failed: {e}"}