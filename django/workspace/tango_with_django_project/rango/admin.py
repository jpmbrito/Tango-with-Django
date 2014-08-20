from django.contrib import admin
from rango.models import Category, Page

#Customize the admin page
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'likes', 'views')

class PageAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'url', 'views')


#Register the models
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)

