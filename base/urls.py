from django.urls import include,re_path,path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve 


urlpatterns = [
    path('',views.home),
    re_path(r'signup/$',views.signup),
    re_path(r'login/$',views.login),
    re_path(r'logout/$',views.logout),
    re_path(r'profilepage/$',views.profilepage),
    re_path(r'show-profile/(?P<username>\d+)/$',views.show_profile),
    re_path(r'add-comment/(?P<post_id>\d+)/$',views.add_comment),
    re_path(r'show-comment/(?P<post_id>\d+)/$',views.show_comment),
    re_path(r'edit-profile-picture/$',views.edit_profile_pictute),
    re_path(r'edit-profile/$',views.edit_profile),
    re_path(r'like-post/(?P<post_id>\d+)/$',views.add_like),
    re_path(r'like-post-profile/(?P<post_id>\d+)/$',views.add_like_profile),
    re_path(r'delet-post/(?P<post_id>\d+)/$',views.delet_post),
    re_path(r'search/',views.search),
    re_path(r'show-post/(?P<post_id>\d+)/(?P<notification_id>\d+)/$',views.show_post),
    re_path(r'createthread/$',views.create_thread),
    re_path(r'inbox/(?P<thread_id>\d+)/(?P<notification_id>\d+)/$',views.inbox),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),     
]

handeler404= 'base.views.error_404_views'