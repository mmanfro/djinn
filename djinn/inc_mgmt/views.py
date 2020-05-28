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

def self_register(request):
    area_list = Area.objects.all().order_by('name')
    context = {'area_list': area_list}
    if request.method == 'POST':
        form = UserSelfCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            context['register_success'] = True
            return render(request, 'registration/register.html', context)
    else:
        return render(request, 'registration/register.html', context)

def index(request):
    return area_list(request)

@login_required(login_url='/login')
def area_list(request):
    area_list = Area.objects.all().filter(user__id=request.user.id)
    context = {'area_list': area_list}
    return render(request, 'inc_mgmt/area_list.html', context)

@login_required(login_url='/login')
def ticket_list(request, area_name):
    get_object_or_404(request.user.areas.all().filter(name=area_name))
    
    area_ticket_list = Ticket.objects.all().filter(area_id=Area.objects.all().filter(name=area_name)[0]).order_by('-time_created')
    page = request.GET.get('page', 1)
    paginator = Paginator(area_ticket_list, 20)
    try:
        p_area_ticket_list = paginator.page(page)
    except PageNotAnInteger:
        p_area_ticket_list = paginator.page(1)
    except EmptyPage:
        p_area_ticket_list = paginator.page(paginator.num_pages)
        
    context = {'area_ticket_list': p_area_ticket_list,
               'area_name': area_name,
               }
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
