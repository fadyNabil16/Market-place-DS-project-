import sys
from createFiles import CreateFile
from database import Database
from user import User
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from utils import *


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("./ui/login.ui", self)
        password(self.password)
        self.login.clicked.connect(self.gotoprofile)
        self.signup.clicked.connect(self.gotosignup)

    def gotoprofile(self):
        if len(self.email.text()) > 0 and len(self.password.text()) > 0:
            global user, loged_in
            user = User(my_db, self.email.text(), self.password.text(), "1")
            loged_in = user.enter_app()
            if loged_in is not False:
                prof = Operation()
                widget.addWidget(prof)
                widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                self.error.setText("Not a user, or input error")

    def gotosignup(self):
        sign = Signup()
        widget.addWidget(sign)
        widget.setCurrentIndex(widget.currentIndex()+1)


class Signup(QDialog):
    def __init__(self):
        super(Signup, self).__init__()
        loadUi("./ui/signup.ui", self)
        password(self.password)
        self.signup.clicked.connect(self.gotoprofile)

    def gotoprofile(self):
        email = self.email.text().lower()
        name = self.name.text()
        password = self.password.text().lower()
        region = self.region.currentText().lower()
        store = self.store.text()
        if len(email) > 0 and len(name) > 0 and len(password) > 0 and len(store) > 0:
            global user, loged_in
            user = User(my_db, email, password, "0", name, region, store)
            loged_in = user.enter_app()
            if loged_in is not False:
                pp = Operation()
                widget.addWidget(pp)
                widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                self.error.setText("Already register, or error")


class Operation(QDialog):
    def __init__(self):
        global Self
        Self = self
        super(Operation, self).__init__()
        loadUi("./ui/operation.ui", self)
        self.vertical = QVBoxLayout()
        self.pro = Profile()
        self.vertical.addWidget(self.pro)
        self.change.setLayout(self.vertical)
        self.user.clicked.connect(self.gotoprofile)
        self.search.clicked.connect(self.gotosearch)
        self.history.clicked.connect(self.gotohistory)
        self.plus.clicked.connect(self.gotoproadd)

    def gotoprofile(self):
        self.vertical.itemAt(0).widget().deleteLater()
        self.pro = Profile()
        Self = self
        self.vertical.addWidget(self.pro)
        self.change.setLayout(self.vertical)

    def gotosearch(self):
        self.vertical.itemAt(0).widget().deleteLater()
        self.search = Search()
        self.vertical.addWidget(self.search)
        self.change.setLayout(self.vertical)

    def gotohistory(self):
        self.vertical.itemAt(0).widget().deleteLater()
        self.histor = History()
        self.vertical.addWidget(self.histor)
        self.change.setLayout(self.vertical)
    def gotoproadd(self):
        self.vertical.itemAt(0).widget().deleteLater()
        self.add = Add()
        self.vertical.addWidget(self.add)
        self.change.setLayout(self.vertical)
        self.add.adding.clicked.connect(self.add_in_store)

    def add_in_store(self):
        name = self.add.name.text().lower()
        url = self.add.url.text()
        brand = self.add.brand.text()
        price = self.add.price.text()
        quantity = self.add.quantity.text()
        if name != "" and url != "" and brand != "" and price != "" and quantity != "":
            user.item_in_store("add", name, url, brand, float(
                price), int(quantity), loged_in[0][0])
            self.add.error.setText("*Add to your account")
        else:
            self.add.error.setText("*All fieled required")

#user ptofile calss add to it items class to push in scroll area
class Profile(QDialog):
    def __init__(self):
        super(Profile, self).__init__()
        loadUi("./ui/profile.ui", self)
        self.first_screen()

    def first_screen(self):
        global tot_cash
        total = user.add_cash(0, loged_in[0][0])
        tot_cash = total[0]
        self.total.setText(str(total[0]))
        self.wid = QWidget()
        vertical = QVBoxLayout()
        items = user.user_items(loged_in[0][0])
        for i in items:
            item = Item(i[0])
            item.name.setText(i[1])
            item.brand.setText(i[3])
            item.quantity.setText(str(i[5]))
            item.price.setText(str(i[4]) + " $")
            vertical.addWidget(item)
        self.wid.setLayout(vertical)
        self.scroll.setWidget(self.wid)
        self.add.clicked.connect(self.add_money)

    def add_money(self):
        global tot_cash
        amount = self.money.text()
        if amount != "":
            amount = int(amount)
            total = user.add_cash(amount, loged_in[0][0])
            tot_cash = total[0]
            self.total.setText(str(total[0]))

