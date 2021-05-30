import datetime


# Creates a new file in .tree extension where the current status of the program is saved.
# if called with an argument it returns name_treediagram.tree, else datetime_treediagram.tree
def create_new_file(existing_filename=None):
    if existing_filename:
        # removes the path of the file
        if "/" in existing_filename:
            existing_filename = existing_filename.split('/')[-1]
        # removes the ending
        new_file_name = existing_filename.split('.')[0] + "_treediagram.tree"
    else:
        new_file_name = get_date_time() + "_treediagram.tree"
    f = open(new_file_name, "w")
    f.close()
    return new_file_name


# returns date and time in this format: YYYYMMDD_HHMMSS, example: 20210528_215355
def get_date_time():
    x = datetime.datetime.now()
    return (x.strftime("%Y") + x.strftime("%m") + x.strftime("%d") + "_" + x.strftime("%H") + x.strftime("%M")
            + x.strftime("%S"))
