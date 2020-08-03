import file_reader_import



def get_date(file, x):
    if file[x][1] == 'Report':
        return ["Date", file[x + 1][0]]


def get_cash(file, x):
    if file[x][1] == 'Payments':
        return ["Cash Payments", file[x][2]]


def get_amex(file, x):
    if file[x][0] == 'AMEX':
        return ["AMEX", file[x][2]]


def get_visa(file, x):
    if file[x][0] == 'VISA':
        return ["Visa", file[x][2]]


def get_mc(file, x):
    if file[x][0] == 'MC':
        return ["MC", file[x][2]]


def get_gift_pay(file, x):
    if file[x][1] == 'Amount':
        if file[x+4][0] == "Gift":
            return ["GC Payments", file[x+4][3]]


def get_discover(file, x):
    if file[x][0] == 'DISCOVER':
        return ["Discover", file[x][2]]


def get_hse_acct(file, x):
    if file[x][1] == 'ACCT':
        return ["HSE ACCT", file[x][3]]


def get_gc_sales(file, x):
    if file[x][1] == 'Card':
        if file[x][2] == 'Promos':
            return ["GC Sales", file[x + 2][1]]


# def get_cc_tips(file, x):
#     if len(file[x]) > 3:
#         print("CC Tips Received")
#         return ["CC Tips", file[x][3]]


def get_auto_grat(file, x):
    if len(file[x]) > 3:
        file_reader_import.final.append(["CC Tips", file[x][3]])
        return ["Auto Grat", file[x + 2][3]]



def get_food(file, x):
    if file[x][1] != "Tax":
        return ["Food Sales", file[x][1]]


def get_na_bev(file, x):
    if file[x][1] == "BEVERAGES":
        return ["NA Bev", file[x][2]]


def get_beer(file, x):
    if len(file[x]) > 3:
        return ["Beer Sales", file[x][1]]


def get_wine(file, x):
    if len(file[x]) > 3:
        return ["Wine Sales", file[x][1]]


def get_liquor(file, x):
    if len(file[x]) > 3:
        return ["Liquor Sales", file[x][1]]


def get_retail(file, x):
    if file[x][1] == "Categories":
        if file[x + 7][0] == "Subtotal":
            return ["Retail Sales", file[x + 7][1]]


def get_tax(file, x):
    return ["Tax Total", file[x - 1][1]]
