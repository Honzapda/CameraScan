import cv2
import pafy
from decouple import config


def cameraScan():
    # pafy를 사용하여 동영상 정보 가져오기
    video = pafy.new(config('YOUTUBE_URL'))

    # 가장 높은 품질의 스트림 선택
    best_stream = video.getbest()

    # 비디오 캡처 객체 생성
    cap = cv2.VideoCapture(best_stream.url)

    frame_number = 0

    while True:
        # 비디오의 단일 프레임을 캡처
        ret, frame = cap.read()

        # 프레임이 올바르게 읽히면 출력
        if ret == True:
            # 사진 한 장만 캡처
            if frame_number == 0:
                cv2.imwrite('captured_frame.jpg', frame)
                break
            
            frame_number += 1

        else:
            break

    cap.release()
    cv2.destroyAllWindows()