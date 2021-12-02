import sqlite3
from sqlite3 import Error
from sqlite3.dbapi2 import Row
from hashlib import sha256


class Database:
    def __init__(self):
        try:
            self.connected_1 = sqlite3.connect(
                r"C:\sqlite\\market1.db")
            self.connected_2 = sqlite3.connect(
                r"C:\sqlite\\market2.db")
            self.cursorObj_1 = self.connected_1.cursor()
            self.cursorObj_2 = self.connected_2.cursor()
            self.createTables()
        except Error as e:
            print(e)

    """ 
        :params -> table_name  table will be created in database
        :params -> db_code  database number like 1 or 2 or 3
    """

    def createTable(self, table_name):
        try:
            self.cursorObj_1.execute(table_name)
            self.cursorObj_2.execute(table_name)
        except Error as e:
            print(e)

    # internal use
    # structure of tables
    def createTables(self):
        create_user_table = """
            CREATE TABLE IF NOT EXISTS USER(
                id CHAR(32) PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                isAdmin BOOLEAN DEFAULT FALSE,
                store Text DEFAULT NULL,
                cash INT DEFAULT NULL,
                location CHAR(4)
            );
        """
        create_item_table = """
            CREATE TABLE IF NOT EXISTS ITEM(
                name KEY TEXT NOT NULL,
                image TEXT DEFAULT NULL,
                brand TEXT,
                price FLOAT NOT NULL,
                quantity INT NOT NULL,
                sold BOOLEAN DEFAULT FALSE,
                want_to_sell CHAR(32) DEFAULT NULL,
                itemOwner CHAR(32) NOT NULL,
                FOREIGN KEY(itemOwner) REFERENCES USER(id) ON DELETE CASCADE ON UPDATE CASCADE
            );
        """
        create_history_table = """
            CREATE TABLE IF NOT EXISTS HISTORY(
                owner KEY CHAR(32) NOT NULL,
                seller_assistant CHAR(32) DEFAULT NULL,
                buyer CHAR(32) NOT NULL,
                itemId INT NOT NULL,
                payments INT NOT NULL,
                name TEXT NOT NULL,
                quantity INT NOT NULL
            );
        """
        tables = [
            create_user_table, create_history_table,
            create_item_table
        ]
        if self.connected_1 is not None and self.connected_2 is not None:
            for ele in tables:
                self.createTable(ele)

    # use to insert

    def insert_to_database(self, type, my_tuple):
        if type == "user":
            sql = ''' INSERT INTO USER(id, email, password, isAdmin, name, store, location)
                VALUES(?,?,?,?,?,?,?) '''
            self.location(my_tuple[6])
            y = list(my_tuple)
            y[2] = sha256(y[2].encode('utf-8')).hexdigest()
            my_tuple = tuple(y)
        elif type == "history":
            sql = ''' INSERT INTO HISTORY(owner, seller_assistant, buyer, itemId, payments, name, quantity)
                VALUES(?,?,?,?,?,?,?) '''
        elif type == "item":
            sql = ''' INSERT INTO ITEM(name, brand, price, quantity, itemOwner)
                VALUES(?,?,?,?,?) '''
        if self.db_code == 1:
            self.connected_1.cursor().execute(sql, my_tuple)
            self.connected_1.commit()
        else:
            self.connected_2.cursor().execute(sql, my_tuple)
            self.connected_2.commit()

    # check if user exists
    def check_user(self, email="", password=""):
        if email is not None and password is not None:
            sql = '''SELECT * FROM USER WHERE email = ? and password = ?;'''
            user_tuple = (email, sha256(password.encode('utf-8')).hexdigest())
            rows = self.select_db(sql, user_tuple, 1)
            _rows = self.select_db(sql, user_tuple, 2)
            if rows != []:
                self.location(rows[0][7])
                return rows
            else:
                if _rows != []:
                    self.location(_rows[0][7])
                    return _rows
                else:
                    return False
        else:
            return False
    # get amont of cash

    def add_cash_amuont(self, amount, from_id):
        if amount is not None:
            sql = '''SELECT cash FROM USER WHERE id = ?;'''
            cash_tuple = (from_id,)
            rows = self.select_db(sql, cash_tuple, self.db_code)
            sql_2 = '''UPDATE USER SET cash = ? WHERE id = ?'''
            if rows[0][0] is not None:
                cash_tuple = (amount + rows[0][0], from_id)
            else:
                cash_tuple = (amount, from_id)
            if self.db_code == 1:
                self.connected_1.cursor().execute(sql_2, cash_tuple)
                self.connected_1.commit()
            else:
                self.connected_2.cursor().execute(sql_2, cash_tuple)
                self.connected_2.commit()
        else:
            error = "add mount of money"
            print(error)

    # select from database any select
    def select_db(self, sql, select_tuple, db_code):
        if db_code == 1:
            cur = self.connected_1.cursor()
            rows = cur.execute(sql, select_tuple).fetchall()
        else:
            cur = self.connected_2.cursor()
            rows = cur.execute(sql, select_tuple).fetchall()
        return rows

    def delete_form_db(self, item_tuple):
        sql_item = '''DELETE FROM ITEM WHERE itemOwner = ? and name = ? and sold is False and rowid = ?'''
        if self.db_code == 1:
            self.connected_1.cursor().execute(sql_item, item_tuple)
            self.connected_1.commit()
        else:
            self.connected_2.cursor().execute(sql_item, item_tuple)
            self.connected_2.commit()

    def update_db(self, property, item_tuple):
        sql_item = '''UPDATE ITEM SET {change} = ? WHERE itemOwner = ? and sold is False and name =? and rowid = ?'''
        sql_item = sql_item.format(change=property)
        if self.db_code == 1:
            self.connected_1.cursor().execute(sql_item, item_tuple)
            self.connected_1.commit()
        else:
            self.connected_2.cursor().execute(sql_item, item_tuple)
            self.connected_2.commit()
    # search for item in database

    def search(self, userId, name):
        sql = '''SELECT rowid,* FROM ITEM WHERE itemOwner NOT IN (?) AND name = ? AND quantity > 0 AND (want_to_sell NOT IN (?) OR want_to_sell IS NULL);'''
        my_tuple = (userId, name, userId,)
        rows = self.select_db(sql, my_tuple, self.db_code)
        if len(rows) > 0:
            return rows
        else:
            return False

    def want_to_sell(self, item_tuple):
        sql_item = '''UPDATE ITEM SET want_to_sell = ? WHERE quantity > 0 and name =? and rowid = ? AND itemOwner NOT IN (?)'''
        if self.db_code == 1:
            self.connected_1.cursor().execute(sql_item, item_tuple)
            self.connected_1.commit()
        else:
            self.connected_2.cursor().execute(sql_item, item_tuple)
            self.connected_2.commit()

    def location(self, ele):
        if ele == "east":
            self.db_code = 1
        else:
            self.db_code = 2
