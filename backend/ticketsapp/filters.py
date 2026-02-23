import django_filters # type: ignore
from ticketsapp.models import Ticket

class TicketFilter(django_filters.FilterSet):
    class Meta:
        model = Ticket
        fields = ['category', 'priority', 'status']

