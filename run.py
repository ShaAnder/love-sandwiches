### --- IMPORTS --- ###

# imports the entire gspread library
import gspread
#imports our service account credentials
from google.oauth2.service_account import Credentials

### --- API CALLS FOR GOOGLE SHEETS --- ###

# I AM (identity and access management) scope of our code
# in python constant vairable names (don't change) are in caps
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# create our creds constant - we create our credentials from the credentials json file
CREDS = Credentials.from_service_account_file("creds.json")
# our scoped credentials - gives our credentials the scope it's allowed to access
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# now create our gspread clinet, by authorizing our scoped creds
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# next we get our sheet constant, by telling the client to open our google sheet
SHEET = GSPREAD_CLIENT.open("love_sandwiches")


### --- FUNCTIONS --- ###

# in a real world situation we would likely have an api setup from python directly
# to a businesses software but as we are doing a walkthrough project we shall keep
# it simple and have the user input via the terminal

# collect our sales data

def get_sales_data():
    """
    Get the sales figures from the user
    """

    while True:

        # instructions for user
        print("Please enter sales data from the last market")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,53,23,21,15,12\n")

        # get our data str, and provide feedback
        data_str = input("Enter your data here:\n")
        
        # get our data as a list
        sales_data = data_str.split(",")
        
        if validate_data(sales_data):
            print("Data is valid.")
            break

    return sales_data

def get_last_five_entries_sales():
    """
    Collects the last 5 columns from the sales worksheet, 
    and returns the data in a list of lists
    """
    # we get our sales sheet here for manipulating
    sales = SHEET.worksheet("sales")
    # set our columns array
    columns = []
    # now we loop through and get our columns
    for ind in range(1,7):
        #  set the column as our sales column values
        column = sales.col_values(ind)
        # append the last 5 columns to the columns array
        columns.append(column[-5:])
    
    # return our array of arrays
    return columns

        


def validate_data(values):
    """
    Validatae our data using a try except block, will try to convert all valeus
    into integers and will raise a value error if they cannot or if there isn't
    exactly 6 values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid Data: {e}, please try again.\n")
        return False

    return True

def update_worksheet(data, worksheet):
    """
    Updates the selected worksheet with the data provided, takes the data and selected worksheet
    as our arguments.
    """ 
    # user feedback
    print(f"Updating {worksheet} worksheet... \n")
    # get our worksheet to update
    worksheet_to_update = SHEET.worksheet(worksheet)
    # now append the data (append row method)
    worksheet_to_update.append_row(data)
    # more user feedback
    print(f"Updated {worksheet} worksheet successfully.\n")


def calculate_surplus(sales_row):
    """
    Compare sales and stock to calculate the surplus of each item

    The surplus is defined as (stock - sales):
        - Positive figures indicate wasted stock
        - Negative figures indicate extra made when stock sold out
    """
    #user feedback 
    print("Calculating surplus data... \n")
    #now ew want to get our current stock using get all values
    stock = SHEET.worksheet("stock").get_all_values()
    #now we get our last stock row
    stock_row = stock[len(stock)-1]
    
    # next we get the stock surplus, using the zip method to iterate over both lists
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculate stock data...\n")
    # now we get our new stock data from looping through the columns
    new_stock_data = []
    # this gets the average for each column
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        # now we want 10% added onto that to account for needs
        stock_num = (average * 1.1)
        # now we append, and round the numbers to ensure whole numbers
        new_stock_data.append(round(stock_num))
    
    return new_stock_data


def main():
    """
    Run all program functions
    """
    # now we call our sales data function and get our data
    data = get_sales_data()
    # now we need to convert this data into integers once again for our spreadsheet
    sales_data = [int(value) for value in data]
    # we want to update the sales worksheet 
    update_worksheet(sales_data, "sales")
    # we feed the sales data into calculate_surplus and use the return of that as our 
    # argument for updating the surplus worksheet
    update_worksheet(calculate_surplus(sales_data), "surplus")
    # now we're calculating the stock data    
    sales_columns = get_last_five_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")
    return stock_data


### --- RUN APP --- ###

print("Welcome to Love Sandwiches Data Automation. \n")
stock_data = main()


def get_stock_values(data):
    """
    Gets the stock values and headings to give the user feedback on what to
    make for the next market
    """
    headings = SHEET.worksheet("stock").get_all_values()[0]
    stock_data_dict = dict(zip(headings, data))
    return stock_data_dict

stock_values = get_stock_values(stock_data)
print("Here are the recommended sandwich quanitites for the next market:\n")
print(stock_values)
