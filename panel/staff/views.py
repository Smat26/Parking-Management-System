from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from form import UserForm


@login_required
def LogoutUser(request):
	logout(request);
	return HttpResponseRedirect("/login/")

# Create your views here.
def LoginUser(request):

	error= ''
	loggedout = True;

	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
		    username = request.POST['username']
		    password = request.POST['password']
		    user = authenticate(username=username, password=password)

		    if user is not None:
		        if user.is_active:
		            login(request, user)
		            return HttpResponseRedirect("/main/")

		            # Redirect to a success page.
		        else:
		        	error = 'Account disabled'
		        	# Return a 'disabled account' error message
        	else:
				# Return an 'invalid login' error message.
				error = 'Invalid login'
		if error == '':
			error = 'Wrong Username and/or Password'

	if request.user.is_active:
		loggedout = False;
	



	Context = ({
		'form' : UserForm(),
		'loggedout' : loggedout,
		'error' : error,
	})


	return render(request, 'login.html', Context)


