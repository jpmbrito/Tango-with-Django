from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

#Integration with the models
from rango.models import Category
from rango.models import Page
from datetime import datetime

# Create your views here.
def index(request):
    context = RequestContext(request)

    top_category_list = Category.objects.order_by('-likes')[:5]

    #Add the url attribute to the category object
    for category in top_category_list:
        category.url = category.name.replace(' ', '_')
    
    # Process the template
    response =  render_to_response('rango/index.html', 
            {
            'categories' : top_category_list, 
            'pages' : Page.objects.order_by('-views')[:5]
            },
            context)
    
    #Server side cookie processing
    if request.session.get('last_visit'):
        #Get the server cookie
        last_visit_time = request.session.get('last_visit')
        visits = request.session.get('visits',0)
        
        
        #Check if it elapsed in seconds (to be more visible)
        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).seconds > 0:
            request.session['visits'] = visits + 1
            request.session['last_visit'] = str(datetime.now())
    else:
        #Create the Cookie
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1
        
    return response
    
def about(request):
    context = RequestContext(request)
    
    context_dict = {'aboutMessage': 
            "This is the about message"}
                    
        
    return render_to_response('rango/about.html', 
            {
            'aboutMessage': 'This is the about message',
            'last_visit' : request.session['last_visit'],
            'visits' :  request.session['visits']
            }, 
            context)

def exercice(request):
    context = RequestContext(request)
    context_dict = { 'varName' : 'Exercice Completed :)' }
    return render_to_response('rango/exercice.html', context_dict, context)

def category(request, category_name_url):
    context = RequestContext(request)

    #Parse the category name that comes in the URL
    category_name = category_name_url.replace('_', ' ')

    #Create the Context Dictionary that will be passed for the template
    context_dict = {'category_name' : category_name , 'category_name_url' : category_name_url }

    try:
        #Get the category object
        category = Category.objects.get(name=category_name)

        #Get the pages of the object
        pages = Page.objects.filter(category=category)

        #Add the pages object to the context variable to be passed for the template
        context_dict['pages'] = pages

        #Add the category object for the context variable to show more details
        context_dict['category'] = category

    except Category.DoesNotExist:
        pass
    
    return render_to_response('rango/category.html', context_dict, context)


from rango.forms import CategoryForm
@login_required
def add_category(request):
    context = RequestContext(request)

    #Check the html message type
    if request.method == 'POST' :
        form = CategoryForm(request.POST)

        #Validate the form
        if form.is_valid():
            #Save the new object
            form.save(commit=True)
            #Redirect the user to the index
            return index(request)
        else:
            #Print errors on terminal
            print form.errors
    else:
        #Get the form attributes
        form = CategoryForm()

    #Bad Form (or form details)
    #Render the form with error messages
    return render_to_response('rango/add_category.html',
            {'form':form},
            context)

from rango.forms import PageForm
@login_required
def add_page(request, category_name_url ):
    context = RequestContext(request)
    category_name = category_name_url.replace(' ', '_')
    
    if request.method == 'POST' :
        print "POST"
        form = PageForm(request.POST)
        
        if form.is_valid():
            page = form.save(commit=False)
            
            try:
                cat = Category.objects.get(name = category_name)
                page.category = cat #Foreign Key
                
            except Category.DoesNotExist:
                return render_to_response('rango/add_category.html',
                        {},
                        context)
                        
            page.views = 0
            page.save()
           
            return category(request, category_name_url)
        else:
            print form.errors
    
    else:
        form = PageForm()
        
    return render_to_response('rango/add_page.html',
            {'form' : form, 
            'category_name_url' : category_name_url,
            'category_name' : category_name},
            context)

from rango.forms import UserForm, UserProfileForm
        
def register(request):
    context = RequestContext(request)
    
    registered = False
    
    if request.method == 'POST' :
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
      
        if user_form.is_valid() and profile_form.is_valid():
            #Work in default django User
            user = user_form.save() #Save user in database
            
            user.set_password(user.password) #Hash the password in DB
            user.save()
            
            #Work in rango user
            profile = profile_form.save(commit=False)
            profile.user = user #Foreign key assignment
            
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()
            
            registered = True
        else:
            print user_form.errors, profile_form.errors
            
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    return render_to_response(
        'rango/register.html',
        {
        'user_form' : user_form,
        'profile_form' : profile_form,
        'registered' : registered
        },
        context)

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
def user_login(request):
    context = RequestContext(request)
    
    if request.method == 'POST':
        #Gather the username and password from POST
        username = request.POST['username']
        password = request.POST['password']
        
        #Try to authenticate with django auth application
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your Rango Account is disabled")
        else:
            print "Invalid Login Details; {0} , {1}".format(username,password)
            return HttpResponse("Invalid login details supplied.")
    else:
        #Present the login page
        return render_to_response(
            'rango/login.html',
            {},
            context)
            
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")
    
from django.contrib.auth import logout
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')