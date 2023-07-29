import numpy as np
import onnxruntime as ort
from PIL import Image
import cv2

# create session and get input/output names
session = ort.InferenceSession("model.onnx")
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

# set up video capture
cap = cv2.VideoCapture(0)

# loop over frames from the video stream
while True:
    # read frame from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # resize frame and convert to numpy array
    img = cv2.resize(frame, (224, 224))
    img = np.asarray(img)

    # convert from HWC to CHW format
    img = np.transpose(img, (2, 0, 1))

    # add batch dimension and convert to float32
    img = np.expand_dims(img, axis=0).astype('float32')

    # run inference
    outputs = session.run([output_name], {input_name: img})

    # get the predicted class
    predicted_class = np.argmax(outputs[0][0])

    # display the predicted class on the image
    cv2.putText(frame, f"Class: {predicted_class}", (20, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # display the image
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# cleanup
cap.release()
cv2.destroyAllWindows()
