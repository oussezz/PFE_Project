import datetime
import json
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.admin.models import LogEntry
from .models import *
from .utils import *
from .VideoCamera import VideoCamera, gen
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
thread_list = []
#impor the login_required decorator
from django.contrib.auth.decorators import login_required
streaming_serv=streaming_server()
def get_user(request):
        return PlatformUser.objects.get(user=request.user)

@login_required(login_url='login')
def home(request):
        if request.user.is_staff:
                return redirect("stats")
        else:
                return redirect("clientcameras")
@login_required(login_url='login')
def streaming_server_cameras(request):
        camera=None
        users=User.objects.filter(is_staff=False)
        if request.method == "POST":
                id=request.POST.get("editcameraID")
                name=request.POST.get("editcameraName")
                ip=request.POST.get("editcameraIP")
                camera=Camera.objects.get(id=id)
                camera.name=name
                camera.ip=ip
                for i in users:
                        if str(i.id) in request.POST:
                                camera.viewers.add(i.id)
                        else:
                                camera.viewers.remove(i.id)
                camera.save()
                
                LogEntry.objects.log_action(
                                user_id=request.user.id,
                                content_type_id=ContentType.objects.get_for_model(Camera).pk,
                                object_id=camera.id,
                                object_repr=request.user.username+" has changed a camera named : "+camera.name,
                                action_flag=CHANGE)
                return render(request, 'streaming_server_cameras_ajax.html', {'cameras': Camera.objects.all(),"users":users})
        cameras = Camera.objects.all()
        
        return render(request,"streaming_server_cameras.html",{"cameras":cameras,"streaming_server":streaming_serv,"user":get_user(request),"users":users})
@login_required(login_url='login')
def add_camera(request):
        return add_camera_utils(request)
@login_required(login_url='login')
def delete_camera(request,id):
        return delete_camera_utils(request,id)

@login_required(login_url='login')
@gzip.gzip_page
def live_camera(request,id):
    try:
        ip=Camera.objects.get(id=id).ip
        cam = VideoCamera(ip)
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass
@login_required(login_url='login')
def view_camera(request,id):
        camera = Camera.objects.get(id=id)
        return render(request,"view_camera.html",{'camera':camera,'streaming_server':streaming_serv,"user":get_user(request)})
@login_required(login_url='login')
def activate_camera(request):
        try:
                id=request.GET.get("data")
                camera = Camera.objects.get(id=id)
                import requests
                if(not camera.status):
                        url='http://127.0.0.1:5000/config/start_stream/'+str(camera.ip)
                        response = requests.get(url)

                        # Check the response status code
                        if response.status_code == 200:
                        # Request was successful, print the response content
                                print(response.content)
                        else:
                        # Request failed, print the status code and reason
                                print(response.status_code, response.reason)
                else:
                        url='http://127.0.0.1:5000/config/stop_stream/'+str(camera.ip)
                        response = requests.get(url)

                        # Check the response status code
                        if response.status_code == 200:
                        # Request was successful, print the response content
                                print(response.content)
                        else:
                        # Request failed, print the status code and reason
                                print(response.status_code, response.reason)
                camera.status = not camera.status
                camera.save()
                
                # thread=threading.Thread(target=cameras_thread, args=(camera,))
                # thread.start()
                # thread_list.append(thread)
                # print("ok")
                return render(request, 'streaming_server_cameras_ajax.html', {'cameras': Camera.objects.all()})
        
        except:
                return render(request, 'streaming_server_cameras_ajax.html', {'cameras': Camera.objects.all()})


        
@login_required(login_url='login')
def admins(request):
        return admins_utils(request, get_user(request))
@login_required(login_url='login')
def users(request):
        return  users_utils(request, get_user(request))   
@login_required(login_url='login')
def delete_user(request,id):
        return delete_user_utils(request, id)       
                


def live_camera_ajax(request,id):
        camera = Camera.objects.get(id=id)
        return render(request, 'live_camera_ajax.html', {'camera': camera,'streaming_server':streaming_serv,"user":get_user(request)})


@login_required(login_url='login')
def myaccount(request):
    return myaccount_utils(request, get_user(request))  
      
        
def firedetection(request):
        return render(request,"firedetection.html",{"user":get_user(request)})
        
def stop_thread(request):
        print("stop")
        return JsonResponse({'success': True}, status=200)
def map(request):
        Cameras=Camera.objects.all()
        return render(request,"map.html",{"user":get_user(request),"cameras":Cameras})


def stop(request):
        return render(request,"stop.html")

def history(request):
        cameras = Camera.objects.all()
        
        return render(request,"history.html",{"user":get_user(request),"cameras":cameras,})

#import settings

