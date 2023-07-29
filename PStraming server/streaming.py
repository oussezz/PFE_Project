import json
from flask import Flask, jsonify, render_template
from StreamThread import StreamThread

thread_list = []
inference_server = '192.168.114.1'
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',message='Welcome to our streaming server')

@app.route('/onlinecamerasjson')
def onlinecamerasjson():
    onlinecameras=[]
    x=0
    for i in thread_list:
        onlinecameras.append((x,str(i.add)))
        x+=1
    onlinecameras=dict(onlinecameras)
    print(onlinecameras)
    with open('onlinecameras.json', 'w') as outfile:
        json.dump(onlinecameras, outfile)
    return jsonify(onlinecameras)

@app.route('/onlinecameras')
def onlinecameras():
    onlinecameras=[]
    for i in thread_list:
        print(str(i.add))
        onlinecameras.append(str(i.add))
    print(onlinecameras)
    return render_template('onlinecameras.html',onlinecameras=onlinecameras)
    

@app.route('/config/start_stream/<add>')
def start_stream(add):
    for i in thread_list:
        if(i.add==add):
            return 'Stream already exist'
    
    streamThread=StreamThread(add=add,inference_server=inference_server)
    thread_list.append(streamThread)
    return (f'Stream {add} started')

@app.route('/config/stop_stream/<add>')
def stop_stream(add):
    for i in thread_list:
        if(i.add==add):
            i.stop_event.set()
            thread_list.remove(i)
            return (f'Stream {add} stopped')
    return (f'Stream {add} not found')

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="5000",threaded=True)





