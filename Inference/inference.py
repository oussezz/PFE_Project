import time
from flask import Flask, request, jsonify
from PIL import Image
import io
import numpy as np

import base64
import os
from django.http import JsonResponse
from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from PIL import Image
import subprocess
import torch.nn.functional as F
# model_name_or_path = 'google/vit-base-patch16-224-in21k'#facebook/deit-base-patch16-224
model_name_or_path = 'facebook/deit-base-patch16-224'#google/vit-base-patch16-224-in21k
from transformers import ViTFeatureExtractor, ViTForImageClassification
import requests
feature_extractor = ViTFeatureExtractor.from_pretrained(model_name_or_path)
model = ViTForImageClassification.from_pretrained('model/')


app = Flask(__name__)


# Définition des classes


# Route pour le traitement d'image
@app.route('/predict', methods=['POST'])
def predict():
    # Récupérer l'image
    
    image_data = request.json['image']
    ip=request.json['ip']
    image_bytes = base64.b64decode(image_data)
    image=Image.open(io.BytesIO(image_bytes))
    inputs = feature_extractor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    probs = F.softmax(logits, dim=-1)
    probs = probs.detach().numpy().tolist()[0]
    result=model.config.id2label[predicted_class_idx]
    response = {'class': str(result), 'probabilities': probs[predicted_class_idx]}
    
    #write the response in a json file
    import json
    with open("C:/Users/Ezziane/FireDetectionTemp/"+str(ip)+".json", 'w') as f:
    # write dictionary to the file
        json.dump(response, f)
    print(response)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=4040)
