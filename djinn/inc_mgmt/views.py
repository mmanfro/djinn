from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from inc_mgmt.models import Area, Ticket, Status, Priority, User, TicketUpdate
from inc_mgmt.forms import TicketCreationForm, TicketUpdateForm,\
    TicketChangeForm, UserSelfCreationForm
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import Permission
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from inc_mgmt.token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.http import response
from django.contrib.auth import login, password_validation
from functools import reduce
import operator
import json


def self_register(request):
    area_list = Area.objects.all().order_by('name')
    context = {'area_list': area_list,
               'password_help_text': password_validation.password_validators_help_text_html(),}
    if request.method == 'POST':
        areas = request.POST.getlist('areas')
        context['selected_areas'] = areas
        form = UserSelfCreationForm(request.POST)
        context['form'] = form
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            user.areas.set(Area.objects.all().filter(name__in=areas))
            user.save()
            context['register_success'] = True
            
            # Send confirmation e-mail
            current_site = get_current_site(request)
            html_message = render_to_string('registration/email_confirmation.html', 
                                            {'user': user, 
                                            'domain': current_site.domain, 
                                            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                            'token':account_activation_token.make_token(user),})
            send_mail(
                'Activate your DJINN account',
                '',
                'djinnincmgmt@gmail.com',
                ['mauriciomanfro@gmail.com'],
#                 [user.email],
                html_message=html_message,
            )
        return render(request, 'registration/register.html', context)
    else:
        return render(request, 'registration/register.html', context)

def confirm_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_trusty = True
        user.save()
        login(request, user)
        return render(request, 'registration/confirm_account.html')
    else:
        return response('Activation link is invalid!')

@login_required(login_url='/login')
def index(request):
    return area_list(request)

@login_required(login_url='/login')   
def activate_user_list(request):
    user_list = User.objects.all().filter(is_active=False, is_trusty=True)
    context = {'user_list': user_list}
    return render(request, 'registration/activate_user_list.html', context)

@login_required(login_url='/login')
def activate_user(request):
    data = {'activated': False,}
    
    if request.method == "POST":
        user_id = json.loads(request.body)
        user = User.objects.get(pk=user_id)
        user.is_active = True
        user.save()
        data['activated'] = True
        
    return JsonResponse(data)

@login_required(login_url='/login')
def area_list(request):
    area_list = Area.objects.all().filter(user__id=request.user.id)
    status_list = Status.objects.all()
    context = {'area_list': area_list,
               'status_list': status_list}
    return render(request, 'inc_mgmt/area_list.html', context)

@login_required(login_url='/login')
def ticket_list(request, area_name, fast_status_filter=None):
    get_object_or_404(request.user.areas.all().filter(name=area_name))
    area_ticket_list = Ticket.objects.all().filter(area_id=Area.objects.all().filter(name=area_name)[0]).order_by('-time_created')
    status_list = Status.objects.all()
    context = {'status_list': status_list,}
    
    if fast_status_filter:
        area_ticket_list = area_ticket_list.filter(status__in=fast_status_filter)
        context['status_filter'] = Status.objects.all().filter(id__in=fast_status_filter)
        
    if request.method == 'GET':
        status_filter = request.GET.getlist('status-filter')
        title_descr_filter = request.GET.get('title-description-filter')
        atm_filter = request.GET.get('assigned-to-me')
        cbm_filter = request.GET.get('created-by-me')
        
        if status_filter:
            area_ticket_list = area_ticket_list.filter(status__in=status_filter)
            context['status_filter'] = Status.objects.all().filter(id__in=status_filter)
            print(status_filter)
        if title_descr_filter:
            title_descr_filter = title_descr_filter.split(' ')
            query1 = reduce(operator.or_, (Q(title__contains = word) for word in title_descr_filter))
            query2 = reduce(operator.or_, (Q(description__contains = word) for word in title_descr_filter))
            area_ticket_list = area_ticket_list.filter(query1 | query2)
            
            x = ''
            for i in range(len(title_descr_filter)):
                x += title_descr_filter[i] + ' '
            context['title_descr_filter'] = x
        if atm_filter:
            area_ticket_list = area_ticket_list.filter(assigned_to=request.user)
            context['atm_filter'] = atm_filter
        if cbm_filter:
            area_ticket_list = area_ticket_list.filter(created_by=request.user)
            context['cbm_filter'] = cbm_filter

    page = request.GET.get('page', 1)
    paginator = Paginator(area_ticket_list, 20)
    try:
        p_area_ticket_list = paginator.page(page)
    except PageNotAnInteger:
        p_area_ticket_list = paginator.page(1)
    except EmptyPage:
        p_area_ticket_list = paginator.page(paginator.num_pages)
        
    context['area_ticket_list'] = p_area_ticket_list
    context['area_name'] = area_name
    
    return render(request, 'inc_mgmt/ticket/list.html', context)

