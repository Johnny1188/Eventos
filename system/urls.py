from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('e'+'<int:event_id>/', views.eventPage, name="eventpage"),
    path('mypage/<int:user_id>/', views.myPage, name="myrewards"),
    path('newrewardcollector/<int:event_id>/', views.newRewardCollector, name="newcollector"),
    path('mybuddies/<int:user_id>/', views.myBuddies, name="mybuddies"),
    path('settings/<int:user_id>/', views.settingsPage, name="settingspage"),
    path('e'+'<int:event_id>/<int:user_id>/', views.recommendedEventPage),
    path('events', views.eventlist, name="eventlist"),
    path('rewarder/<int:rewID>/', views.getReward, name="rewarder"),
    path('changepreference', views.changePreference),
    path('chat', views.ajaxGetOlderMessages),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)