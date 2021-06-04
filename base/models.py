from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from django.utils import timezone
import os
from moviepy.editor import *
import time


class Userprofile(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	bio=models.CharField(max_length=200,null=True,blank=True)
	gender=models.CharField(max_length=7,null=True,blank=True)
	dob=models.DateField(null=True,blank=True)
	address=models.CharField(max_length=100,null=True,blank=True)
	profile_picture=models.ImageField(default='image/profile_picture/default.jpeg',upload_to='image/profile_picture')
	created=models.DateTimeField(default=timezone.now)

	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)
		img=Image.open(self.profile_picture.path)

		if img.height>200 or img.width>200:
			new_image=(200,200)
			img.thumbnail(new_image)
			img.save(self.profile_picture.path)

	def __str__(self):
		return str(self.user)

class Post(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	caption=models.TextField(max_length=200)
	post_picture=models.FileField(upload_to='image/post_picture',null=True,blank=True)

	likes_user=models.ManyToManyField(User,related_name='likes_user')
	created=models.DateTimeField(default=timezone.now)

	def save(self,*args,**kwargs):
		name,extension=os.path.splitext(self.post_picture.name)

		if extension=='.jpg' or extension=='.png' or extension=='.jpeg':
			super().save(*args,**kwargs)
			img=Image.open(self.post_picture.path)

			if img.height>400:
				new_image=(400,img.width)
				img.thumbnail(new_image)
				img.save(self.post_picture.path)				
		elif extension=='.mp4':
			super().save(*args,**kwargs)			

			clip1=VideoFileClip(self.post_picture.path)

			if clip1.w>200 or clip1.h>200:
				original_file_name=os.path.basename(os.path.normpath(self.post_picture.path))
				temp_file=self.post_picture.path.replace(original_file_name,'temp_xyz_abc.mp4')
				clip2=clip1.resize(width=300,height=300)
				clip2.write_videofile(temp_file)
				os.remove(self.post_picture.path)
				os.rename(temp_file, self.post_picture.path)
			
	def __str__(self):
		return str(self.caption)
	def get_extension(self):
		name, extension = os.path.splitext(self.post_picture.name)
		if extension=='.jpg' or extension=='.png' or extension=='.jpeg':
			return 'pic'
		elif extension=='.mp4':
			return 'vdo'


class Comment(models.Model):
	post=models.ForeignKey(Post,on_delete=models.CASCADE)
	text=models.CharField(max_length=200,null=True,blank=True)
	commenter=models.ForeignKey(User,on_delete=models.CASCADE)
	created=models.DateTimeField(default=timezone.now)

	def __str__(self):
		return str(self.text)+""+str(self.post)


class ThreadModel(models.Model):
	sender=models.ForeignKey(User, on_delete=models.CASCADE,related_name='+',blank=True,null=True)
	reciver=models.ForeignKey(User, on_delete=models.CASCADE,related_name='+',blank=True,null=True)

class MessageModel(models.Model):
	thread=models.ForeignKey(ThreadModel,on_delete=models.CASCADE,related_name='+',blank=True,null=True)
	sender=models.ForeignKey(User, on_delete=models.CASCADE,related_name='+')
	reciver=models.ForeignKey(User, on_delete=models.CASCADE,related_name='+')
	text=models.CharField(max_length=500)
	is_seen=models.BooleanField(default=False)
	created=models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
	#1->like 2->comment 3->message 4->post
	notification_type=models.PositiveIntegerField()
	to_user=models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name='notification_to')
	from_user=models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name='notification_from')
	post=models.ForeignKey(Post,on_delete=models.CASCADE,null=True,blank=True)
	thread=models.ForeignKey(ThreadModel,on_delete=models.CASCADE,null=True,blank=True)
	date=models.DateTimeField(default=timezone.now)
	user_is_seen=models.BooleanField(default=False)

	def __str__(self):
		return str(self.to_user)
