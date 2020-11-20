from django.contrib import admin
from .models import Blog,BlogComment,Like
# Register your models here.
admin.site.register((BlogComment,Like))

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
	class Media:
		js=('tiny.js',)