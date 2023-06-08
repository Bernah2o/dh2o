from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from authApp.forms import LoginForm
from django.views import View
from django.urls import reverse
#from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib import messages


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request, user)
                admin_url = reverse('admin:index')  # Obtiene la URL de administración
                return redirect(admin_url)  # Redirige al usuario al panel de administración
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos.')
        return render(request, 'login.html', {'form': form})
    
    def logout(self, request):
        logout(request)
        messages.success(request, 'Has cerrado sesión exitosamente.')
        return redirect('login')
