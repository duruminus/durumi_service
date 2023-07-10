import os
import errno
import base64
import io
from PIL import Image

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Failed to create directory!!!!!")
            raise

def imageConvert(img):
    img = base64.b64decode(img)
    img = io.BytesIO(img)
    img = Image.open(img)
    return img