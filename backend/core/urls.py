# routiner_backend/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Estas são as linhas que resolvem o erro 404 para o login/registro
    path('api-auth/', include('dj_rest_auth.urls')),
    path('api-auth/registration/', include('dj_rest_auth.registration.urls')),

    # Esta linha conecta o arquivo que você me mostrou ao projeto principal
    path('api/', include('api.urls')),
]