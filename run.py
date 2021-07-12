import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")


def get_sales_data():
    """
    Get sales figures from user input
    """
    while True:
        print("Please enter sales data from last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Correct info passed")
            break
    return sales_data


def validate_data(values):
    """
    Inside try, coverts values to int.
    Raises ValueError if strings cannot be converted into integers,
    or if there aren't exactly 6 values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values needed, you provided {len(values)}")
    except ValueError as e:
        print(f"invalid data: {e}, please try again. \n")
        return False

    return True


def calculate_surplus_data(sales_row):
    """
    Compare sales and stock to get surplus for each item.

    The surplus is the sales figure subtracted from stock:
    - Positive surplus is waste
    - Negative surplus indicates extra made after stock sold out.
    """
    print("Calculating surplus")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def update_worksheet(data, worksheet):
    """
     This function will handle all worksheets that will be updated.
     Update selected worksheet, add new row with the list of data provided.
     """
    print(f"Updating {worksheet} worksheet... \n")
    surplus_worksheet = SHEET.worksheet(worksheet)
    surplus_worksheet.append_row(data)
    print(f"Updated {worksheet} worksheet successfully \n")


def get_last_5_entries_sales():
    """
    Collects collums of data from the sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")
    columns = []
    for col in range(1, 7):
        column = sales.col_values(col)
        columns.append(column[-5:])
    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data.... \n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / 5
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data


def main():
    """
    Runs all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")



print("Welcome to Love Sandwiches data automation")
main()
