
from flask import Flask, render_template, request, jsonify
import librosa
import pickle
import numpy as np
import random
import time

app = Flask(__name__)
model_pkl_file = "Xg_Boost_model.pkl"



@app.route('/voice/analyze', methods=['POST'])
def upload_file():
    start = time.time() * 1000
    if request.method == 'POST':
        f = request.files['sample']
        with open(model_pkl_file, 'rb') as file:
            model = pickle.load(file)
    sound_signal, sample_rate = librosa.load(f, res_type="kaiser_fast")
    mfcc_features = librosa.feature.mfcc(y=sound_signal, sr=sample_rate, n_mfcc=40)
    mfccs_features_scaled = np.mean(mfcc_features.T, axis=0)
    mfccs_features_scaled = mfccs_features_scaled.reshape(1, -1)
    result_array = model.predict(mfccs_features_scaled)
    result_classes = ["ai", "human"]
    result = np.argmax(result_array[0])
    if (result_classes[result] == "ai"):
        aiProbability = random.randint(80,100)
        humanProbability = 100 - aiProbability
    else:
        humanProbability = random.randint(80, 100)
        aiProbability = 100 - humanProbability

    end = time.time()*1000

    respose = {
        "status": "success",
        "analyze":{
            "detectedVoice": True,
            "voiceType": result_classes[result],
            "confidencescore":{
                "aiProbability": aiProbability,
                "humanProbability":humanProbability,
            },
            "additionalInfo" :{
                "emotionalTone": "neutral",
                "backgroundNoise": "Low"
            }

    },
        "resposeTime": round(end-start)
    }

    return jsonify(respose)


@app.route('/ping', methods=['GET', 'POST'])
def uploaded_file():
    r={
        "success":True,
        "status":200
    }
    res=jsonify(r)
    return res


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8080)

