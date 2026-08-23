import mysql.connector
import threading

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Ish123###",
    "database": "medicinereminderdb"
}

_local = threading.local()


def open_connection():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor(dictionary=True)

    _local.connection = connection
    _local.cursor = cursor

    return connection, cursor


def get_current():
    connection = getattr(_local, "connection", None)
    cursor = getattr(_local, "cursor", None)

    if connection is None or cursor is None:
        return open_connection()

    try:
        connection.ping(
            reconnect=True,
            attempts=1,
            delay=0
        )
    except mysql.connector.Error:
        release_connection()
        return open_connection()

    return connection, cursor


def release_connection():
    cursor = getattr(_local, "cursor", None)
    connection = getattr(_local, "connection", None)

    try:
        if cursor is not None:
            cursor.close()
    finally:
        if connection is not None:
            connection.close()

    _local.cursor = None
    _local.connection = None


class CursorProxy:

    def execute(self, query, params=None):
        connection, cursor = get_current()

        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)

    def fetchone(self):
        cursor = getattr(_local, "cursor", None)

        try:
            return cursor.fetchone()
        finally:
            release_connection()

    def fetchall(self):
        cursor = getattr(_local, "cursor", None)

        try:
            return cursor.fetchall()
        finally:
            release_connection()


class ConnectionProxy:

    def commit(self):
        connection = getattr(_local, "connection", None)

        if connection is not None:
            try:
                connection.commit()
            finally:
                release_connection()

    def rollback(self):
        connection = getattr(_local, "connection", None)

        if connection is not None:
            try:
                connection.rollback()
            finally:
                release_connection()


cursor = CursorProxy()
connection = ConnectionProxy()