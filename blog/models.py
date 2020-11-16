from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Blog(models.Model):
	id=models.AutoField
	author=models.CharField(max_length=40)
	title=models.CharField(max_length=100,unique=True)
	blog=models.TextField()
	date=models.DateField(auto_now_add=True)
	views=models.IntegerField(default=0)
	likes=models.IntegerField(default=0)
	def __str__(self):
		return self.title


class BlogComment(models.Model):
	id=models.AutoField
	comment=models.TextField()
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	blog=models.ForeignKey(Blog, on_delete=models.CASCADE)
	parent=models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
	dateTime=models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f'{self.user.first_name} - {self.comment}'


class Like(models.Model):
	userIp=models.CharField(max_length=15)
	blogid=models.IntegerField()