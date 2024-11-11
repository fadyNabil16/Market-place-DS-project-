from createFiles import CreateFile
from database import Database
from user import User
import sys
from PyQt5.QtWidgets import *
from welcome import WelcomeScreen


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     ex = WelcomeScreen()
#     sys.exit(app.exec_())
    #     CreateFile.create()
    #     method = input("Sign Up or Login > ")
    #     email = input("enter your email > ")
    #     password = input("enter password > ")
    #     loged_in = ""
    #     my_db = Database()
    #     user = User(my_db, email, password, method)
    #     loged_in = user.enter_app()
    #     falg_x1 = False
    # # check if loged in
    #     if loged_in == False:
    #         print("user not registered")
    #     else:
    #         loged_id = loged_in[0][0]  # user id to use###########
    #         total_cash = loged_in[0][6]
    #         falg_x1 = True
    #         # print(loged_in)

    #     if falg_x1 == True:
    #         # add cash to account
    #         user.add_cash(300, loged_id)

    #         """
    #             in order -> name, image uri, user id, brand, price, quantity, store id
    #         """
    #         user.item_in_store("add", "koko", None,
    #                            "kik23", 250.6, 2, loged_id)

    #         # user id, name of item, rowid
    #         # user.item_in_store("delete", loged_id, "koko", 12)

    #         # image to change, url of img, userid, name of item, rowid
    #         #user.item_in_store("edit", "image", "lolll", loged_id, "koko", 2)

    #         _1 = input("search for  ")
    #         # return false or list of items
    #         search_result = user.search(loged_id, _1)
    #         # print(search_result)
    #         if search_result is not False:
    #             rowid = search_result[0][0]
    #             # id of user, name of item , rowid
    #             #user.want_to_sell(loged_id, "koko", 3)
    #             # must throw id not owned by the user
    #             #   user.buy_item(loged_id, "rowid", "ownerid", "seller_Ass", "price")
    #             user.buy_item(loged_id, rowid, 2)
    #         else:
    #             print("not found")
