from fastapi import FastAPI

from src.ticket.router import router as ticket_router
from src.users.router import router_auth, router_users
from src.chat.router import router as chat_router
from src.pages.router import router as pages_router


app = FastAPI(
    title='Ticket manager'
)

app.include_router(ticket_router)
app.include_router(router_auth)
app.include_router(router_users)
app.include_router(chat_router)
app.include_router(pages_router)
