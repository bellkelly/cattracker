import json
import logging.config
from sys import exit
from datetime import datetime

import gspread
from evdev import InputDevice, ecodes
from oauth2client.service_account import ServiceAccountCredentials


logging.config.fileConfig('logging.ini')
log = logging.getLogger(__name__)
log.debug("Logging is configured.")


SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]


def get_current_sheet():
    """
    Return the sheet for the current month.

    Expect the name of the Google Sheet to be "Cat Tracker <YEAR>"
    and the name of the worksheet to be the full month name.
    """
    client = login()
    now = datetime.now()
    month = now.strftime("%B")
    year = now.strftime("%Y")
    doc_name = f"Cat Tracker {year}"
    return client.open(doc_name).worksheet(month)


def login():
    """
    Login to Goole Drive.
    """
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", SCOPES)
    return gspread.authorize(creds)


def create_entry(col):
    """
    Append a timestamp to the first empty row in column col.
    """
    sheet = get_current_sheet()
    row = len(sheet.col_values(col)) + 1
    timestamp = datetime.now().strftime("%m/%d/%Y %I:%M %p")
    sheet.update_cell(row, col, timestamp)


def main():
    """
    Continuously process input from external controller.

    Button presses are configured in the config.json file
    to map to a column in a Google Sheet. When the button
    is pressed, a timestamp is logged in that column and a
    log message is added to the configured log file.
    """
    exception = None
    terminate = False

    print("Ready to track cat data...")

    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    gamepad = InputDevice(config["input_path"])
    button_mapping = config["input_code_mapping"]

    try:
        for event in gamepad.read_loop():
            log.debug(event.code)
            if event.type == ecodes.EV_KEY and event.value:
                button_data = button_mapping.get(str(event.code), {})
                if not button_data:
                    continue

                log.info(button_data.get("log_message", ""))
                create_entry(button_data.get("data_column", 0))

    except KeyboardInterrupt:
        print("Exiting")
        terminate = True
        exit()

    except Exception as ex:
        exception = ex

    finally:
        logging.error(str(exception))
        if not terminate:
            main()


if __name__ == '__main__':
    main()
