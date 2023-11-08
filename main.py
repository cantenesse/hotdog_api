import io
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
from keras.preprocessing import image
import tensorflow as tf
import numpy as np
import boto3

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_model_from_s3():
    s3 = boto3.client("s3")
    bucket_name = "hotdognothotdogmodel"
    s3_file_path = "model_inception_resnet_v2.h5"
    local_file_path = "model_inception_resnet_v2.h5"
    s3.download_file(bucket_name, s3_file_path, local_file_path)
    model = load_model("model_inception_resnet_v2.h5")

    return model


def load_image(image_file):
    img_width, img_height = 256, 256
    img = image.load_img(image_file, target_size=(img_width, img_height))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)

    return img


def predict_hotdog(file):
    img = load_image(file)
    prediction = model.predict(img).flatten()
    prediction = tf.nn.sigmoid(prediction)
    prediction = tf.where(prediction <= 0.5, 0, 1)
    if (prediction.numpy()[0]) == 0:
        is_hot_dog = True
    else:
        is_hot_dog = False

    return is_hot_dog


@app.post("/hotdog/")
async def hotdog_endpoint(file: UploadFile = File(...)):
    file_contents = await file.read()
    file_like = io.BytesIO(file_contents)
    is_hot_dog = predict_hotdog(file_like)
    return {"hotdog": is_hot_dog}


@app.get("/")
async def get_endpoint():
    return {"status": True}


model = get_model_from_s3()
