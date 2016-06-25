import cv2
from PIL import Image
import io


class Stream(object):

    # WE GET THE VIDEO OBJECT OF THE RTSP STREAM USING OPENCV VIDEOCAPTURE() FUNCTION
    def __init__(self):

        # self.frames = cv2.VideoCapture(c)
        self.frames = cv2.VideoCapture('rtsp://mm2.pcslab.com/mm/7m800.mp4')

        # FOR WEBCAM
        # self.frames = cv2.VideoCapture(0)

        # FOR VIDEO FILE
        # self.frames = cv2.VideoCapture('video.mp4')

    # TO GET EACH INDIVIDUAL FRAME WE USE THE READ() FUNCTION, CONVERTS THE FRAME INTO
    # BYTE ARRAY AND THE CONVERT & RETURN IT AS A BINARY STREAM
    def get_frame(self):
        ret, vid = self.frames.read()
        if ret:
            img = Image.fromarray(vid, 'RGB')
            output = io.BytesIO()
            img.save(output, format='JPEG')
            return output.getvalue()

        else:
            return b'0'
            # return Image.new('RGBA', (100, 100), (255,0,0,0))
