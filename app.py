from flask import Flask, request, jsonify, render_template, Response
import cv2
import base64
import sys, json, requests
import torch
import numpy as np
import os
import io
import PIL.Image as Image
import uuid
import time
import random
from dotenv import load_dotenv

load_dotenv()

application = Flask(__name__)

application.static_folder = 'static'  # 사용할 정적 파일 폴더 경로

youtube_link=""

@application.route("/webhook/", methods=["POST"])
def webhook():
    request_data = request.json
    print("req_data",request_data)
    global youtube_link
    bot_res = request_data['result']['choices'][0]['message']['content']
    bot_res += youtube_link
    call_back = requests.post(request_data['callback_url'], json={
        "version": "2.0", "template": { "outputs": [{
            "simpleText": {"text": bot_res}
        }]}})
    print(call_back.status_code, call_back.json())
    return 'OK'

@application.route("/question", methods=["POST"])
def call_openai_api():
    user_request = request.json.get('userRequest', {})
    print("user req", user_request)
    
    global youtube_link
    link = get_youtube_url(user_request["utterance"])

    if (link):
        youtube_link=f"\n\n👇영상으로 사용법 보러가기\n{link}"
    else:
        youtube_link = ""
        
    messages = []
    messages.append({'role':'system', 'content':'너는 디지털취약계층을 위한 디지털 전문가 비서처럼 행동할거야. 1, 2, 3 이런식으로 넘버링해서 존댓말로 공손하게 최대한 자세히 대답해줘. 500자 이내로. '})
    messages.append({"role": "user", "content": user_request.get('utterance', '')})
    callback_url = user_request.get('callbackUrl')
    openai=os.getenv("OPENAI")
    asyncia=os.getenv("ASYNCIA")
    try:  # Asyncia 서비스 이용 - http://asyncia.com/
        api = requests.post('https://api.asyncia.com/v1/api/request/', json={
            "apikey": openai,
            "messages" :messages,
            "userdata": [["callback_url", callback_url]]},
            headers={"apikey":asyncia}, timeout=2)
        print("==========")
        print(api)
    except requests.exceptions.ReadTimeout:
        pass
    return jsonify({
      "version" : "2.0",
      "useCallback" : True
    })
    


def get_youtube_url(question): 
    question = question.replace(" ","")
    question = question.lower()
    youtube_data = []
    with open('youtube_data.json', 'r', encoding="utf-8") as file:
        youtube_data = json.load(file)
        
    urls = []
    for content in youtube_data:
        keywords = content["keywords"]
        for keyword in keywords:
            keyword = keyword.replace(" ","")
            keyword = keyword.lower()
            if keyword in question:
                
                key = keyword+str(content["id"])
                urls.append(content["url"])

                break
    if len(urls) > 0:
        url = random.sample(urls, 1)[0]
    else:
        url = ""
    return url

# camera = cv2.VideoCapture(0)

model = torch.hub.load('./yolov5', 'custom', './yolov5/engine/paik.pt', source='local')


@application.route('/test', methods=['POST'])
def test():
    infer = cv2.imread('./test.png')
    inference(infer)
    return "ok"

@application.route('/version', methods=['GET'])
def api_test():
    return {"version":"v1.0"}
    
    
def inference(frame):
    # print('Inference start')
    start_time = time.time()
    inference_results = model(frame, size=640)  # model inference result
    inference_results.render()
    end_time = time.time()
    execution_time = end_time - start_time

    # print('Inference end')
    # print(f"My function took {execution_time} seconds to execute.")
    # print(inference_results)
    return inference_results.imgs[0]


def generate_frames(video_frame):
    inference_frame = inference(video_frame)
    ret, buffer = cv2.imencode('.jpg', inference_frame)
    dst_frame = buffer.tobytes()
    yield (base64.b64encode(dst_frame))


    
@application.route('/')
def index():
    return render_template('index.html')

@application.route('/video_feed',methods=['GET', 'POST'])
def video_feed():
    # print("video feed start")
    #frame_data = request.get_data()
    req_data = request.get_json()
    frame_data = req_data['frame_data']
    # Base64로 인코딩된 이미지 데이터를 디코딩합니다.
    decoded_data = base64.b64decode(frame_data)
    
    # 이미지 데이터를 NumPy 배열로 변환합니다.
    np_data = np.frombuffer(decoded_data, dtype=np.uint8)

    # NumPy 배열을 OpenCV의 Mat 형식으로 변환합니다.
    mat_data = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        
    return Response(generate_frames(mat_data), mimetype='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    application.run(host='0.0.0.0', port=80)