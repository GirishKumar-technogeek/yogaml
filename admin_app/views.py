from django.shortcuts import render,redirect
from django.contrib import auth
from django.http import JsonResponse,HttpResponse
from django.conf import settings
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests,math,random,boto3
from accounts.models import *
from app.models import *
UserModel = get_user_model()

@login_required
def view_poses(request):
    poses = Pose.objects.filter(added_by=request.user).all()
    return render(request,'admin_app/view_poses.html',{'poses':poses})

@login_required
def add_pose(request):
    if request.method == "POST":
        pose_name = request.POST['pose_name']
        pose_description = request.POST['pose_description']
        pose_type = request.POST['pose_type']
        user_duration = request.POST['user_duration']
        img_url = request.POST['img_url']
        pose = Pose(added_by=request.user,pose_name=pose_name,pose_description=pose_description,pose_type=pose_type,user_duration=user_duration,img_url=img_url,
        nose_x = request.POST['nose_x'],
        nose_y = request.POST['nose_y'],
        leftear_x = request.POST['leftear_x'],
        leftear_y = request.POST['leftear_y'],
        rightear_x = request.POST['rightear_x'],
        rightear_y = request.POST['rightear_y'],
        lefteye_x = request.POST['lefteye_x'],
        lefteye_y = request.POST['lefteye_y'],
        righteye_x = request.POST['righteye_x'],
        righteye_y = request.POST['righteye_y'],
        leftshoulder_x = request.POST['leftshoulder_x'],
        leftshoulder_y = request.POST['leftshoulder_y'],
        rightshoulder_x = request.POST['rightshoulder_x'],
        rightshoulder_y = request.POST['rightshoulder_y'],
        leftelbow_x = request.POST['leftelbow_x'],
        leftelbow_y = request.POST['leftelbow_y'],
        rightelbow_x = request.POST['rightelbow_x'],
        rightelbow_y = request.POST['rightelbow_y'],
        leftwrist_x = request.POST['leftwrist_x'],
        leftwrist_y = request.POST['leftwrist_y'],
        rightwrist_x = request.POST['rightwrist_x'],
        rightwrist_y = request.POST['rightwrist_y'],
        lefthip_x = request.POST['lefthip_x'],
        lefthip_y = request.POST['lefthip_y'],
        righthip_x = request.POST['righthip_x'],
        righthip_y = request.POST['righthip_y'],
        leftknee_x = request.POST['leftknee_x'],
        leftknee_y = request.POST['leftknee_y'],
        rightknee_x = request.POST['rightknee_x'],
        rightknee_y = request.POST['rightknee_y'],
        leftankle_x = request.POST['leftankle_x'],
        leftankle_y = request.POST['leftankle_y'],
        rightankle_x = request.POST['rightankle_x'],
        rightankle_y = request.POST['rightankle_y'])
        pose.save()
        return redirect('admin_view_poses')
    else:
        return render(request,'admin_app/add_pose.html')