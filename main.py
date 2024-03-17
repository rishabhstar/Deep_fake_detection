
from flask import Flask, render_template, request, jsonify
import librosa
import pickle
import numpy as np

app = Flask(__name__)
model_pkl_file = "Xg_Boost_model.pkl"



@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        with open(model_pkl_file, 'rb') as file:
            model = pickle.load(file)
    sound_signal, sample_rate = librosa.load(f, res_type="kaiser_fast")
    mfcc_features = librosa.feature.mfcc(y=sound_signal, sr=sample_rate, n_mfcc=40)
    mfccs_features_scaled = np.mean(mfcc_features.T, axis=0)
    mfccs_features_scaled = mfccs_features_scaled.reshape(1, -1)
    result_array = model.predict(mfccs_features_scaled)
    print(result_array)
    result_classes = ["FAKE", "REAL"]
    result = np.argmax(result_array[0])
    print("Result:", result_classes[result])

    return result_classes[result]


@app.route('/uploader', methods=['GET', 'POST'])
def uploaded_file():
    print("inside")
    return "Ok"


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=5555)