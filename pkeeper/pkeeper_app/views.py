from django.shortcuts import render
import threading
import json
import requests
from django.core import serializers
from .models import *
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.db.models import Count
from django.views.decorators.cache import never_cache
from django.core.files.storage import FileSystemStorage
import os
from datetime import date
from datetime import datetime
import re
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from .checks import *
from datetime import datetime,timedelta
from blockchain import *
import ipfshttpclient
# Create your views here.

@never_cache
def display_login(request):
	return render(request, "login_register.html", {})

@never_cache
def check_login(request):
	username = request.POST.get("name")
	password = request.POST.get("pass")
	# print(username)
	# print(password)

	if username == "admin" and password == "admin":
		request.session['uid'] = "admin"
		return HttpResponse("<script>alert('Login Successful');window.location.href='/show_home_admin/';</script>")
	else:
		obj2=Users.objects.filter(Username=username,Password=password)
		c2=obj2.count()
		if c2==1:
			ob=Users.objects.get(Username=username,Password=password)
			request.session['username'] = username
			request.session['uid'] = username
			request.session["pub_key"]=ob.P_address
			return HttpResponse("<script>alert('Login Successful');window.location.href='/show_home_user/';</script>")
		else:
			return HttpResponse("<script>alert('Invalid');window.location.href='/display_login/';</script>")
##########################################################################################
#Admin
@never_cache
def show_home_admin(request):
	if 'uid' in request.session:
		return render(request, 'home_admin.html')
	else:
		return render(request, 'login_register.html')

@never_cache
def logout(request):
	if 'uid' in request.session:
		del request.session['uid']
	return render(request, 'login_register.html')

@never_cache
def register(request):
	username = request.POST.get("uname")
	email=request.POST.get("email")
	password = request.POST.get("pswd")
	phn = request.POST.get("phone")
	p_address =request.POST.get("p_address")
	if not verify_adr(p_address):
		return HttpResponse("<script>alert('Public Key does not belong to blockchain');window.location.href='/display_login/';</script>")
	else:
		obj10 = Requests.objects.filter(
			Username=username, P_address=p_address,Email=email, Password=password,Phone=phn)
		co = obj10.count()
		if co == 1:
			return HttpResponse("<script>alert('Request is already sended, please wait for approval');window.location.href='/display_login/'</script>")
		else:
			obj1 = Requests(Username=username,P_address=p_address,Email=email, Password=password,Phone=phn)
			obj1.save()
			return HttpResponse("<script>alert('Registration request sended successfully, please wait for approval');window.location.href='/display_login/'</script>")


@never_cache
def view_requests(request):
	if 'uid' in request.session:
		mlist=Requests.objects.all()
		return render(request,'vrequest.html',{'req': mlist}) 
	else:
		return render(request,'login_register.html')


@never_cache
def display_users(request):
	if 'uid' in request.session:
		mlist=Users.objects.all()
		return render(request,'vusers.html',{'req': mlist}) 
	else:
		return render(request,'login_register.html')

@never_cache
def approve1(request):
	S_id=request.POST.get('S_id')
	Username=request.POST.get('Username')
	email=request.POST.get('Email')
	P_address=request.POST.get('P_address')
	password=request.POST.get('Password')
	phn=request.POST.get('Phone')
	obj10 = Users.objects.filter(
			Username=Username, Email=email, Password=password,Phone=phn,P_address=P_address)
	co = obj10.count()
	if co==1:
		obj1=Requests.objects.get(S_id=int(S_id))
		obj1.delete()
		return HttpResponse("<script>alert('User already existed');window.location.href='/view_requests/'</script>")
	else:		
		obj1=Users(
			Username=Username, Email=email, Password=password,Phone=phn,P_address=P_address)
		obj1.save()
		S_id=int(S_id)
		add_user1(S_id,P_address,Username,email,password,phn)
		obj3=Requests.objects.get(S_id=int(S_id))
		obj3.delete()
		return HttpResponse("<script>alert('Approved Successfully');window.location.href='/view_requests/'</script>")

@never_cache
def reject1(request):
	S_id=request.POST.get('S_id')
	obj1=Requests.objects.get(S_id=int(S_id))
	obj1.delete()
	return HttpResponse("<script>alert('Rejected Successfully');window.location.href='/view_requests/'</script>")
################################################################################################################


@never_cache
def view_records(request):
	if 'uid' in request.session:
		username=request.session['username']
		rec_list=Records.objects.filter(access=username)
		return render(request,'view_records.html',{'records': rec_list}) 
	else:
		return render(request,'login_register.html')

