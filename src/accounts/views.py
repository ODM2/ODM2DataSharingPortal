from django.conf import settings
from django.contrib.auth import logout as django_logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render


from datetime import datetime

from accounts.backend import CognitoBackend
from dataloaderinterface.forms import OrganizationForm

_cognitobackend = CognitoBackend()

_SESSION_KEY = settings.SESSION_KEY
_BACKEND_SESSION_KEY = settings.BACKEND_SESSION_KEY
_HASH_SESSION_KEY = settings.HASH_SESSION_KEY

def login(request:HttpRequest) -> HttpResponse:
    return (redirect (settings.COGNITO_SIGNIN_URL))

def logout(request:HttpRequest) -> HttpResponse: 
    django_logout(request)
    return redirect('home')

def signup(request:HttpRequest) -> HttpResponse:
    return redirect (settings.COGNITO_SIGNUP_URL)

def reset_password(request:HttpRequest) -> HttpResponse:
    return redirect (settings.COGNITO_RESET_URL)

def login_failed(request:HttpRequest) -> HttpResponse:
    """Placeholder authorization failed endpoint"""
    return render(
        request,
        'auth/login_failed.html',
        {
            'title':'Login Failed',
            'year':datetime.now().year,
        }
    )

def _login_success(request:HttpRequest) -> HttpResponse:    
    """post login placeholder for more advanced rerouting - e.g. organziation specific page"""
    return redirect('home')

def oauth2_cognito(request:HttpRequest) -> HttpResponse:
    try: 
        auth_code = request.GET['code']
        user = _cognitobackend.authenticate(code=auth_code)
        _cognitobackend.login(request, user)
        return _login_success(request)
    except Exception as e:
        return redirect(login_failed)
 
def account(request:HttpRequest) -> HttpResponse:
    return render(
        request,
        "auth/account.html",
        {
            'organization_form': OrganizationForm()
        },
    )

def update_account(request:HttpRequest) -> HttpResponse:
    form_data = request.POST.dict()
    user = request.user
    user._set_access_token(request.session['TOKEN'])
    try:
        for key, value in form_data.items():
            current_value = getattr(user, key)
            if current_value != value:
                setattr(user, key, value)       
        return HttpResponse(
            content='updates accepted',
            status=201,
        )
    except AttributeError as e:
        #TODO this needs to return error code, butt I've not implemented organization update yet
        return HttpResponse(
            content=f"Unknown attribute: '{e.name}'",
            status=400,
        )
    except Exception as e:
        return HttpResponse(
            content='updates failed',
            status=500,
        )

