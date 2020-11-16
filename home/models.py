from django.db import models

# Create your models here.
class Contact(models.Model):
	msgno=models.AutoField
	name=models.CharField(max_length=40)
	email=models.CharField(max_length=20)
	issue=models.TextField()
	date=models.DateField(auto_now_add=True)
	def __str__(self):
		return f'{self.name} - {self.email}'