import datetime
import platform


# colors used to display messages in the terminal.
class TerminalColors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


# Creates a new file in .tree extension where the current status of the program is saved.
# if called with an argument it returns name_treediagram.tree, else datetime_treediagram.tree
def create_new_file(existing_filename=None):
    if existing_filename:
        # removes the path of the file
        if "/" in existing_filename:
            existing_filename = existing_filename.split('/')[-1]
        # removes the ending
        new_file_name = existing_filename.split('.')[0] + "_td.tree"
    else:
        new_file_name = get_date_time() + "_td.tree"
    f = open(new_file_name, "w")
    f.close()
    return new_file_name


# returns date and time in this format: YYYYMMDD_HHMMSS, example: 20210528_215355
def get_date_time():
    x = datetime.datetime.now()
    return (x.strftime("%Y") + x.strftime("%m") + x.strftime("%d") + "_" + x.strftime("%H") + x.strftime("%M")
            + x.strftime("%S"))


# prints an error or confirmation message to the terminal, if the system is Darwin (macOS) the text is coloured
# depending on the message type
def print_message(message_type, message, new_line=True):
    # Darwin = MacOS
    if platform.system() == 'Darwin':
        # if we want to have a blank line after a message
        if new_line:
            message = message[:-1]
            if message_type:
                print(f"{TerminalColors.OKGREEN}{message}{TerminalColors.ENDC}\n")
            else:
                print(f"{TerminalColors.FAIL}{message}{TerminalColors.ENDC}\n")
        else:
            if message_type:
                print(f"{TerminalColors.OKGREEN}{message}{TerminalColors.ENDC}")
            else:
                print(f"{TerminalColors.FAIL}{message}{TerminalColors.ENDC}")
    else:
        print(message)