@login_required(login_url='/login')
def ticket_new(request, area_name):
    if request.method == "POST":
        file = request.FILES['file'] if request.FILES else None
        form = TicketCreationForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.area = Area.objects.all().filter(name=area_name)[0]
            ticket.created_by = request.user
            ticket.status = Status.objects.all().filter(status='Open')[0]
            ticket.priority = Priority.objects.all().filter(priority=request.POST.get('priority'))[0]
            ticket.file = None if file == 'undefined' else file
            ticket.save()
            
            return redirect('ticket_list', area_name=area_name)
    else:
        prioritiy_list = Priority.objects.all()
        context = {'area_name': area_name,
                   'priority_list': prioritiy_list,
                   }
        return render(request, 'inc_mgmt/ticket/new.html', context)

@login_required(login_url='/login')
def ticket_detail(request, ticket_id, area_name):
    ticket = Ticket.objects.all().filter(pk=ticket_id)[0]
    get_object_or_404(request.user.areas.all().filter(name=ticket.area))
    ticketupdate_list = TicketUpdate.objects.all().filter(ticket=ticket).order_by('-posted_time')
    context = {'ticket': ticket,
               'ticketupdate_list': ticketupdate_list,
               }
    if request.user.has_perm('inc_mgmt.change_ticket'):
        context['user_area_list'] = Area.objects.all().filter(user__id=request.user.id)
        context['priority_list'] = Priority.objects.all()
        context['status_list'] = Status.objects.all()
        
        perm = Permission.objects.get(codename='change_ticket')  
        context['user_assign_list'] = User.objects.all().filter(Q(groups__permissions=perm) | Q(user_permissions=perm) | Q(is_superuser=True), 
                                                                Q(areas=ticket.area)).distinct().order_by('name')
                                                                
    return render(request, 'inc_mgmt/ticket/detail.html', context)

def ticket_change(request, ticket_id, area_name):
    if request.method == "POST":
        form = TicketChangeForm(request.POST)
        if form.is_valid():
            ticket = Ticket.objects.all().filter(pk=ticket_id)[0]
            ticket.area = Area.objects.all().filter(name=request.POST.get('area'))[0]
            ticket.assigned_to = User.objects.all().filter(pk=request.POST.get('assigned_to'))[0]
            ticket.status = Status.objects.all().filter(status=request.POST.get('status'))[0]
            ticket.priority = Priority.objects.all().filter(priority=request.POST.get('priority'))[0]
            ticket.save()

    return redirect('ticket_detail', ticket_id=ticket_id)
            
def ticket_update(request):
    data = {'updated': False,
        }
    
    if request.method == "POST":
        ticket_id = request.POST.get('ticket_id', None)
        ticket = Ticket.objects.all().filter(pk=ticket_id)[0]
        ticketupdate_list = TicketUpdate.objects.all().filter(ticket=ticket).order_by('-posted_time')
        file = request.FILES['file'] if request.FILES else None
        form = TicketUpdateForm(request.POST)
        if form.is_valid():
            ticketupdate = form.save(commit=False)
            ticketupdate.ticket = ticket
            ticketupdate.file = file
            ticketupdate.created_by = request.user
            ticketupdate.save()
            data['ticketupdate_list_html'] = render_to_string('inc_mgmt/ticket/detail_update_list.html', {'ticketupdate_list': ticketupdate_list,})
            data['updated'] = True
            
    return JsonResponse(data)
