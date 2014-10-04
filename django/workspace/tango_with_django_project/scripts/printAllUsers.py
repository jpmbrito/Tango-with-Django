from django.contrib.auth.models import User
from rango.models import UserProfile
import traceback 

def run():
    for userObj in User.objects.all():
        print userObj.username
        try:
            print UserProfile.objects.get(user=userObj).website
        except:
            pass