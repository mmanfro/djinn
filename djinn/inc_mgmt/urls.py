from django.conf import settings
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView as logout, LoginView as login
from inc_mgmt import views as v


app_name = 'inc_mgmt'
urlpatterns = [
    url(r'^register/$', v.self_register, name='register'),
    url(r'^login/$', login.as_view(), {'next_page': settings.LOGIN_REDIRECT_URL}, name='login'),
    url(r'^logout/$', logout.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('index/', v.index, name='index'),
    path('<area_name>/ticket/list/', v.ticket_list, name='ticket_list'),
    path('<area_name>/ticket/new/', v.ticket_new, name='ticket_new'),
    path('<area_name>/ticket/<ticket_id>/detail/', v.ticket_detail, name='ticket_detail'),
    path('<area_name>/ticket/<ticket_id>/change/', v.ticket_change, name='ticket_change'),
    path('ajax/update_ticket/', v.ticket_update, name='ticket_update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
