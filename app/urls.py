from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.views.generic import RedirectView

from . import views


urlpatterns = [
    path('', RedirectView.as_view(url='/home/', permanent=True)),
    path('signup/', views.signup, name='signup'),
    path('home/', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('myorders/create/', views.ordercreate, name='order-create'),
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
