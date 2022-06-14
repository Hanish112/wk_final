from gettext import install
from django.shortcuts import render, redirect
from django.urls import reverse
from authlib.integrations.django_client import OAuth
from django.conf import settings
from urllib.parse import quote_plus, urlencode
from django.db import models
from panel.model_creator import create_model
from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered


oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("dashboard")))

def dashboard(request):
    if request.session.get('user') == None:
        return redirect('login')
    from django.apps import apps
    app_models = [model.__name__ for model in apps.get_models(include_auto_created=True)]
    print(app_models)
    from django.contrib.contenttypes.models import ContentType
    ContentType.objects.filter(app_label="auth")
    session = request.session.get("user")
    return render(request, 'panel/index.html', {'name': session['userinfo']['name']})

def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )

def create_table(request):
    if request.method == 'POST':
        table_name = request.POST.get('table_name')
        if table_name.strip() == '':
            return render(request, 'panel/create_table.html', {'error': 'Table name is mandatory !'})
        print(request.POST)
        field_cnt = (len(request.POST.keys()) - 3) // 3
        if field_cnt == 0:
            return render(request, 'panel/create_table.html', {'error': 'No fields added !'})
        field_names = []
        field_types = []
        primary_key = -1
        for i in range(1, field_cnt+1):
            name = request.POST.get('field_name' + str(i))
            if name.strip() == '':
                return render(request, 'panel/create_table.html', {'error': 'One or more field names are empty !'})
            type = request.POST.get('field_type' + str(i))
            pr_key = request.POST.get('primary_key' + str(i))
            if pr_key == 'Yes':
                if primary_key != -1:
                    return render(request, 'panel/create_table.html', {'error': 'Only one primary key is allowed!'})
                else:
                    primary_key = i
            field_names.append(name)
            field_types.append(type)
        print(field_names)
        print(field_types)
        fields = {}
        for i in range(field_cnt):
            pr = (primary_key == (i+1))
            if field_types[i] == 'String':
                model = models.CharField(max_length=200, null=True, primary_key=pr)
            if field_types[i] == 'Number':
                model = models.IntegerField(null=True, primary_key=pr)
            if field_types[i] == 'Boolean':
                model = models.BooleanField(null=True, primary_key=pr)
            if field_types[i] == 'Email':
                model = models.EmailField(null=True, primary_key=pr)
            if field_types[i] == 'Datetime':
                model = models.DateTimeField(null=True, primary_key=pr)
            fields[field_names[i].replace(' ', '_')] = model

        table_name = table_name.strip().replace(' ', '_')
        mdl = create_model(
            name=table_name,
            fields=fields,
            app_label='panel'
        )
        return redirect('dashboard')
    return render(request, 'panel/create_table.html')

def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("login")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )