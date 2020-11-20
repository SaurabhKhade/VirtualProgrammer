from django.shortcuts import render,HttpResponse,redirect
from .models import Contact
from django.contrib import messages
from blog.models import Blog,Like,BlogComment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import json
from blog.templatetags import tags

# Create your views here.
def home(request,msgkey='',msg=''):
	context={}
	if msg != '':
		if msgkey=='success':
			messages.success(request,msg)
			context['msgkey']=msgkey
		else:
			messages.error(request,msg)
			context['msgkey']=msgkey
			
	viewed_blogs=Blog.objects.all().order_by('-views')[:5]
	context['viewedBlogs']=viewed_blogs
	viewed_insights={}
	for blog in viewed_blogs:
		likes=Like.objects.filter(blogid=blog.id).count()
		comments=BlogComment.objects.filter(blog=blog,parent=None).count()
		views=blog.views
		viewed_insights[blog.id]=[likes,comments,views]
	context['viewed_insights']=viewed_insights
	
	latest_blogs=Blog.objects.all().order_by('-id')[:5]
	context['latestBlogs']=latest_blogs
	latest_insights={}
	for blog in latest_blogs:
		likes=Like.objects.filter(blogid=blog.id).count()
		comments=BlogComment.objects.filter(blog=blog,parent=None).count()
		views=blog.views
		latest_insights[blog.id]=[likes,comments,views]
	context['latest_insights']=latest_insights
	
	liked_blogs=Blog.objects.all().order_by('-likes')[:5]
	context['likedBlogs']=liked_blogs
	liked_insights={}
	for blog in liked_blogs:
		likes=Like.objects.filter(blogid=blog.id).count()
		comments=BlogComment.objects.filter(blog=blog,parent=None).count()
		views=blog.views
		liked_insights[blog.id]=[likes,comments,views]
	context['liked_insights']=liked_insights
	
	context['tot_members']=User.objects.all().count()
	blogs=Blog.objects.all()
	context['tot_blogs']=blogs.count()
	context['tot_comments']=BlogComment.objects.filter(parent=None).count()
	context['tot_replies']=BlogComment.objects.all().exclude(parent=None).count()
	views=0
	for blog in blogs:
		views+=blog.views
	context['tot_views']=views
	context['tot_likes']=Like.objects.all().count()
	
	return render(request,'home/index.html',context)
	

def about(request):
	context={}
	context['members']=User.objects.all().count()
	blogs=Blog.objects.all()
	context['blogs']=blogs.count()
	context['comments']=BlogComment.objects.filter(parent=None).count()
	context['replies']=BlogComment.objects.all().exclude(parent=None).count()
	views=0
	for blog in blogs:
		views+=blog.views
	context['views']=views
	context['likes']=Like.objects.all().count()
	return render(request,'home/about.html',context)
	
	
def contact(request):
	param={}
	if request.method=='POST':
		try:
			name=request.POST['name']
			email=request.POST['email']
			issue=request.POST['issue']
			if len(name)<3 or len(email)<5 or len(issue)<5:
				messages.error(request,'too short details, please fill form correctly')
				param['msgkey']='danger'
			else:
				contact=Contact(name=name,email=email,issue=issue)
				messages.success(request,'Message has been sent successfully')
				param['msgkey']='success'
		
		except:
			messages.error(request,'Failed to send the message! please try again.')
			param['msgkey']='danger'
		
	return render(request,'home/contact.html',param)

	
def HandleSignup(request):
	if request.method=="POST":
		try:
			username=request.POST['username']
			fname=request.POST['fname']
			lname=request.POST['lname']
			email=request.POST['email']
			password=request.POST['password']
			user = User.objects.create_user(username, email, password)
			user.first_name=fname
			user.last_name=lname
			user.save()
			login(request,user)
			return home(request,'success','Your account has been created successfully')
		except:
			return home(request,'danger','Failed to create account! please try again or use different username.')
			
	else:
		return redirect('/')
	
	
def HandleLogin(request):
	if request.method=="POST":
		try:
			username=request.POST['username']
			password=request.POST['password']
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request,user)
				return home(request,'success','You have been logged in successfully')
			else:
				return home(request,msgkey='danger',msg='Invalid Credentials')
		except:
			return home(request,msgkey='danger',msg='Failed to login! please try again.')
	else:
		return redirect('/')
	
	
def HandleLogout(request):
	logout(request)
	return home(request,'success','logged out successfully')
	
	
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
	
def like(request):
	if request.method=="POST":
		get_client_ip(request)
		id=request.POST['id']
		user=request.user
		ip=get_client_ip(request)
		try:
			like=Like.objects.get(userIp=ip,blogid=id)
		except:
			ip=get_client_ip(request)
			like=Like(userIp=ip,blogid=id)
			like.save()
		finally:
			result={'status':'success'}
			result['likes']=Like.objects.filter(blogid=id).count()
			blog=Blog.objects.get(id=id)
			blog.likes=result['likes']
			blog.save()
		return HttpResponse(json.dumps(result), content_type='application/x-json')
		
	return redirect('/')
	