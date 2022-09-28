from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView

from . import views

urlpatterns = [
                  path('', RedirectView.as_view(url='/home/', permanent=True)),
                  path('signup/', views.signup, name='signup'),
                  path('home/', views.index, name='index'),
                  path('profile/', views.profile, name='profile'),
                  path('myorders/create/', views.ordercreate, name='order-create'),
                  path('myorders/', views.OrdersByUserListView.as_view(), name='myorders'),
                  path('order/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
                  path('order/<int:pk>/delete', views.OrderDeleteView.as_view(), name='order-delete'),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('orders/', views.AllOrdersListView.as_view(), name='all-orders'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
