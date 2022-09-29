from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView

from . import views

urlpatterns = [

                  path('', RedirectView.as_view(url='/home/', permanent=True)),
                  path('signup/', views.signup, name='signup'),
                  path('home/', views.Index.as_view(), name='index'),
                  path('myorders/create/', views.ordercreate, name='order-create'),
                  path('myorders/', views.OrdersByUserListView.as_view(), name='myorders'),
                  path('order/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
                  path('order/<int:pk>/delete', views.OrderDeleteView.as_view(), name='order-delete'),
                  path('order/<int:pk>/status-change', views.statuschange, name='status-change'),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('orders/', views.AllOrdersListView.as_view(), name='all-orders'),
                  path('order/<int:pk>/complete-order/', views.CompleteStatusChange.as_view(), name='complete-order'),
                  path('orders/delete', views.deletecategory, name='delete-category'),
                  path('orders/add', views.CategoryAdd.as_view(), name='add-category'),
                  path('order/<int:pk>/accepted-order/', views.AcceptedStatusChange.as_view(), name='accepted-order'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
