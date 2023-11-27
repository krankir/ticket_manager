from pydantic import BaseModel


class TicketS(BaseModel):
    client_id: int
    employee_id: int
