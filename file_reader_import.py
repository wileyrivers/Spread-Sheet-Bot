import os
import pdb
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from get_methods import get_amex, get_beer, get_cash, \
    get_date, get_discover, get_food, get_gc_sales, \
    get_gift_pay, get_hse_acct, get_liquor, get_mc, \
    get_tax, get_visa, get_wine, get_na_bev, get_retail, get_auto_grat

final = []


def breakdown_file(file_path):
    """
    method takes a file path provided and turns the corresponding file into raw line for line data. If any errors
    occur method will print error message. This method will finally trigger the first_word_search method.
    :param file_path: path to a file in the raw directory
    """
    file_breakdown = []
    try:
        raw_file = open(file_path, mode='rt')
        for line in raw_file:
            data_line = line.strip().rsplit()
            file_breakdown.append(data_line)
    except OSError:
        print("Error loading file")
    else:
        file_breakdown = list(filter(None, [x for x in file_breakdown if x]))
        # for x in range(len(lines)):
        #     print(str(x)+" "+str(lines[x]))
        first_word_search(file_breakdown)
    finally:
        raw_file.close()


def first_word_search(file):
    """
    Populates global list final with the data supplied by execute_transfer.
    The single required parameter is (an iterable line for line breakdown of Aloha Manager Systems
    Daily Sales report) a list corresponding with data in the name_dict a dictionary of
    string:get_ method values. All value (get_) methods included in the module are intended to run inside first_word_search
    after the key (string) is found in the file. The key word is then pop()'d out of the dictionary to
    prevent data from being collected more than once per run of the method.
    """
    global final
    name_dict = {'Sales': get_date, 'Cash': get_cash, "AMEX": get_amex, "VISA": get_visa,
                 "MC": get_mc, "Qty": get_gift_pay, "DISCOVER": get_discover, "HSE": get_hse_acct,
                 "Gift": get_gc_sales, "Non-Cash": get_auto_grat, "FOOD": get_food, "NA": get_na_bev,
                 "BEER": get_beer,
                 "WINE": get_wine, "LIQUOR": get_liquor, "Retail": get_retail, "****************************": get_tax}

    final = []
    try:
        for x in range(len(file)):
            if len(file[x]) > 0:
                # print(str(x) + " " + str(file[x]))
                if file[x][0] in name_dict.keys():
                    run = name_dict.get(file[x][0])
                    result = run(file, x)
                    if result is not None:
                        final.append(result)
                        name_dict.pop(file[x][0])
                    else:
                        continue
    except IndexError:
        print("Index error at " + str(x))
        pdb.set_trace()

    num = 0
    for x in range(len(final)):
        if final[x][0] == "GC Payments" or final[x][0] == "HSE ACCT":
            num += float(final[x][1])
    final.append(["GC/HSE", num])

    populate_spread_sheet(final)


def build_path_list():
    """
    This method return a list of filepaths each one leading to a file in the raw directory. Files in the raw directory
    should be Aloha Manager reports printed in the correct configuration.
    :return: directory_path_list
    """
    directory = r'files/raw'
    directory_path_list = []
    for files in os.scandir(directory):
        directory_path_list.append(files)
    return directory_path_list


def execute_transfer(path_list):
    """
    This method takes a list of file paths and one by one feeds them into the breakdown_file() method, leading
    on to the rest of the program through nested calls.
    :param path_list:
    :return:
    """
    for line in path_list:
        path = os.path.abspath(line)
        breakdown_file(path)


def get_data_column(data):
    """
    method used by the populate_spread_sheet() method in order to retrieve the correct Column corresponding
    with the type of name of the type of data. Method will always be called automatically by populate_spread_sheet()
    """
    data_dict = {"Cash Payments": "B", "AMEX": "C", "Visa": "D", "MC": "E", "Discover": "F",
                 'GC/HSE': "G", "GC Sales": "K", "CC Tips": "L", "Auto Grat": "M",
                 "Food Sales": "N", "NA Bev": "O", "Beer Sales": "P",
                 "Wine Sales": "Q", "Liquor Sales": "R", "Retail Sales": "S", "Tax Total": "T"}
    if data in data_dict.keys():
        return data_dict.get(data)


def populate_spread_sheet(data_list):
    """
    This method is automatically called by the first_word_search() method. This method takes the data_list named final
    and iterates through the list using get_data_column() to creat the A1 notation needed for Google Sheets API.
    :param data_list: final variable from the first_word_search()
    """
    date = data_list[0]
    # month = int(date[1][:2]) - 1
    month = int(date[1][:2])
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("Daily Sales 2020").get_worksheet(month)
    day = int(date[1][3:5])
    year = int(date[1][-4:])
    day_index = str(day + 3)

    input_list = []
    for x in range(1, len(data_list)):
        column = str(get_data_column(data_list[x][0]))
        notation = column + day_index + ":" + column + day_index
        modify_cell(sheet, notation, data_list[x][1])


def modify_cell(sheet, notation, value):
    """
    This method performs modification and finalization on the sheet supplied by parameters.
    :param sheet: the sheet on the google sheet to modify, configured automatically.
    :param notation: the A1 notation of the data, configured automatically.
    :param value: the value to upload to the spreadsheet.
    :return: None
    """
    try:
        cell_list = sheet.range(notation)
        for cell in cell_list:
            cell.value = value
            sheet.update_cells(cell_list)
    except gspread.exceptions.APIError:
        print("APIError")
        return
