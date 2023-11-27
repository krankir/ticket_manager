from src.dao.base import BaseDAO
from src.ticket.models import Ticket


class TicketDAO(BaseDAO):
    model = Ticket
