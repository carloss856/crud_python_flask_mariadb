import mariadb

def get_db():
    return mariadb.connect(
        host="127.0.0.1",
        port=3307,
        user="root",
        password="",
        database="python_flask_mariadb"
    )
