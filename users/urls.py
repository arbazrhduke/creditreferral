from django.conf.urls import url

from users.views import SignUpView, InviteUserView

urlpatterns = [
    url(r'^$', SignUpView.as_view(), name='user-signup'),
    url(r'^invite/$', InviteUserView.as_view(), name='invite-user'),
]
