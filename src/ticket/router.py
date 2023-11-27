import datetime

from fastapi import APIRouter, Depends

from src.exceptions import TicketIsNotClosed
from src.ticket.dao import TicketDAO
from src.ticket.models import StatusEnum
from src.ticket.schemas import TicketS

router = APIRouter(
    prefix='/ticket',
    tags=['tickets job']
)


@router.post('/add')
async def add_ticket(ticket_data: TicketS):
    tickets_user = await TicketDAO.find_all(client_id=ticket_data.client_id)
    if tickets_user:
        for ticket in tickets_user:
            if ticket.get('status') == StatusEnum.OPENED:
                raise TicketIsNotClosed
    created_at = datetime.datetime.utcnow()
    await TicketDAO.add(
        client_id=ticket_data.client_id,
        employee_id=ticket_data.employee_id,
        created_at=created_at
    )


@router.post('/update_status/{ticket_id}')
async def partial_update(ticket_id: int, status: StatusEnum):
    await TicketDAO.partial_update(
        id=ticket_id,
        status=status,
    )


@router.get('/all')
async def get_all_tickets():
    tickets = await TicketDAO.find_all()
    return tickets
