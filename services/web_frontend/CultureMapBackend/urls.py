from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from lugares import views as lugares_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/lugares/', permanent=True)),
    path('lugares/', include('lugares.urls')),
    
    path('accounts/login/', lugares_views.login_view, name='login'),
    path('accounts/register/', lugares_views.register, name='register'),
    
    path('accounts/logout/', lugares_views.logout_view, name='logout'),

]