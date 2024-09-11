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
# our scoped credentials - this gives our credentials the scope or the sites it's allowed to access
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
# now create our gspread clinet, which will do all our sheet accessing, by authorizing our scoped creds
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# next we get our sheet constant, by telling the client to open our google sheet
SHEET = GSPREAD_CLIENT.open("love_sandwiches")


### --- MAIN --- ###

# in a real world situation we would likely have an api setup from python directly to a businesses software but as we are doing a walkthrough project we shall keep it simple and have the user input via the terminal