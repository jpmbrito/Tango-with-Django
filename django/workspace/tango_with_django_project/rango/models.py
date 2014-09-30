from django.db import models

# Add more fields to the User
from django.contrib.auth.models import User
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    #Add more user Attributes
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username
    
# Create your models here.
class Category(models.Model):
	class Meta:
		verbose_name_plural = "Categories"
	
	name = models.CharField(max_length=128, unique=True)
	views = models.IntegerField(default = 0)
	likes = models.IntegerField(default = 0)

	def __unicode__(self):
		return self.name

class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=128)
	url = models.URLField(unique=True)
	views = models.IntegerField(default = 0)

	def __unicode__(self):
		return self.title
