from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse

#Integration with the models
from rango.models import Category
from rango.models import Page

# Create your views here.

def index(request):
	context = RequestContext(request)

	top_category_list = Category.objects.order_by('-likes')[:5]

	#Add the url attribute to the category object
	for category in top_category_list:
		category.url = category.name.replace(' ', '_')
	
	
	context_dict = {'categories' : top_category_list}

	page_list = Page.objects.order_by('-views')[:5]
	context_dict['pages'] = page_list

	return render_to_response('rango/index.html', context_dict, context)

def about(request):
	context = RequestContext(request)
	
	context_dict = {'aboutMessage': 
			"This is the about message"}
	return render_to_response('rango/about.html', 
			context_dict, 
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