from database import DatabaseConfig, DatabaseConnection


class MigrationManager:

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.connection = DatabaseConnection(self.config)

    def create_tables(self):
        # Initialize
        conn = self.connection.get_connection()
        cursor = conn.cursor()

        # Execution
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ticket(
                        id SERIAL PRIMARY KEY,
                        row  DECIMAL(10,2) NOT NULL
                        place DECIMAL(10,2) NOT NULL
                        name_movie VARCHAR(100) NOT NULL 
                        prise  DECIMAL(10,2) NOT NULL
                        )
            ''')
        conn.commit()

        # Deinitialize
        cursor.close()
        conn.close()