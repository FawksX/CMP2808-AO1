import os
import logging

from MySQLdb import Connection
from MySQLdb import Connect
from MySQLdb.cursors import Cursor


"""
SQL Connection Details from .env file
"""
SQL_HOST = os.getenv('SQL_HOST')
SQL_USER = os.getenv('SQL_USER')
SQL_PORT = os.getenv('SQL_PORT')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')
SQL_DATABASE = os.getenv('SQL_DATABASE')

LOGGER = logging.getLogger("SqlDatabaseHandler.py")
logging.basicConfig(level=logging.DEBUG)

class SqlDatabaseHandler:
    def __init__(self):
        self.initializeConnection()

    def initializeConnection(self):
        
        if not hasattr(self, "connection") or not hasattr(self, "cursor"):
            self.createConnectionAndCursor()
        else:
            LOGGER.info("Reconnecting to MySQL Database...")
            self.closeConnection()
            self.createConnectionAndCursor()

    def createConnectionAndCursor(self):
        self.connection: Connection = Connect(
            host=SQL_HOST,
            port=int(SQL_PORT),
            user=SQL_USER,
            password=SQL_PASSWORD,
            database="adventureworks2019"
        )
        self.cursor: Cursor = self.connection.cursor(cursorclass=Cursor)

    def closeConnection(self):
        try:
            LOGGER.info("Closing SQL Connection...")
            self.cursor.close()
            self.connection.close()

            delattr(self, "cursor")
            delattr(self, "connection")

            LOGGER.info("SQL Connection Closed!")
        except Exception as exception:
            LOGGER.critical("Could not close SQL Connection!")
            LOGGER.critical(exception)
    
    def commit(self):
        self.connection.commit()

    def getCursor(self) -> Cursor:
        # First, check that the connection has been initialized
        #self.initializeConnection()
        return self.cursor

sqlDatabaseHandler = SqlDatabaseHandler()

