from django.shortcuts import render
from django.http import HttpResponse
from .models import *

from collections import defaultdict
from io import TextIOWrapper
import io
from .forms import *
from django.contrib import messages
from django.shortcuts import render, HttpResponse
from django_pandas.io import read_frame
import csv
import pandas as pd 
import numpy as np 
import os
import joblib

def adminlogin1(request):
    return render(request, "adminlogin.html")

def adminloginentered(request):
    if request.method == 'POST':
        uname=request.POST['uname']
        passwd=request.POST['upasswd']
        if uname =='admin' and passwd =='admin':
            return render(request,"adminloginentered.html")
        else:
            return HttpResponse("invalied credentials")
    return render(request, "adminloginentered.html")

def userdetails(request):
    qs=userModel.objects.all()
    return render(request,"userdetails.html",{"qs":qs})

def activateuser(request):
    if request.method =='GET':
        uname=request.GET.get('pid')
        print(uname)
        status='Activated'
        print("pid=",uname,"status=",status)
        userModel.objects.filter(id=uname).update(status=status)
        qs=userModel.objects.all()
        return render(request,"userdetails.html",{"qs":qs})

# Create your views here.
def index(request):
    return render(request,'index.html')

def logout(request):
    return render(request, "index.html")

def userlogin(request):
    return render(request,'userlogin.html')

def userregister(request):
    if request.method=='POST':
        form1=userForm(request.POST)
        if form1.is_valid():
            form1.save()
            print("succesfully saved the data")
            return render(request, "userlogin.html")
        else:
            print("form not valied")
            return HttpResponse("form not valid")
    else:
        form=userForm()
        return render(request,"userregister.html",{"form":form})

def userlogincheck(request):
    if request.method == 'POST':
        sname = request.POST['email']
        print(sname)
        spasswd = request.POST['upasswd']
        print(spasswd)
        try:
            check = userModel.objects.get(email=sname,passwd=spasswd)
            print(check)
            status = check.status
            print('status',status)
            if status == "Activated":
                request.session['email'] = check.email
                return render(request, 'userpage.html')
            else:
                messages.success(request,'user is not activated')
                return render(request, 'userlogin.html')
        except Exception as e:
            print('Exception is ',str(e))
            pass
        messages.success(request,'Invalid name and password')
        return render(request,'userlogin.html')

path1 = r"C:/Users/Rohith/Downloads/Final Project/Final Project/3_Frustation detection/Frustraion_UI/Frustraion/dnn/tfidf.pkl"
assert os.path.isfile(path1)
with open(path1, "rb") as f1:
    tfidf = joblib.load(f1)

path2 = r"C:/Users/Rohith/Downloads/Final Project/Final Project/3_Frustation detection/Frustraion_UI/Frustraion/dnn/nb_model.sav"
assert os.path.isfile(path2)
with open(path2, "rb") as f2:
    model = joblib.load(f2)

data_img = []

def checkspam(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        #example = np.zeros(100)
        example =[str(message)]
        print(example)
        enc = tfidf.transform(example)
        score = model.predict(enc)
        print(score)  
        preds = np.round(abs(score))
        cluster_name=['Frusted', 'Not Frusted']
        prediction=cluster_name[int(preds)]
        return render(request, 'spamreport.html', {"object": prediction})
    return render(request, 'spaminput.html')
        
def adddata(request):
    return render(request,'spaminput.html')








