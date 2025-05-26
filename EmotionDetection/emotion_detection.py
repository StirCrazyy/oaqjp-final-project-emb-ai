import requests
import json

def emotion_detector(text_to_analyse):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    myobj = {"raw_document": {"text": text_to_analyse}}

    try:
        response = requests.post(url, json=myobj, headers=headers)
        response.raise_for_status()  # Ensure request was successful

        # Convert response text into a dictionary
        data = response.json()

        # Extract emotion scores properly from the nested structure
        emotions = data.get("emotionPredictions", [{}])[0].get("emotion", {})

        # Format the extracted emotions
        relevant_emotions = {key: emotions.get(key, 0) for key in ['anger', 'disgust', 'fear', 'joy', 'sadness']}

        # Find the dominant emotion (highest score)
        dominant_emotion = max(relevant_emotions, key=relevant_emotions.get) if relevant_emotions else "unknown"

        # Modify the output format as required
        formatted_output = relevant_emotions
        formatted_output["dominant_emotion"] = dominant_emotion

        return formatted_output

    except requests.exceptions.RequestException as e:
        return {"error": f"API Request failed: {e}"}

    return response.text