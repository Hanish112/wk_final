from django.shortcuts import render, redirect
from authlib.integrations.django_client import OAuth
from django.conf import settings


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
