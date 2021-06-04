from django.shortcuts import render
from .forms import PostUploadForm,CommentForm,profilePictureForm,UsereditForm
from django.contrib.auth.models import User,auth
from .models import Userprofile,Post,Comment,Notification,ThreadModel,MessageModel
import os
from django.db.models import Q
from pathlib import Path
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def error_404_views(request,exception):
	return render(request, '404.html')



@login_required
def home(request):
	if request.user.is_anonymous:
		return HttpResponseRedirect('login/')
	if request.method=='POST':
		fm_1=PostUploadForm(request.POST,request.FILES)
		fm_2=CommentForm()
		if fm_1.is_valid():
			user=request.user
			caption=fm_1.cleaned_data['caption']
			post_picture=fm_1.cleaned_data['post_picture']

			post=Post(user=user,caption=caption,post_picture=post_picture)

			post.save()

			for i in User.objects.all():
				Notification(notification_type=4,to_user=i,from_user=request.user,post=post).save()
			return HttpResponseRedirect('/')
	else:
		fm_1=PostUploadForm()

	post=Post.objects.all().order_by('id').reverse()
	comment=Comment.objects.all()
	user_profile=Userprofile.objects.all()
	notification=Notification.objects.filter(to_user=request.user).exclude(from_user=request.user).order_by('id').reverse()
	count_notification=Notification.objects.filter(to_user=request.user).exclude(user_is_seen=True).exclude(from_user=request.user)
	user_list=User.objects.exclude(username=request.user)
	return render(request,'home.html',{"form":fm_1,"post":post,"notifications_like":notification,"count_notification":count_notification,"user_profile":user_profile,"user_list":user_list})

def login(request):
	if request.method=='POST':
		username=request.POST['username']
		password=request.POST['password']
		user=auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request, user)
			return HttpResponseRedirect('/')
		else:
			messages.error(request,"Invalid Credential")
			return render(request,'login.html')
	return render(request,'login.html')

@login_required
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('login/')

@login_required
def profilepage(request):
	profile=Userprofile.objects.get(user=request.user)
	post=Post.objects.all().filter(user=request.user)
	fm_1=profilePictureForm()
	fm_2=UsereditForm()
	return render(request,'profilepage.html',{"profile":profile,"post":post,"access":True,"form_1":fm_1,"form_2":fm_2})

def signup(request):
	if request.method=='POST':
		first_name=request.POST['first_name']
		last_name=request.POST['last_name']
		username=request.POST['username']
		email=request.POST['email']
		password=request.POST['password']
		c_password=request.POST['conform_password']

		if User.objects.filter(username=username).exists():
			messages.error(request, 'Username alredy exists,try Some other username.')
			return HttpResponseRedirect('signup/')
		elif User.objects.filter(email=email).exists():
			messages.error(request, 'Email alredy taken,try with new email.')
			return HttpResponseRedirect('signup/')
		elif password!=c_password:
			messages.error(request, 'Two password fields does not matching.')
			return HttpResponseRedirect('signup/')
		else:
			User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name).save()
			messages.success(request,'Account Created.')
			return HttpResponseRedirect('login/')
	
	
	return render(request,'signup.html')

@login_required
def show_profile(request,username):
	profile=Userprofile.objects.get(user=username)
	post=Post.objects.all().filter(user=username)
	return render(request,'profilepage.html',{"profile":profile,"post":post,"access":False})

@login_required
def add_comment(request,post_id):
	if request.method=='POST':
		comment_text=request.POST['text']
		Comment(post=Post.objects.get(id=post_id),text=comment_text,commenter=request.user).save()
		Notification(notification_type=2,to_user=Post.objects.get(id=post_id).user,from_user=request.user,post=Post.objects.get(id=post_id)).save()
	return HttpResponseRedirect('/')

@login_required
def show_comment(request,post_id):
	comment=Comment.objects.all().filter(post=post_id)
	post=Post.objects.get(id=post_id)
	
	if request.method=="POST":
		fm=CommentForm(request.POST)
		if fm.is_valid():
			comment_text=fm.cleaned_data['text']
			Comment(post=Post.objects.get(id=post_id),text=comment_text,commenter=request.user).save()
			Notification(notification_type=2,to_user=Post.objects.get(id=post_id).user,from_user=request.user,post=Post.objects.get(id=post_id)).save()
	fm=CommentForm()
	return render(request,'show_comment.html',{"all_comments":comment,"post":post,"comment":fm})

@login_required
def edit_profile_pictute(request):
	if request.method=='POST':
		fm=profilePictureForm(request.POST,request.FILES)
		if fm.is_valid():
			profile=Userprofile.objects.get(user=request.user)
			profile.profile_picture=fm.cleaned_data['profile_picture']
			profile.save()
	return HttpResponseRedirect('/')

@login_required
def edit_profile(request):
	if request.method=='POST':
		profile=Userprofile.objects.get(user=request.user)
		profile.bio=request.POST['bio']
		profile.gender=request.POST['gender']
		profile.dob=request.POST['dob']
		profile.address=request.POST['address']
		profile.save()

	return HttpResponseRedirect('/')

@login_required
def add_like(request,post_id):
	if request.user in Post.objects.get(id=post_id).likes_user.all():
		Post.objects.get(id=post_id).likes_user.remove(request.user)
	else:
		Post.objects.get(id=post_id).likes_user.add(request.user)
		Notification(notification_type=1,to_user=Post.objects.get(id=post_id).user,from_user=request.user,post=Post.objects.get(id=post_id)).save()
	
	return HttpResponseRedirect('/')

@login_required
def add_like_profile(request,post_id):
	if request.user in Post.objects.get(id=post_id).likes_user.all():
		Post.objects.get(id=post_id).likes_user.remove(request.user)
	else:
		Post.objects.get(id=post_id).likes_user.add(request.user)
		Notification(notification_type=1,to_user=Post.objects.get(id=post_id).user,from_user=request.user,post=Post.objects.get(id=post_id)).save()
	return HttpResponseRedirect('profilepage/')

@login_required
def delet_post(request,post_id):
	post=Post.objects.get(id=post_id)
	post.delete()
	x=str(Path(__file__).resolve().parent.parent) +  str(post.post_picture.url)
	os.remove(x)
	return HttpResponseRedirect('profilepage/')

@login_required
def search(request):
	if request.method=='POST':
		x=request.POST['name']
		y=User.objects.filter(Q(first_name__icontains=x) | Q(last_name__icontains=x)  )
		user_list=[]
		for i in y:
			user_list.append(i)
		return render(request,'search.html',{'user':user_list})
	return render(request,'search.html',{'user':[]})

@login_required
def show_post(request,post_id,notification_id):
	profile=Userprofile.objects.get(user=request.user)
	post=Post.objects.filter(id=post_id)
	fm=profilePictureForm()
	notification=Notification.objects.get(id=notification_id)
	notification.user_is_seen=True
	notification.save()
	return render(request,'profilepage.html',{"profile":profile,"post":post,"access":False,"form":fm})


@login_required
def create_thread(request):
	if request.method=='POST':
		reciver_name=request.POST['reciver_name']
		reciver_name=reciver_name.split(' ')[0]

		if reciver_name==(request.user.first_name):
			messages.error(request,'Please Enter Valid user name')
			return HttpResponseRedirect('/')

		else:
			try:
				reciver=User.objects.get(first_name=reciver_name)
				if ThreadModel.objects.filter(sender=request.user,reciver=reciver).exists():
					thread = ThreadModel.objects.filter(sender=request.user, reciver=reciver)[0]
					x=str(thread.id)
					return HttpResponseRedirect('inbox/'+x+'/'+'0')

				elif ThreadModel.objects.filter(sender=reciver,reciver=request.user).exists():
					thread = ThreadModel.objects.filter(sender=reciver, reciver=request.user)[0]
					x=str(thread.id)			
					return HttpResponseRedirect('inbox/'+x+'/'+'0')

				else:
					thread=ThreadModel(sender=request.user,reciver=reciver)
					thread.save()
					x=str(thread.id)
					return HttpResponseRedirect('inbox/'+x+'/'+'0')
			except:
				messages.error(request,'Please Enter Valid user name')
				return HttpResponseRedirect('/')

	return HttpResponseRedirect('/')

@login_required
def inbox(request,thread_id,notification_id):
	thread=ThreadModel.objects.get(id=thread_id)
	reciver=''
	if thread.sender==request.user:
		reciver=thread.reciver
	else:
		reciver=thread.sender


	if request.method=='POST':
		message=request.POST['message']
		
		if thread.sender==request.user:
			MessageModel(thread=thread,sender=request.user,reciver=thread.reciver,text=message).save()
			Notification(notification_type=3,to_user=thread.reciver,from_user=request.user,thread=thread).save()
		else:
			MessageModel(thread=thread,sender=thread.reciver,reciver=thread.sender,text=message).save()
			Notification(notification_type=3,to_user=thread.sender,from_user=thread.reciver,thread=thread).save()
	msg=MessageModel.objects.filter(thread=thread)

	if int(notification_id) > 0:
		notification=Notification.objects.get(id=notification_id)
		notification.user_is_seen=True
		notification.save()
	return render(request, 'inbox.html',{'all_message':msg,'reciver':reciver})

	