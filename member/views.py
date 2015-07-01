import uuid
import json

from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from member.models import UserProfile, create_user_with_random_username
from member.forms import RegistrationForm, AuthenticationForm
from food.forms import TokenCheckForm


#join
@csrf_exempt
def register(request):
    def get_registration_user_profile(cleaned_data):
        user = create_user_with_random_username(email=cleaned_data['email'], password=cleaned_data['password'])
        _user_profile = UserProfile.objects.create(user=user, birthday=cleaned_data['birthday'],
                                                   gender=cleaned_data['gender'], token=str(uuid.uuid4()))
        return _user_profile

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_profile = get_registration_user_profile(form.cleaned_data)
            return HttpResponse(json.dumps(dict(status=dict(title="Register", code="OK", reason="OK"),
                                                user=user_profile.to_dict())), content_type='application/json')
        return HttpResponse(json.dumps(dict(status=dict(title="Register", code="FAIL", reason=form.errors.keys()[0]))),
                            content_type='application/json')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            return HttpResponse(json.dumps(dict(status=dict(title="Login", code="OK", reason="OK"),
                                                user=user.get_profile().to_dict())), content_type='application/json')
        return HttpResponse(json.dumps(dict(status=dict(title="Login", code="FAIL", reason=form.errors.keys()[0]))),
                            content_type='application/json')
    return HttpResponse(json.dumps(dict(status=dict(title="Login", code="FAIL", reason="NOT POST"))),
                        content_type='application/json')


@csrf_exempt
def user_delete(request):
    form = TokenCheckForm(request.POST)
    if form.is_valid():
        user = form.get_user()
        user.get_profile().delete()
        user.delete()
        return HttpResponse(json.dumps(dict(status=dict(code="OK", reason="OK", title="UserDelete"))),
                            content_type='application/json')
    return HttpResponse(json.dumps(dict(status=dict(title="UserDelete", code="FAIL", reason=form.errors.keys()[0]))),
                        content_type='application/json')
