import torch
from PIL import Image
import cv2
from youtubeScan import cameraScan

def scanPeople():
    # 모델을 로드합니다.
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', force_reload=False)

    # 이미지를 로드합니다.
    cameraScan()
    img = cv2.imread('captured_frame.jpg')

    # 이미지를 모델에 전달하고 결과를 얻습니다.
    results = model(img)

    # 클래스 이름 목록을 가져옵니다.
    names = results.names

    # 결과 텐서에서 사람을 찾습니다.
    people = [x for x in results.xyxyn[0] if names[int(x[-1])] == 'person']

    # 감지된 사람들의 수를 출력합니다.
    print('Number of people detected:', len(people))

    return len(people)
