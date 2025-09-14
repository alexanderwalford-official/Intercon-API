import datetime as dt
import os

SYSTEM_LOG_FILE_NAME = "system.log"

class systemlogger:
    def __init__(self):
        pass

    def LogEntry(self, value: str, elevation: int = 0):
        str_prep = ""
        if elevation > 0:
            str_prep = str_prep + "[ X ] "
        else:
            str_prep = str_prep + "[ ! ] "
        str_prep = str_prep + " [" + dt.datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + "] "
        str_prep = str_prep + value + "\n"
        print(str_prep)
        if not os.path.exists(SYSTEM_LOG_FILE_NAME):
            open(SYSTEM_LOG_FILE_NAME, "x")
        with open(SYSTEM_LOG_FILE_NAME, "a") as f:
            f.write(str_prep)