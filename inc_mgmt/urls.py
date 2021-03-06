from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.views import LogoutView as logout, LoginView as login
from django.urls import path
from inc_mgmt import views as v


app_name = 'inc_mgmt'
urlpatterns = [
    url(r'^register/$', v.self_register, name='register'),
    url(r'^login/$', login.as_view(), {'next_page': settings.LOGIN_REDIRECT_URL}, name='login'),
    url(r'^logout/$', logout.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^register/confirm_account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', v.confirm_account, name='confirm_account'),
    url(r'^activate_account/list/$', v.activate_user_list, name='activate_user_list'),
    url('ajax/activate_account/', v.activate_user, name='activate_user'),
    path('', v.index, name='index'),
    path('<area_name>/ticket/list/', v.ticket_list, name='ticket_list'),
    path('<area_name>/ticket/list/<fast_status_filter>/', v.ticket_list, name='ticket_list'),
    path('<area_name>/ticket/new/', v.ticket_new, name='ticket_new'),
    path('<area_name>/ticket/<ticket_id>/detail/', v.ticket_detail, name='ticket_detail'),
    path('<area_name>/ticket/<ticket_id>/change/', v.ticket_change, name='ticket_change'),
    path('ajax/update_ticket/', v.ticket_update, name='ticket_update'),
]
