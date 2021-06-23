import mysql.connector

from lib import config


class Helpers():
    def fix_date(self, date):
        if date < 10:
            new_format = '0'+str(date)
        else:
            new_format = str(date)
        
        return new_format

    def db_consult(self, consult):
        if consult:
            db = mysql.connector.connect(
                host = config.host,
                user = config.user,
                password = config.password,
                database = config.database
            )

            cursor = db.cursor()
            sql = consult
            cursor.execute(sql)
            db_data = sorted(cursor.fetchall())
            db.close()
        else:
            db_data = None

        return db_data

    def db_update(self, update):
        if update:
            db = mysql.connector.connect(
                host = config.host,
                user = config.user,
                password = config.password,
                database = config.database
            )

            cursor = db.cursor()
            sql = update
            cursor.execute(sql)
            db.commit()
            db.close()

        return None