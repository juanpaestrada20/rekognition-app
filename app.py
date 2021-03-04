from flask import Flask, request, jsonify
import boto3
from botocore.client import Config
import base64

import json

app = Flask(__name__)

with open('keys.json') as json_file:
    data = json.load(json_file)


def getRekognition():
    rekognition = boto3.client(
        'rekognition',
        region_name=data['rekognition']['region'],
        aws_access_key_id=data['rekognition']['accessKeyId'],
        aws_secret_access_key=data['rekognition']['secretAccessKey'],
    )
    return rekognition


rek = getRekognition()


@app.route('/tarea3-201800709')
def rekognition():
    image = json.loads(request.data)['image']
    bytesImage = base64.b64decode(image)
    res = rek.detect_labels(
        Image={'Bytes': bytesImage},
        MaxLabels=15)
    result = {
        'status': 200,
        'image': res
    }
    response = {
        'result': result['image']['Labels']
    }
    return jsonify(response), result['status'], {'Content-Type': 'application/json'}
