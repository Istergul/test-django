from django.conf.urls import patterns, url

urlpatterns = patterns('app.views',
    url(r'^get-users$', 'get_users', name='get_users'),
    url(r'^add-user$', 'add_user', name='add_user'),
    url(r'^update-user$', 'update_user', name='update_user'),
    url(r'^get-rooms$', 'get_rooms', name='get_rooms'),
    url(r'^add-room$', 'add_room', name='add_room'),
    url(r'^update-room$', 'update_room', name='update_room'),
)
