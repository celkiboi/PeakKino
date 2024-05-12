from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .decorators import staff_required
from .models import User
from django.http import JsonResponse

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

@login_required
@staff_required
def approve_accounts(request):
    accounts = User.objects.filter(is_approved = False)

    context = {
        'accounts' : accounts
    }

    return render(request, 'approve_accounts.html', context)

@login_required
@staff_required
@require_POST
def approve_account(request, id):
    user = get_object_or_404(User, pk=id)
    user.is_approved = True
    user.save()

    return JsonResponse({'success': True, 'message': 'User approved succesfully'})