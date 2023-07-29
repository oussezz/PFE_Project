import threading
import cv2
from django.http import JsonResponse
from django.shortcuts import redirect, render
import numpy as np
import zmq
from django.contrib.admin.models import LogEntry
from .models import *
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from .models import Camera
from .models import *
from django.contrib.auth.hashers import make_password
from PIL import Image

streaming_serv = "127.0.0.1"
def streaming_server():
    return streaming_serv

def add_camera_utils(request):
        if request.method == "POST":
                try:
                    name = request.POST.get("cameraName")
                    address = request.POST.get("cameraIP")
                    # port = request.POST.get("port")
                    gps_position_x = request.POST.get("editcameraLatitude")
                    gps_position_y = request.POST.get("editcameraLongitude")
                    camera = Camera(name=name,ip=address,gps_position_x=gps_position_x,gps_position_y=gps_position_y)
                    camera.save()
                    LogEntry.objects.log_action(
                                user_id=request.user.id,
                                content_type_id=ContentType.objects.get_for_model(Camera).pk,
                                object_id=camera.id,
                                object_repr=request.user.username+" has added a camera named : "+camera.name,
                                action_flag=ADDITION)
                    return render(request, 'streaming_server_cameras_ajax.html', {'cameras': Camera.objects.all()})
                except:
                    return JsonResponse({'success': False}, status=404)
        else:
                return JsonResponse({'success': False}, status=404)

         
def delete_camera_utils(request,id):
    try:
        camera = Camera.objects.get(id=id)
        if camera:
            LogEntry.objects.log_action(
                                user_id=request.user.id,
                                content_type_id=ContentType.objects.get_for_model(Camera).pk,
                                object_id=camera.id,
                                object_repr=request.user.username+" has delete a camera named : "+camera.name,
                                action_flag=DELETION)
        camera.delete()
        return render(request, 'streaming_server_cameras_ajax.html', {'cameras': Camera.objects.all()})
    except:
        return JsonResponse({'success': False}, status=404)

def admins_utils(request, user):
        if request.method == 'POST':
                username = request.POST['username']
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                email = request.POST['email']
                password = request.POST['password']
                image = request.FILES['image']
                
                # Create a new User object with the submitted data
                user = User(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=make_password(password),
                is_staff=True,
                )
                user.save()
                LogEntry.objects.log_action(
                                user_id=request.user.id,
                                content_type_id=ContentType.objects.get_for_model(User).pk,
                                object_id=user.id,
                                object_repr=request.user.username+" has added an Admin named : "+user.username,
                                action_flag=ADDITION)
                Customuser=PlatformUser(user=user)
                Customuser.img=image
                Customuser.save()
                image=Image.open(image)
                image=image.resize((100,100))
                image.save("mediafiles/"+str(Customuser.img))
                return redirect('/admins')  # Or any other page you want to redirect the user to after successful submission
        admins=User.objects.all()
        return render(request,"admins.html",{'admins':admins,"user":user})
    
def users_utils(request, user):
        if request.method == 'POST':
                username = request.POST['username']
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                email = request.POST['email']
                password = request.POST['password']
                image = request.FILES['image']
                
                
                

                # Create a new User object with the submitted data
                user = User(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=make_password(password),
                is_staff=False,
                )
                user.save()
                LogEntry.objects.log_action(
                                user_id=request.user.id,
                                content_type_id=ContentType.objects.get_for_model(User).pk,
                                object_id=user.id,
                                object_repr=request.user.username+" has added a User named : "+user.username,
                                action_flag=ADDITION)
                Customuser=PlatformUser(user=user,img=image)
                Customuser.save()
                image=Image.open(image)
                image=image.resize((100,100))
                image.save("mediafiles/"+str(Customuser.img))

                return redirect('/users')  # Or any other page you want to redirect the user to after successful submission
        users=User.objects.all()
        return render(request,"users.html",{'users':users,"user":user})



def myaccount_utils(request,userr):
    if request.method == 'POST':
        # Get the user's information from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image = request.FILES.get('image')
        is_admin = request.POST.get('is_admin') == 'on'
        
        # Update the user's information
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if password:
        
            print(password)    
            user.set_password(password)
        if is_admin:
            user.is_staff = True
        else:
            user.is_staff = False
            
        # Save the new image file and update the user's image field
        if image:
            # Resize the image to 100x100 pixels
            
                platformUser=PlatformUser.objects.get(user=user)
                platformUser.img=image
                platformUser.save()
                image=Image.open(image)
                image=image.resize((100,100))
                image.save("mediafiles/"+str(platformUser.img))
            # Set the image field of the user to the new image name
            
        
        # Save the updated user information
        LogEntry.objects.log_action(
                                user_id=request.user.id,
                                content_type_id=ContentType.objects.get_for_model(User).pk,
                                object_id=user.id,
                                object_repr=request.user.username+" has changed his profile",
                                action_flag=CHANGE)
        user.save()
        
        # Show a success message
        
        # Redirect to the user's profile page
        return render(request,"myaccount.html",{"user":userr,'alert':True}) 
    
    # If the request method is GET, show the edit profile form
    return render(request,"myaccount.html",{"user":userr,'alert':False})      
      
        
def delete_user_utils(request,id):
    
        try:
                user=User.objects.get(id=id)
                boolean=user.is_staff
                if user:
                    LogEntry.objects.log_action(
                                user_id=request.user.id,
                                content_type_id=ContentType.objects.get_for_model(User).pk,
                                object_id=user.id,
                                object_repr=request.user.username+" has delete a user named : "+user.username,
                                action_flag=DELETION)
                    user.delete()
                platformUser=PlatformUser.objects.get(user=user)
                if platformUser:
                    platformUser.delete()
                if boolean:
                    return redirect('/admins')
                return redirect('/users')
        except:
               try:
                        platformUser=PlatformUser.objects.get(user=user)
                        if platformUser:
                                platformUser.delete()
                       
                        return redirect('/admins')
               except:
                      return redirect('/admins')       
                
                

import os

def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)



               
def cameras_thread(camera):
        port = int(str(camera.ip).split('.')[-1])+2000
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://"+str(streaming_server())+":"+str(port))
        print("tcp://"+str(streaming_server())+":"+str(port))
        socket.setsockopt_string(zmq.SUBSCRIBE, "")
        while True:
                # Receive a frame from the network
                msg = socket.recv()
                label, frame = msg.split(b" ", 1)
                label = label.decode("utf-8")
                frame_array = np.frombuffer(frame, dtype=np.uint8)# Decode the JPEG-encoded frame
                frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
                path="mediafiles/history/cameras/"+str(camera.ip)+"_"+str(camera.name)+"/temp/"
                create_path(path)
                cv2.imwrite(path+"/temp.jpg", frame)