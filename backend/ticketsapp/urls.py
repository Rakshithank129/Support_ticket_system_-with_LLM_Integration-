from rest_framework.routers import DefaultRouter
from ticketsapp.views import TicketViewSet

router = DefaultRouter()
router.register(r'tickets', TicketViewSet, basename='ticket')

urlpatterns = router.urls