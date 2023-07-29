import cv2
import imutils
import io
from imutils.video import VideoStream
import threading
import zmq
import cv2
import datetime
import base64
import os



# # model_name_or_path = 'google/vit-base-patch16-224-in21k'#facebook/deit-base-patch16-224
# model_name_or_path = 'facebook/deit-base-patch16-224'#google/vit-base-patch16-224-in21k
# from transformers import ViTFeatureExtractor, ViTForImageClassification
# import requests
# feature_extractor = ViTFeatureExtractor.from_pretrained(model_name_or_path)
# model = ViTForImageClassification.from_pretrained('model/')


import requests
import json
import base64

socket=[]

endpoint_url = 'http://localhost:4040/predict'

class StreamThread:
    def stream(self,stop_event,add):
            global socket
            prediction = "No_Fire"
            i=0
            port = int(add.split('.')[-1])+2000
            print(f'port: {port}')
            if not socket:
                context = zmq.Context()
                socket = context.socket(zmq.PUB)
                socket.bind("tcp://*:"+str(port))
            video_stream = cv2.VideoCapture('http://'+str(add)+':8080/video')
            print(f'streaming...http://'+str(add)+':8080/video')
            while not stop_event.is_set():
                rep,frame = video_stream.read()
                if frame is None:
                    continue
                # Convert the frame to a byte string
               
                # predicted_class = response_json['class']
                # probabilities = response_json['probabilities']
                
                # # Show the predicted class and probabilities on the frame
                # cv2.putText(frame, f'Class: {predicted_class}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                # cv2.putText(frame, f'Probabilities: {probabilities}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                result = prediction
                now = datetime.datetime.now()

                # Get the seconds of the current time
                seconds = now.time().second

                # Check if the seconds are even
                def send_request(img):
                    _, image_bytes = cv2.imencode('.jpg', img)
                    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                    
                    # Set the data for the request
                    data = {'image': image_base64,  'ip': str(add)}
                    
                    # Send the POST request
                    requests.post(endpoint_url, json=data,stream=True)
                    
                    
                i+=1
                if i % 60 == 0:
                    threading.Thread(target=send_request,args=(frame,)).start()
                    i=0
                    
                #open the json file
                try:
                    if os.path.isfile("C:/Users/Ezziane/FireDetectionTemp/"+str(add)+".json"):
                        with open("C:/Users/Ezziane/FireDetectionTemp/"+str(add)+".json", 'r') as f:
                            data = json.load(f)
                        class_label = data['class']
                        probability = data['probabilities']

                        # Write the class label and probability on the image
                        cv2.putText(frame, f"Class: {class_label}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                        cv2.putText(frame, f"Prob: {probability:.2f}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                except:
                    print("error")
                # Get the current date and time
                now = datetime.datetime.now()
                date_str = now.strftime("%Y-%m-%d")
                time_str = now.strftime("%H:%M:%S")

                # Set the font and font scale
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.8

                # Set the text and text position
                text = f"{date_str} {time_str}"
                text_pos = (frame.shape[1] - 300, 20)

                # Set the text color, thickness, and line type
                text_color = (255, 255, 255)
                text_thickness = 2
                line_type = cv2.LINE_AA

                # Draw the text on the frame
                cv2.putText(frame, text, text_pos, font, font_scale, text_color, text_thickness, line_type)


                # # Set the camera name and text position
                # camera_name = result
                # camera_pos = (10, 20)

                # # Set the camera name color, thickness, and line type
                # camera_color = (0, 255, 0)
                # camera_thickness = 1
                # line_type = cv2.LINE_AA

                # # Draw the camera name on the frame
                # cv2.putText(frame, camera_name, camera_pos, font, font_scale, camera_color, text_thickness, line_type)


                frame = cv2.resize(frame,(720,480))
                path="..FDPlatform/mediafiles/history/cameras/"+str(add)
                #create path of not exist
                if not os.path.exists(path):
                    os.makedirs(path)
                #save the image with time in name
                print(path+str(f"/{date_str} {time_str}")+".jpg")
                cv2.imwrite(path+str(f"/{date_str} {time_str}")+".jpg", frame)


                frame= cv2.imencode(".jpg", frame)[1].tobytes()
                label = f'{add}'.encode('utf-8')
                message= label + b' ' + frame   
                # msg=[str(add),frame]
                socket.send(message)
            video_stream.release()
            cv2.destroyAllWindows()
    def __init__(self,add,inference_server):
        self.add=str(add)
        self.stop_event = threading.Event()
        self.thread=threading.Thread(target=self.stream,args=(self.stop_event,add,))
        self.thread.start()
        self.inference_server=inference_server
        
        
        