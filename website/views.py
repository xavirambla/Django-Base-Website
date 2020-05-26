from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.db.utils import IntegrityError
from django.core.exceptions import  ValidationError
from django.contrib.auth import authenticate, login, logout ,get_user
from django.contrib.auth.models import User , Group
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.password_validation   import  validate_password
from django.contrib import messages
from django.core.mail import send_mail
from .forms import User_Form


# Create your views here.
def index(request):
    if  request.user.is_authenticated:
        return render(request ,"private/index.html")
    else:
        return render(request ,"public/index.html")


@login_required
def private_index(request):
    return render(request ,"private/index.html")



#registramos al usuario
def register(request):
    if request.method == 'POST':
        username   = request.POST["username"]
        email      = request.POST["email"]
        password   = request.POST["password"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]



#validate_password(password, user=None, password_validators=None)

        try:
            validate_password(password)    
            user = User.objects.create_user(username = username, email = email, password = password, first_name = first_name , last_name = last_name)            
            user.save()

        except IntegrityError:
            messages.error(request, _('Usuario ya existe, escoja otro nombre de usuario.'))
            return render(request,"registration/register.html")
#        except ValueError as inst:            
        except ValidationError as inst:     
            messages.error(request, _(inst.__str__()))
            return render(request,"registration/register.html")

        #except Exception as error:   
         #   messages.error(request, str(error) )
          #  return render(request,"registration/register.html")
                                                
        messages.info(request, _('Usuario creado.')  )

        return render(request,"private/index.html")
    else:    
        return render(request,"registration/register.html")


@login_required
def myaccount_details(request):
    user = get_user(request)

    if request.method == 'POST': 
        user_form = User_Form(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()

            messages.info(request, _('Datos modificados.')  )
            
            return render(request,"private/index.html")
        else:
            context = {
              'form': user_form,
                } 
            messages.error(request, _('Please correct the error below.'))
            return render(request,"registration/myaccount_details.html", context)
    else:
        user_form = User_Form(instance=request.user)
        context = {
            'form': user_form,
        } 

        return render(request,"registration/myaccount_details.html",context )