def cam_history(request,id):
        camera = Camera.objects.get(id=id)
        video_dir = "mediafiles/history/cameras/"+str(camera.ip)
        if not os.path.exists(video_dir):
                os.makedirs(video_dir)
        # Liste des noms de fichiers des vidéos
        video_files = os.listdir(video_dir)

        # Ajouter le chemin complet du fichier vidéo pour chaque vidéo
        video_paths = [os.path.join('history', f) for f in video_files]
        print(video_paths)
        video_data = []
        for f in video_files:
                file_path = os.path.join(video_dir, f)
                statinfo = os.stat(file_path)
                creation_time = datetime.datetime.fromtimestamp(statinfo.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
                size_in_mb = round(statinfo.st_size / 1024 / 1024, 2)
                video_data.append({
                'name': os.path.basename(f),
                'creation_time': creation_time,
                'size': size_in_mb,
                'permissions': oct(statinfo.st_mode)[-3:],
                'url': os.path.join('/media/history/cameras/{}'.format(camera.ip), f)
                })
        return render(request,"cam_history.html",{"user":get_user(request),"video_paths":video_paths,"camera":camera,"video_name":video_data,"video_data":video_data})


def reports(request):
        with open("C:/Users/Ezziane/FireDetectionTemp/notif/notif.json", 'r') as f:
        # write dictionary to the file
            data = json.load(f)
        notifications = data['notifications']
        notifications_new=False
        for notification in notifications:
                from datetime import datetime
                date_str = notification['date']
                date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
                notification['date'] = datetime.strftime(date_obj, '%A %d %B %Y at %H:%M:%S')
                path = notification['path']
                parent_dir = os.path.basename(os.path.dirname(path))
                cam_ip = parent_dir
                notification['cam_ip'] = cam_ip
                if notification['status'] == 'unread':
                        notifications_new=True

        
        return render(request,"reports.html",{"user":get_user(request),"notifications":notifications,"notifications_new":notifications_new})

def stats(request):
        import os
from django.conf import settings
from django.shortcuts import render


from django.conf import settings
from django.shortcuts import render

def stats(request):
    data = []
    cameras = Camera.objects.all()
    for camera in cameras:
        camera_folder = os.path.join(settings.MEDIA_ROOT, 'history', 'cameras', camera.ip)
        if not os.path.exists(camera_folder):
            os.makedirs(camera_folder)
        total_size = 0
        for filename in os.listdir(camera_folder):
            file_path = os.path.join(camera_folder, filename)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
        total_size_mb = total_size / (1024 * 1024) # convert bytes to megabytes
        data.append({'camera': camera.name, 'size': total_size_mb})
    visits=Visits.objects.all()
    return render(request, 'stats.html', {'user': get_user(request), 'data': data,'visits':visits})



def logs(request):
        list=LogEntry.objects.all()
        
        return render(request,"logs.html",{"user":get_user(request),"list":list})

def update_notifications(request):
    with open("C:/Users/Ezziane/FireDetectionTemp/notif/notif.json", 'r') as f:
        data = json.load(f)
    notifications = data['notifications']
    notifications_new = False
    for notification in notifications:
        from datetime import datetime
        date_str = notification['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
        notification['date'] = datetime.strftime(date_obj, '%A %d %B %Y at %H:%M:%S')
        path = notification['path']
        parent_dir = os.path.basename(os.path.dirname(path))
        cam_ip = parent_dir
        notification['cam_ip'] = cam_ip
        if notification['status'] == 'unread':
            notifications_new = True

    # reverse the order of notifications based on their id
    notifications = sorted(notifications, key=lambda x: x['id'], reverse=True)

    response = render(request, "update_notif.html", {"notifications": notifications, "notifications_new": notifications_new})
    return response




def clientcameras(request):
        #get all the cameras that the users is in their viewers 
        cameras=Camera.objects.filter(viewers=request.user.id)
        return render(request,"clientcameras.html",{"user":get_user(request),"cameras":cameras})
        
def view_video(request,ip,name):
        video_name="/media/history/cameras/"+str(ip)+"/"+str(name)
        
        return render(request,"view_video.html",{"user":get_user(request),"video_name":video_name})
def mark_notification_as_read(request,id):
        #delete a file 
        
                
        notification_id = id
        print(id)
        if notification_id is not None:
            # Load the notification JSON file
            with open("C:/Users/Ezziane/FireDetectionTemp/notif/notif.json", 'r') as f:
                notifications = json.load(f)
            # Find the notification with the given ID and mark it as read
            cam_ip=None    
            for notification in notifications['notifications']:
                if notification['id'] == str(notification_id):
                    import os

                    path = notification['path']
                    parent_dir = os.path.basename(os.path.dirname(path))
                    cam_ip = parent_dir    
                    notification['status'] = 'read'
                    break
        
            if os.path.isfile("C:/Users/Ezziane/FireDetectionTemp/should_create_a_report_"+str(cam_ip)+".json"):
                os.remove("C:/Users/Ezziane/FireDetectionTemp/should_create_a_report_"+str(cam_ip)+".json")    
            # Save the updated JSON file
            with open("C:/Users/Ezziane/FireDetectionTemp/notif/notif.json", 'w') as f:
                json.dump(notifications, f)
        #     print(notifications)    
            # Return a JSON response with status "success"
            return JsonResponse({'status': 'success'})