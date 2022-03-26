import numpy as np
from math import sqrt
from django.shortcuts import render,redirect
from django.contrib import auth
from django.http import JsonResponse,HttpResponse
from django.conf import settings
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import requests,math,random,boto3
from accounts.models import *
from .models import *
UserModel = get_user_model()

@login_required
def view_profile(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    return render(request,'app/view_profile.html',{'profile':profile})

@login_required
def add_profile(request):
    if request.method == "POST":
        full_name = request.POST['full_name']
        age = request.POST['age']
        gender = request.POST['gender']
        height = request.POST['height']
        weight = request.POST['weight']
        bmi = request.POST['bmi']
        UserProfile(user=request.user,full_name=full_name,age=age,gender=gender,height=height,weight=weight,bmi=bmi).save()
        return redirect('view_profile')
    else:
        return render(request,'app/add_profile.html')

@login_required
def search_poses(request):
    if request.method == "POST":
        search = request.POST['search']
        pose = Pose.objects.filter(pose_name=search).first()
        return redirect('view_pose',pk=pose.pk)

@login_required
def view_poses(request):
    poses = Pose.objects.all()[0:5]
    return render(request,'app/view_poses.html',{'poses':poses})

@login_required
def view_pose(request,pk):
    pose = Pose.objects.filter(pk=pk).first()
    return render(request,'app/view_pose.html',{'pose':pose})

@csrf_exempt
def score_user(request,pk):
    cosine_similarities = []
    refpose = Pose.objects.filter(pk=pk).first()
    refarr = [refpose.nose_x,refpose.nose_y,refpose.leftear_x,refpose.leftear_y,refpose.rightear_x,refpose.rightear_y,refpose.lefteye_x,refpose.lefteye_y,refpose.righteye_x,refpose.righteye_y,refpose.leftshoulder_x,refpose.leftshoulder_y,refpose.rightshoulder_x,refpose.rightshoulder_y,refpose.leftelbow_x,refpose.leftelbow_y,refpose.rightelbow_x,refpose.rightelbow_y,refpose.leftwrist_x,refpose.leftwrist_y,refpose.rightwrist_x,refpose.rightwrist_y,refpose.lefthip_x,refpose.lefthip_y,refpose.righthip_x,refpose.righthip_y,refpose.leftknee_x,refpose.leftknee_y,refpose.rightknee_x,refpose.rightknee_y,refpose.leftankle_x,refpose.leftankle_y,refpose.rightankle_x,refpose.rightankle_y]
    data = request.POST
    for i in range(0,int(data["length"])):
        userarr=[]
        userarr.append(data["arr["+str(i)+"][nose][x]"])
        userarr.append(data["arr["+str(i)+"][nose][y]"])
        userarr.append(data["arr["+str(i)+"][leftEar][x]"])
        userarr.append(data["arr["+str(i)+"][leftEar][y]"])
        userarr.append(data["arr["+str(i)+"][rightEar][x]"])
        userarr.append(data["arr["+str(i)+"][rightEar][y]"])
        userarr.append(data["arr["+str(i)+"][leftEye][x]"])
        userarr.append(data["arr["+str(i)+"][leftEye][y]"])
        userarr.append(data["arr["+str(i)+"][rightEye][x]"])
        userarr.append(data["arr["+str(i)+"][rightEye][y]"])
        userarr.append(data["arr["+str(i)+"][leftShoulder][x]"])
        userarr.append(data["arr["+str(i)+"][leftShoulder][y]"])
        userarr.append(data["arr["+str(i)+"][rightShoulder][x]"])
        userarr.append(data["arr["+str(i)+"][rightShoulder][y]"])
        userarr.append(data["arr["+str(i)+"][leftElbow][x]"])
        userarr.append(data["arr["+str(i)+"][leftElbow][y]"])
        userarr.append(data["arr["+str(i)+"][rightElbow][x]"])
        userarr.append(data["arr["+str(i)+"][rightElbow][y]"])
        userarr.append(data["arr["+str(i)+"][leftWrist][x]"])
        userarr.append(data["arr["+str(i)+"][leftWrist][y]"])
        userarr.append(data["arr["+str(i)+"][rightWrist][x]"])
        userarr.append(data["arr["+str(i)+"][rightWrist][y]"])
        userarr.append(data["arr["+str(i)+"][leftHip][x]"])
        userarr.append(data["arr["+str(i)+"][leftHip][y]"])
        userarr.append(data["arr["+str(i)+"][rightHip][x]"])
        userarr.append(data["arr["+str(i)+"][rightHip][y]"])
        userarr.append(data["arr["+str(i)+"][leftKnee][x]"])
        userarr.append(data["arr["+str(i)+"][leftKnee][y]"])
        userarr.append(data["arr["+str(i)+"][rightKnee][x]"])
        userarr.append(data["arr["+str(i)+"][rightKnee][y]"])
        userarr.append(data["arr["+str(i)+"][leftAnkle][x]"])
        userarr.append(data["arr["+str(i)+"][leftAnkle][y]"])
        userarr.append(data["arr["+str(i)+"][rightAnkle][x]"])
        userarr.append(data["arr["+str(i)+"][rightAnkle][y]"])
        A=np.array(refarr,dtype=float)
        B=np.array(userarr,dtype=float)
        cos_sim=np.dot(A,B)/(np.linalg.norm(A)*np.linalg.norm(B))
        cosine_similarities.append(cos_sim)
    print(sum(cosine_similarities)/len(cosine_similarities))
    euclid_dist = sqrt(2*(1-sum(cosine_similarities)/len(cosine_similarities)))
    if(euclid_dist<0.21):
        score = 100
    else:
        score = (1-euclid_dist)*100
    
    UserPose(pose=refpose,user=UserProfile.objects.filter(user=request.user).first(),points_earned=score).save()
    return redirect('my_progress')
@login_required
def my_progress(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    userposes = UserPose.objects.filter(user=profile).all()
    return render(request,'app/my_progress.html',{'userposes':userposes})

@login_required
def leaderboard(request):
    userposes = UserPose.objects.all().order_by('-points_earned')
    return render(request,'app/leaderboard.html',{'userposes':userposes})