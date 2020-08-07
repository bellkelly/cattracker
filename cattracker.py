import logging
from datetime import datetime
from enum import Enum
import sys

import gspread
from evdev import InputDevice, ecodes
from oauth2client.service_account import ServiceAccountCredentials


LOG_LEVEL = logging.INFO
LOG_FILE = "logs/cattracker"
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)


SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]


SHEET_NAME = "NEW Cat Tracker 2020"

PUMPKIN_PEE_COLUMN = 1
PUMPKIN_POO_COLUMN = 2
PUMPKIN_PUKE_COLUMN = 3
PATCH_PEE_COLUMN = 4
PATCH_POO_COLUMN = 5
PATCH_PUKE_COLUMN = 6


GAMEPAD = InputDevice("/dev/input/event0")


class Button(Enum):
    X = 288
    A = 289
    B = 290
    Y = 291
    SELECT = 296
    START = 297


def get_current_month():
    now = datetime.now()
    return now.strftime("%B")

def get_current_sheet():
    client = login()
    month = get_current_month()
    return client.open(SHEET_NAME).worksheet(month)

def get_time_string():
    return datetime.now().strftime("%m/%d/%Y %I:%M %p")

def login():
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", SCOPES)
    return gspread.authorize(creds)

def log(col):
    sheet = get_current_sheet()
    row = len(sheet.col_values(col)) + 1
    sheet.update_cell(row, col, get_time_string())


BUTTON_MAPPING = {
    Button.Y.value: (PUMPKIN_PEE_COLUMN, "Pumpkin peed"),
    Button.X.value: (PUMPKIN_POO_COLUMN, "Pumpkin pooed"),
    Button.SELECT.value: (PUMPKIN_PUKE_COLUMN, "Pumpkin puked"),
    Button.B.value: (PATCH_PEE_COLUMN, "Patch peed"),
    Button.A.value: (PATCH_POO_COLUMN, "Patch pooed"),
    Button.START.value: (PATCH_PUKE_COLUMN, "Patch puked"),
}


def main():
    exception = None
    exit = False
    print("Running")
    try:
        for event in GAMEPAD.read_loop():
            if event.type == ecodes.EV_KEY and event.value:
                col, log_msg = BUTTON_MAPPING.get(event.code, (0,""))

                if not col:
                    continue

                log(col)
                logging.info(log_msg)
    except KeyboardInterrupt:
        print("Exiting")
        exit = True
        sys.exit()
    except Exception as ex:
        exception = ex
    finally:
        logging.error(str(exception))
        if not exit:
            main()

if __name__ == '__main__':
    main()
