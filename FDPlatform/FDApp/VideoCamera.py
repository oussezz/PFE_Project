import threading
import cv2
import numpy as np
import zmq
from .utils import streaming_server

class VideoCamera(object):
    def __init__(self,add):
        self.add = add
        self.frame = cv2.imread("mediafiles/loading.jpg")
        self.video = None
        threading.Thread(target=self.update, args=()).start()
        
    
    def update(self):
                # port = int(str(self.add).split('.')[-1])+2000
                port = 2000
                self.context = zmq.Context()
                self.socket = self.context.socket(zmq.SUB)
                self.socket.connect("tcp://"+str(streaming_server())+":"+str(port))
                print("tcp://"+str(streaming_server())+":"+str(port))
                self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
                while True:
                        # print("Thread ID:", threading.get_ident())

                        # Receive a frame from the network
                        msg = self.socket.recv()
                        label, frame = msg.split(b" ", 1)
                        
                        label = label.decode("utf-8")
                        # send the image to the infernece server to check if there is a fire or not
                        if label==str(self.add):
                            frame_array = np.frombuffer(frame, dtype=np.uint8)# Decode the JPEG-encoded frame
                            frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
                            (self.grabbed, self.frame) = label, frame
                        
                
              

    def get_frame(self):
        image = self.frame
        if image is not None:
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()
        
    
    def __del__(self):
                self.socket.close()   
                



def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame:
                yield(b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')