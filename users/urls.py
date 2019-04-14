from django.conf.urls import url

from users.views import SignUpView, InviteUserView, ListUserView

urlpatterns = [
    url(r'^signup/$', SignUpView.as_view(), name='user-signup'),  # Signup POST method
    url(r'^invite-user/$', InviteUserView.as_view(), name='invite-user'),  # Invokes invite user via email.
    url(r'^list-users/$', ListUserView.as_view(), name='list-users'),  # lists users for admin.
]
