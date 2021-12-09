import os


class CreateFile:
    def create():
        if not os.path.exists("market1.db"):
            try:
                f = open("market1.db", "x")
            except Exception:
                pass
        if not os.path.exists("market2.db"):
            try:
                f = open("market2.db", "x")
            except os.error:
                pass
