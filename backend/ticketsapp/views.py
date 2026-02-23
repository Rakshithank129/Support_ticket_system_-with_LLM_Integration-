from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from ticketsapp.models import Ticket    
from ticketsapp.serializers import TicketSerializer
from ticketsapp.filters import TicketFilter
from django.db.models import Count, Avg
from django.db.models.functions import TruncDate
from rest_framework.decorators import action
from rest_framework.response import Response
from ticketsapp.services.llm_service import classify_ticket

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().order_by('-created_at')
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = TicketFilter
    ordering_fields = ['created_at']
    search_fields = ['title', 'description']

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        queryset = Ticket.objects.all()
        total_tickets = queryset.count()
        open_tickets = queryset.filter(status=Ticket.Status.OPEN).count()
        tickets_per_day = queryset.annotate(date=TruncDate('created_at')).values('date').annotate(count=Count('id'))
        avg_tickets_per_day = (tickets_per_day.aggregate(avg=Avg('count'))['avg'] or 0)

        priority_count = queryset.values('priority').annotate(count=Count('id'))
        priority_breakdown = {choice: 0 for choice, _ in Ticket.Priority.choices}
        for item in priority_count:
            priority_breakdown[item['priority']] = item['count']

        category_count = queryset.values('category').annotate(count=Count('id'))
        category_breakdown = {choice: 0 for choice, _ in Ticket.Category.choices}
        for item in category_count:
            category_breakdown[item['category']] = item['count']

        return Response({
            'total_tickets': total_tickets,
            'open_tickets': open_tickets,
            'avg_tickets_per_day': round(avg_tickets_per_day, 2),
            'priority_breakdown': priority_breakdown,
            'category_breakdown': category_breakdown
        })

    @action(detail=False, methods=['post'], url_path='classify')
    def classify(self, request):
        description = request.data.get('description')
        if not description:
            return Response({'error': 'Description is required'}, status=400)
        result = classify_ticket(description)
        if result is None:
            return Response({"suggested_category": None, "suggested_priority": None}, status=200)
        return Response(result, status=200)