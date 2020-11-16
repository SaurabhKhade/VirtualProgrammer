from django.shortcuts import render,HttpResponse
from .models import Blog,BlogComment,Like
from django.contrib import messages
from .templatetags import tags
# Create your views here.

def blogs(request):
	blogs=Blog.objects.all().order_by('-id')
	insights={}
	for blog in blogs:
		likes=Like.objects.filter(blogid=blog.id).count()
		comments=BlogComment.objects.filter(blog=blog,parent=None).count()
		views=blog.views
		insights[blog.id]=[likes,comments,views]
	context={'blogs':blogs,'insights':insights}
	return render(request,'blog/blogs.html',context)
	
	
def site(request,title,msgkey='',msg=''):
	context={}
	if msg != '':
		if msgkey=='success':
			messages.success(request,msg)
			context['msgkey']=msgkey
		else:
			messages.error(request,msg)
			context['msgkey']=msgkey
			
	blog=Blog.objects.filter(title=title).first()
	context['blog']=blog
	context['comments']=reversed(BlogComment.objects.filter(blog=blog,parent=None))
	replies=reversed(BlogComment.objects.filter(blog=blog).exclude(parent=None))
	repDict={}
	for reply in replies:
		if reply.parent.id in repDict:
			repDict[reply.parent.id].append(reply)
		else:
			repDict[reply.parent.id]=[reply]
	context['likes']=Like.objects.filter(blogid=blog.id).count()
	context['replyList']=repDict
	context['likes']=Like.objects.filter(blogid=blog.id).count()
	context['tot_comments']=BlogComment.objects.filter(blog=blog,parent=None).count()
	blog.views+=1
	blog.save()
	context['views']=blog.views
	return render(request,'blog/site.html',context)


def search(request):
	search=request.GET['search']
	context={}
	if len(search)>70:
		results=Blog.objects.none()
		messages.warning(request,'Your query is so big please try with shorter query')
		context['msgkey']='warning'
	else:
		title=Blog.objects.filter(title__icontains=search)
		blog=Blog.objects.filter(blog__icontains=search)
		results=[query for query in title]
		for query in blog:
			if query not in results:
				results.append(query)
	if len(results) == 0:
		context['resultcolor']='danger'
	else:
		context['resultcolor']='success'
		
	insights={}
	for blog in results:
		likes=Like.objects.filter(blogid=blog.id).count()
		comments=BlogComment.objects.filter(blog=blog,parent=None).count()
		views=blog.views
		insights[blog.id]=[likes,comments,views]
	context['insights']=insights
	context['count']=len(results)
	context['results']=results
	context['search']=search
	return render(request,'blog/search.html',context)
	

def postComment(request):
	if request.method=='POST':
		try:
			content=request.POST['comment']
			blogid=request.POST['blogid']
			blog=Blog.objects.get(id=blogid)
			user=request.user
			parentid=request.POST['parent']
			if len(content)<2:
				return site(request,blog.title,msgkey='danger',msg="too Short comment! please try again")
				
			if parentid=='':
				comment=BlogComment(comment=content,user=user,blog=blog)
				comment.save()
				return site(request,blog.title,msgkey='success',msg='Your Comment posted successfully')
			else:
				parent=BlogComment.objects.get(id=parentid)
				comment=BlogComment(comment=content,user=user,blog=blog,parent=parent)
				comment.save()
				return site(request,blog.title,msgkey='success',msg='Your Reply posted successfully')
			
		except:
			return site(request,blog.title,msgkey='danger',msg="Your Comment can't be saved! maybe exactly same comment already present please try again")
		
	return redirect(f'/blog/{blog.title}')
	