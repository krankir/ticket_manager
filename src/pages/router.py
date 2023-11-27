from fastapi import APIRouter, Request, Depends, Form, WebSocket
from fastapi.templating import Jinja2Templates

from src.dao.base import BaseDAO
from src.ticket.dao import TicketDAO
from src.users.dao import ClientDAO
from src.users.dependencies import get_ticket_inspector_user
from src.users.models import Users

router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory='src/templates')


async def get_ws(websocket: WebSocket):
    return websocket


@router.get('')
async def get_all_tickets_page(
        request: Request,
        current_user: Users = Depends(get_ticket_inspector_user)
):
    """Проверяет на право редактирования и открывает только закреплённые за
     сотрудником тикеты."""
    tickets = await TicketDAO.find_all(employee_id=current_user.id)
    return templates.TemplateResponse(
        "tickets.html",
        {
            "request": request,
            "tickets": tickets
        }
    )


@router.post("/chat_client")
async def logs_pod(
        request: Request,
        uid_ticket: str = Form(...),
        employee_id: str = Form(...),
        client_id: str = Form(...),
        ticket_id: str = Form(...),
        current_user: Users = Depends(get_ticket_inspector_user)
):
    """Тригер создания чата с клиентом, чат может создать только
    уполномоченное лицо."""
    if current_user.id == int(employee_id):
        ticket_id = int(ticket_id)
        employee_id = int(employee_id)
        uid_ticket = uid_ticket
        client_id = int(client_id)
        res = await ClientDAO.find_one_or_none(id=client_id)
        telegram_id = res.get('telegram_id')
        return templates.TemplateResponse("chat.html",
                                          {
                                              "request": request,
                                              "uid_ticket": uid_ticket,
                                              "client_id": client_id,
                                              "telegram_id": telegram_id,
                                              "employee_id": employee_id,
                                              "ticket_id": ticket_id,
                                          }
                                          )
