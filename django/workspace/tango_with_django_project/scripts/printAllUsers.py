from django.contrib.auth.models import User
from rango.models import UserProfile
import traceback 

def run():
    try:
        print "-----Users"
        for userObj in User.objects.all():
            print userObj.username
            print UserProfile.objects.get(user=userObj)
    
        print"-----UserProfiles"
        for user_profile in UserProfile.objects.all():
            print user_profile.user.username
    except:
        tb = traceback.format_exc()
        print tb