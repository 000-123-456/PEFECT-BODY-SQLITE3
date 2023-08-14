from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
# Create your views here.
def prueba(request):
     return render(request, "layout/index.html")

class LoginFormView(LoginView):
    template_name='AppUsers/pages-register.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('prueba')
        return super().dispatch(request, *args, **kwargs)
    
def pruebaForm(request):
    data={
        'titulo':'Registro de compra',
        'modulo':'Compra',
    }
    return render(request,'layout/form.html',data)