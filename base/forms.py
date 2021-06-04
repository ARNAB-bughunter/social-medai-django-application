from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Userprofile,Post,Comment

class UsereditForm(forms.ModelForm):
	class Meta:
		model=Userprofile
		fields=['bio','dob','address']
		labels={
		'bio':'',
		'dob':'',
		'address':''
		}

		widgets={
		'bio':forms.TextInput(attrs={ 'class':'form-control','placeholder':'Enter  About You','required':'true'  }),
		'address':forms.TextInput(attrs={ 'class':'form-control', 'placeholder':'Enter Your Adress','required':'true' }),
		'dob':forms.TextInput(attrs={ 'type':'date' ,'class':'form-control','placeholder':'Enter Your Birth Date','required':'true'  })
		}

		


class PostUploadForm(forms.ModelForm):
	class Meta:
		model=Post
		fields=['caption','post_picture']

		widgets={
		'caption':forms.Textarea(attrs={'style':'height:10px;','type':'textarea','class':'form-control','placeholder':"What's Meme in your mind?",'required':'false'}),
		'post_picture':forms.FileInput(attrs={'class':'form-control'})
		}

		labels={
		'caption':'',
		'post_picture':''
		}
		

class CommentForm(forms.ModelForm):
	class Meta:
		model=Comment
		fields=['text']

		widgets={
		'text':forms.Textarea(attrs={'cols':"0",'rows':"0",'autofocus':'true','type':'textarea','class':'form-control','placeholder':"Write a comment...",'required':'false'}),
		}
		labels={
		'text':''
		}

class profilePictureForm(forms.ModelForm):
	class Meta:
		model=Userprofile
		fields=['profile_picture']

		labels={
		'profile_picture':''
		}

		widgets={
		'profile_picture':forms.FileInput(attrs={'class':'form-control'  })
		}

