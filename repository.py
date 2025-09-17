from ticket import Ticket
from database import DatabaseConnection


class TicketRepository:
    '''Класс-репозиторий для доступа к БД'''

    def __init__(self, connection: DatabaseConnection):
        self.connection = connection

    def create_ticket(self, ticket: Ticket):
        """Добавление билета"""

        conn = self.connection.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO tickets
                        (plane,price, name_movie, price)
                        VALUES (%s,%s,%s,%s)
            ''', (ticket.row, ticket.place, ticket.name_movie, ticket.price ))
        conn.commit()

        cursor.close()
        conn.close()

        return ticket

    def get_all(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickets ORDER BY id")
        rows = cursor.fetchall()

        tickets = []
        for row in rows:
            tickets.append(Ticket(
                row[0],
                row[1],
                row[2]
            ))

        cursor.close()
        conn.close()
        return tickets

    def get_by_id(self, ticket_id: int):
        """Получить билет по идентификатору"""
        conn = self.connection.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tickets WHERE id = %s", (ticket_id,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row:
            return Ticket(
                row[0],
                row[1],
                row[2]
            )
        return None

    def update_ticket(self, ticket: Ticket):
        """Изменить существующий рейс.
            Если рейса не существует, ничего не делать."""
        conn = self.connection.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE tickets
            SET price = %s, plane = %s
            WHERE id = %s
            ''', (ticket.prise, ticket.name_movie, ticket.id, ticket.row, ticket.place))

        result = cursor.fetchone()
        ticket.id = result[0]
        conn.commit()

        cursor.close()
        conn.close()

        return ticket

    def delete_ticket(self, ticket_id: int):
        """Удалить существующий рейс.
            Если рейса не существует, ничего не делать."""
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM tickets WHERE id = %s
            ''', (ticket_id,))
        conn.commit()
        deleted = cursor.rowcount

        cursor.close()
        conn.close()

        return deleted > 0