#####################################################################################################################
#####################################################################################################################

#Boat
@never_cache
def show_home_user(request):
	if 'uid' in request.session:
		return render(request, 'home_user.html')
	else:
		return render(request, 'login_register.html')

@never_cache
def display_upload_data(request):
	if 'uid' in request.session:
		return render(request, 'upload_data.html')
	else:
		return render(request, 'login_register.html')


def encryption(data,key,out_path,f_name):
	key = key.encode('utf-8')

	# Generate a new IV for each file
	iv = get_random_bytes(AES.block_size)
	print("IV: ", iv)

	# Create a cipher object with AES algorithm and CBC mode
	cipher = AES.new(key, AES.MODE_CBC, iv)

	# Read the file content
	with open(data, 'rb') as f:
	    plaintext = f.read()

	# Encrypt the content
	ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

	output_file=out_path+f_name
	# Write the IV and encrypted content back to the original file
	with open(output_file, 'wb') as f:
	    f.write(iv + ciphertext)


def decrypt_file(private_key,data):
	key = private_key[:16]
	bytes_key = key.encode('utf-8')

	# Extract the IV and ciphertext
	iv = data[:AES.block_size]
	ciphertext = data[AES.block_size:]

	# Create a cipher object with AES algorithm, CBC mode, and the extracted IV
	cipher = AES.new(bytes_key, AES.MODE_CBC, iv)

	# Decrypt the content
	plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

	return plaintext


@never_cache
def upload_file(request):
	private_key=request.POST.get('pkey')
	file1 = request.FILES["upl"]
	pub_key=request.session["pub_key"]
	username=request.session['username']
	path="pkeeper_app/static/temp_files/"
	path1="pkeeper_app/static/temp_emp_files/"
	file_name=file1.name
	print("file_name : ",file_name)

	verify_result=verify_key(pub_key,private_key,1)
	if(verify_result=="No"):
		return HttpResponse("<script>alert('Key Error');window.location.href='/display_upload_data/'</script>")
	else:
		if Records.objects.filter(record_name=file_name).exists():
			return HttpResponse("<script>alert('File with this name already Exist');window.location.href='/display_upload_data/'</script>")
		else:
			fs = FileSystemStorage("pkeeper_app/static/temp_files/")
			fs.save(file_name, file1)
			get_key=private_key[:16]
			encryption(path+file_name,get_key,path1,file_name)
			f_path="pkeeper_app/static/temp_files/"+str(file_name)
			api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
			new_file = api.add(path1+file_name)
			print(new_file)
			hash1=new_file.get('Hash')

			print("hash : ",hash1)

			now = datetime.now()
			time = now.strftime("%H:%M:%S")
			print("Current Time =", time)

			today = date.today()
			current_date = today.strftime("%d/%m/%Y")
			print("date =",current_date)


			obj4=Records(record_name=file_name,access=username,date=current_date,time=time,hash_value=hash1)
			obj4.save()
			obj3=Records.objects.get(record_name=file_name,access=username,date=current_date,time=time,hash_value=hash1)
			record_id = obj3.id
			record_id=int(record_id)
			#Stored to blockchain
			add_records(record_id,file_name,username,current_date,time,hash1)

			if os.path.exists(f_path):
				os.remove(f_path)

			
			return HttpResponse("<script>alert('Record Uploaded Succesfully');window.location.href='/display_upload_data/'</script>")



###################################################################################################################
###################################################################################################################



def collect(request):
	username=request.session["username"]
	hashh=request.POST.get("hash_value")
	file_name=request.POST.get("record_name")
	private_key = request.POST.get("d_key")

	#print("private_key :::",private_key)

	print("my_hash_value : ",hashh)

	obj1=Users.objects.get(Username=username)
	public_key=obj1.P_address

	verify_result=verify_key(public_key,private_key,1)
	if(verify_result=="No"):
		return HttpResponse("<script>alert('Key Error');window.location.href='/view_records/'</script>")
	else:
		hashh=hashh.strip()
		api = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
		api.get(hashh)
		with open(hashh , 'rb') as f1:
			my_content=f1.read()
			print("**************")
			print(my_content)
			get_decrypted_content=decrypt_file(private_key,my_content)
			print("Decrypted : ",get_decrypted_content)
			response = HttpResponse(get_decrypted_content, content_type="application/vnd.ms-excel")
			response['Content-Disposition'] = 'inline; filename=' + file_name
			return response


