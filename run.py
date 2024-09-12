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
        data_str = input("Enter your data here: ")
        
        # get our data as a list
        sales_data = data_str.split(",")
        
        if validate_data(sales_data):
            print("Data is valid.")
            break

    return sales_data

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

def update_sales_worksheet(data):
    """
    Updates the sales worksheet, adds a new row with list data provided
    """  
    #user feedback
    print("Updating sales worksheet... \n")
    #get our sales worksheet
    sales_worksheet = SHEET.worksheet("sales")
    #now append the data (append row method)
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")


def main():
    """
    Run all program functions
    """
    # now we call our sales data function and get our data
    data = get_sales_data()
    # now we need to convert this data into integers once again for our spreadsheet
    sales_data = [int(value) for value in data]
    update_sales_worksheet(sales_data)


### --- RUN APP --- ###

main()