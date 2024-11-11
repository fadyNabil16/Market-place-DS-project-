import os


class CreateFile:
    def create() -> None:
        """ 
        create function is used to create automatically Db file if its Not created 
        """
        if not os.path.exists("market1.db"):
            try:
                f = open("market1.db", mode="x")
            except TypeError as err:
                print(err)

        if not os.path.exists("market2.db"):
            try:
                f = open("market2.db", "rx")
            except os.error:
                pass
