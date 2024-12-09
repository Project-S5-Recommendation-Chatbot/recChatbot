import psycopg2  # Import psycopg2 to work with PostgreSQL

# Define a class to manage PostgreSQL database connection
class ConnectionPostgreSQLDB:
    def __init__(self, host, user, password, database):
        """
        Initialize the database connection details.
        :param host: Database host
        :param user: Database user
        :param password: User's password
        :param database: Database name
        """
        self.host = host  # Database host
        self.user = user  # Username
        self.password = password  # Password
        self.database = database  # Database name
        self.connection = None  # Placeholder for the connection object

    def connect(self):
        """
        Establish a connection to the PostgreSQL database.
        :return: A connection object
        """
        self.connection = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            dbname=self.database
        )  # Connect to the database
        return self.connection  # Return the connection object

    def close(self):
        """
        Close the database connection if it is open.
        """
        if self.connection:  # Check if the connection exists
            self.connection.close()  # Close the connection
