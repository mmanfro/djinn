from django import template

from inc_mgmt.models import Ticket


register = template.Library()

@register.filter
def area_ticket_status_count(value, arg):
    status = arg
    count = Ticket.objects.all().filter(area=value, status=status).count()
    return count