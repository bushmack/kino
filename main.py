from database import DatabaseConfig, DatabaseConnection
from migrations import MigrationManager
from repository import ticketRepository
from service import ticketService
from fastapi import FastAPI, HTTPException
from ticket import ticket

# Initialize
## DB config
db_config = DatabaseConfig(
    'ticketsdb',
    'postgres',
    'postgres',
    '123Secret_a',
    5432
)
db_connection = DatabaseConnection(db_config)
## Migrations
migration_manager = MigrationManager(db_config)
migration_manager.create_tables()
# Repository and Service
repository = ticketRepository(db_connection)
service = ticketService(repository)

app = FastAPI(
    title="ticket API"
)


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI"}


@app.get("/tickets")
async def get_tickets():
    try:
        return service.get_all()
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Ошибка при получении полётов: {str(e)}")

@app.get("/tickets/{ticket_id}")
async def get_ticket_by_id(ticket_id: int):
    try:
        ticket = service.get_by_id(ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Полёт не найден")
        return ticket
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при получении полёта: {str(e)}")


@app.post("/tickets")
async def create_ticket(ticket_data: dict):
    try:
        # Validation
        required_fields = ["price", "plane"]
        for field in required_fields:
            if field not in ticket_data:
                raise HTTPException(status_code=400, detail=f"Отсутствует обязательное поле {field}")

        ticket = ticket(
            price=ticket_data['price'],
            plane=ticket_data['plane']
        )

        created_ticket = service.create_ticket(ticket)
        return created_ticket

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Ошибка при добавлении полёта: {str(e)}")

@app.put("/tickets/{ticket_id}")
async def update_ticket(ticket_id: int, ticket_data: dict):
    try:
        # Проверка наличия данных для обновления
        if not ticket_data:
            raise HTTPException(status_code=400, detail="Нет данных для обновления")
        # Создаем объект ticket с обновленными данными
        ticket = ticket(
            id=ticket_id,
            price=ticket_data.get('price'),
            plane=ticket_data.get('plane')
        )
        updated_ticket = service.update_ticket(ticket_id, ticket)
        if not updated_ticket:
            raise HTTPException(status_code=404, detail="Полёт не найден для обновления")
        return updated_ticket
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении полёта: {str(e)}")


@app.delete("/tickets/{ticket_id}")
async def delete_ticket(ticket_id: int):
    try:
        result = service.delete_ticket(ticket_id)
        if not result:
            raise HTTPException(status_code=404, detail="Полёт не найден для удаления")
        return {"message": "Полёт успешно удалён"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении полёта: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)