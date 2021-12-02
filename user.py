import uuid


class User:
    def __init__(self, DB, email, password, method):
        self.db = DB
        self.email = email
        self.password = password
        self.method = method  # login -> 0 or signup -> 1
############################## logging methods ############################

    def enter_app(self):
        my_user = ""
        if self.method == "0":
            name = input("name  ")
            location = input("Enter your location east or west  ")
            store_name = input("enter store name  ")
            if location == "e" or location == "east" or location == "1":
                location = "east"
            else:
                location = "west"
            my_user = self.signUp(name, store_name, location)
            return my_user
        else:
            my_user = self.login()
            return my_user

    def login(self):
        user = self.db.check_user(self.email, self.password)
        if(user == False):
            return False
        else:
            return user

    def signUp(self, name, store_name, location, isAdmin=False):
        ID = uuid.uuid1().hex
        user_tuple = (ID, self.email,
                      self.password, isAdmin, name, store_name, location)
        user = self.login()
        if user is False:
            self.db.insert_to_database("user", user_tuple)
            user = self.login()  # after signup is login
            return user
        else:
            return user

    def add_cash(self, amount, userId):
        self.db.add_cash_amuont(amount, userId)
#################################end logging methods ######################

################################manipulate item#########################
    """ 
        :args[0] -> name
        :args[1] -> image
        :args[2] -> brand
        :args[3] -> price
        :args[4] -> quantity
        :args[5] -> userId
    """

    def item_in_store(self, method, *args):
        if method == "add":  # add item to database
            item_tuple = (args[0], args[2], args[3],
                          args[4], args[5],)
            self.db.insert_to_database("item", item_tuple)
        elif method == "delete":
            item_tuple = (args[0], args[1], args[2],)
            self.db.delete_form_db(item_tuple)
        elif method == "edit":
            item_tuple = (args[1], args[2], args[3], args[4],)
            self.db.update_db(args[0], item_tuple)

    def search(self, userId, name):
        result = self.db.search(userId, name)
        if result is False:
            return False
        else:
            return result
    # to requests to sell an item
    # userid of me, name of item, rowid

    def want_to_sell(self, *args):
        item_tuple = (args[0], args[1], args[2], args[0],)
        self.db.want_to_sell(item_tuple)
    """ 
        :args[0] -> userid want to buy
        :args[1] -> rowid
    """

    def buy_item(self, buyerId, rowid, quantity):
        sql = '''SELECT * FROM USER WHERE id = ?;'''
        user_tuple = (buyerId,)
        rows = self.db.select_db(sql, user_tuple, self.db.db_code)
        cash_flow = rows[0][6]
        sql = '''SELECT * FROM ITEM WHERE rowid = ?;'''
        item_tuple = (rowid,)
        _rows = self.db.select_db(sql, item_tuple, self.db.db_code)
        owner, seller_ass, quanti, price = _rows[0][7], _rows[0][6], _rows[0][4], _rows[0][3]
        if cash_flow is not None:
            if quanti >= quantity and (price * quantity) <= cash_flow:
                sql = '''UPDATE ITEM SET quantity = ? WHERE rowid = ?'''
                his_tuple = (owner, seller_ass, buyerId,
                             rowid, price * quantity, _rows[0][0], quantity)
                self.db.insert_to_database("history", his_tuple)
                sql_1 = '''UPDATE USER SET cash = ? WHERE id = ?'''
                sql_perment = '''SELECT * FROM USER WHERE id = ?'''
                _perment = (_rows[0][7],)
                __perment = self.db.select_db(sql_perment, _perment)
                owner_cash = __perment[0][6]
                if owner_cash is None:
                    owner_cash = quantity * price
                else:
                    owner_cash = owner_cash + (quantity * price)
                _Q = (quanti - quantity, rowid,)
                user_tuple = (cash_flow - (price * quantity), buyerId,)
                owner_tuple = (owner_cash, owner,)
                if self.db.db_code == 1:
                    self.db.connected_1.cursor().execute(sql, _Q)
                    self.db.connected_1.commit()
                    self.db.connected_1.cursor().execute(sql_1, user_tuple)
                    self.db.connected_1.commit()
                    self.db.connected_1.cursor().execute(sql_1, owner_tuple)
                    self.db.connected_1.commit()
                else:
                    self.db.connected_2.cursor().execute(sql, _Q)
                    self.db.connected_2.commit()
                    self.db.connected_2.cursor().execute(sql_1, user_tuple)
                    self.db.connected_2.commit()
                    self.db.connected_2.cursor().execute(sql_1, owner_tuple)
                    self.db.connected_2.commit()
            else:
                print("we cant make the transaction")
        else:
            print("add cash first")

    #################################end store method###################################