class Item(QDialog):
    def __init__(self, rowid):
        super(Item, self).__init__()
        loadUi("./ui/item.ui", self)
        self.rowid = rowid
        self.edit.clicked.connect(self.editing)
        self.delet.clicked.connect(self.delete)

    def editing(self):
        if self.entry.text() != "":
            if self.list.currentText() == "price" or self.list.currentText() == "Quantity":
                self.lis = int(self.entry.text())
            else:
                self.lis = self.entry.text()
            user.item_in_store("edit", self.list.currentText(), self.lis,self.rowid)
            Self.gotoprofile()

    def delete(self):
        user.item_in_store("delete", loged_in[0][0], self.rowid)
        Self.gotoprofile()

class Search(QDialog):
    def __init__(self):
        super(Search, self).__init__()
        loadUi("./ui/search.ui", self)
        self.search_btn.clicked.connect(self.find)

    
    def find(self):
        search_key = self.search_entry.text().lower()
        if search_key != "":
            self.result = user.search(loged_in[0][0], search_key)
            self.wid = QWidget()
            self.vertical = QVBoxLayout()
            if self.result is not False:
                for i in self.result:
                    item = BuyItem(i[8], i[0], int(i[5]))
                    user_id = i[8]
                    store = user.store_nam(user_id)[0][0]
                    item.item_info(i[1],i[3],i[4],store)
                    self.vertical.addWidget(item)
                self.wid.setLayout(self.vertical)
                self.scroll.setWidget(self.wid)
            else:
                self.error.setText("not in stock")

class BuyItem(QDialog):
    def __init__(self, owner, rowid, qun):
        super(BuyItem, self).__init__()
        loadUi("./ui/item_buy.ui", self)
        self.buy.clicked.connect(self.buy_item)
        self.sell.clicked.connect(self.sell_item)
        self.owner = owner
        self.rowid = rowid
        self.qun = qun
    
    def item_info(self, *args):
        self._name = args[0]
        self.name.setText(args[0])
        self.brand.setText(args[1])
        self.pric = args[2]
        self.price.setText(str(args[2]))
        self.store.setText(args[3])
    
    def buy_item(self):
        if self.quantity.currentText() != "quantity":
            self.quantit = int(self.quantity.currentText())
            if self.quantit <= self.qun and tot_cash >= self.pric * self.quantit:
                user.buy_item(loged_in[0][0], self.rowid, self.quantit)
                self.error.setText("done!")
            else:
                self.error.setText("!enough cash or quantity")    
        else:
            self.error.setText("*Add quantity")

    def sell_item(self):
        user.want_to_sell(loged_in[0][0], self._name,self.rowid)
        self.error.setText("!thanks dear")

class History(QDialog):
    def __init__(self):
        super(History, self).__init__()
        loadUi("./ui/his_scroll.ui", self)
        self.wid = QWidget()
        self.vertical = QVBoxLayout()
        self.first_screen()

    def first_screen(self):
        buy, sell = user.history(loged_in[0][0])
        if buy != []:
            for i in buy:
                item = ItemHistory("buy",i[4],i[5],i[6])
                self.vertical.addWidget(item)
        if sell != []:
            for i in sell:
                item = ItemHistory("sell",i[4],i[5],i[6])
                self.vertical.addWidget(item)
        self.wid.setLayout(self.vertical)
        self.scroll.setWidget(self.wid)
class ItemHistory(QDialog):
    def __init__(self, *args):
        super(ItemHistory, self).__init__()
        loadUi("./ui/history.ui", self)
        if args[0] == "buy":
            self.operation.setText("Buy")
        else:
            self.operation.setText("Sell")
        self.payments.setText(str(args[1]))
        self.name.setText(args[2])
        self.quantity.setText(str(args[3]))
        

class Add(QDialog):
    def __init__(self):
        super(Add, self).__init__()
        loadUi("./ui/add.ui", self)


app = QApplication(sys.argv)
CreateFile.create()
my_db = Database()
user = None
loged_in = ""
Self = "" #address of operation object
tot_cash = 0
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedWidth(750)
widget.setFixedHeight(560)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("error")

    #         user.item_in_store("add", "koko", None,
    #                            "kik23", 250.6, 2, loged_id)
