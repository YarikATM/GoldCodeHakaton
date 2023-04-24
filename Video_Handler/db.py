#TODO bd
import sqlite3


class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()


    def shipment_exists(self, time, img_path):
        sql = 'SELECT * FROM GoldCode_shipments WHERE time =? AND img =?'
        result = self.cursor.execute(sql, (time, img_path)).fetchmany(1)
        return bool(len(result))
    def add_shipment(self, time, img_path):
        sql = 'INSERT INTO GoldCode_shipments(time, img) VALUES (?,?)'
        self.cursor.execute(sql, (time, img_path))
        self.conn.commit()


