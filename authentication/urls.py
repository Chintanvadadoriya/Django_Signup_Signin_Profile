from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
# from django.conf.urls import url
from django.conf.urls.static import static

from authentication import views


urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('setcookie',views.setcookie,name='setcookie'),
    path('showcookie',views.showcookie,name='showcookie'),
    # path('update',views.updating_cookie,name='update'),
    # path('setcookie1',views.setcookie1,name='setcookie1'),
    # path('getcookie', views.showcookie1,name='getcookie'),
    # path('update1',views.updating_cookie1,name='update1'),
    # path('delet',views.deleting_cookie,name='delet'),
    path('ssession',views.setsession),  
    path('gsession',views.getsession),
    # path('index/', views.index),
    path('crop', views.photo_list, name='photo_list'),
      
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = [
#     url(r'^$', views.photo_list, name='photo_list'),
# ]


