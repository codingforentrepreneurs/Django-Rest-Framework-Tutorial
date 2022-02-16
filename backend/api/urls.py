from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from . import views
# from .views import api_home


urlpatterns = [
    path('auth/', obtain_auth_token),
    path('', views.api_home), # localhost:8000/api/
    # path('products/', include('products.urls'))
]
