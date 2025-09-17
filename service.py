from repository import ticketRepository
from ticket import ticket


class ticketervice:
    def __init__(self, repository: ticketRepository):
        self.repository = repository

    def create_ticket(self, ticket: ticket):
        """Добавление рейса"""
        return self.repository.create_ticket(ticket)

    def get_all(self):
        '''Получить все полёты'''
        return self.repository.get_all()

    def get_by_id(self, ticket_id: int):
        '''Получить полёт по id'''
        return self.repository.get_by_id(ticket_id)

    def update_ticket(self, ticket: ticket):
        """Изменить существующий рейс. 
            Если рейса не существует, ничего не делать."""
        return self.repository.update_ticket(ticket)

    def delete_ticket(self, ticket_id: int):
        """Удалить существующий рейс.
            Если рейса не существует, ничего не делать."""
        return self.repository.delete_ticket(ticket_id)