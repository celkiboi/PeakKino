from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return redirect('/')
        else:
            return self.form_invalid(form)
    
def logout_view(request):
    logout(request)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form, 'student': request.user})