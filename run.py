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

def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet... \n")
    sale_worksheet = SHEET.worksheet("sales")
    sale_worksheet.append_row(data)
    print("Updated successfully")

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
    stock_num = [int(num) for num in stock_row]
    surplus_data = []
    for stock, sales in zip(stock_num, sales_row):
        surplus = stock - sales
        surplus_data.append(surplus)
    print(surplus_data)

    


def main():
    """
    Runs all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)

print("Welcome to Love Sandwiches data automation")
main()