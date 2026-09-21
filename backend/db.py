import pyodbc
def get_connection():
    connection = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=PottoDB;"
        "Trusted_Connection=yes;"
    )
    return connection
try:
    connection = get_connection()
    print("Successfully connected to PottoDB!")
    connection.close()
except Exception as error:
    print("Database connection failed:")
    print(error)