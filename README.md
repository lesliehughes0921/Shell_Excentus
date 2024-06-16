### Shell Excentus
Code Kentucky Data Analysis

### Overview
This project automates the monthly report calculations for Shell Excentus based on three primary reports utlizing python and pandas
Visual presentation of store location reward totals
Visual presentation of time spend processing information manually vs code implementation

## Reports Description

# Shell Site List:
Provides Shell merchant ID, customer name, customer number, and zip code.

# Site Redeemer Issuer Settlement:
Monthly report detailing each store location's daily rewards activities.
Contains information from Shell without customer-specific details related to their accounts.

# Vendor Discount:
Provides Site ID, Site Name/Customer #, Vendor Funded Discount from previous month

### Process
Data Integration:

Merge data from the Shell Site List with the Site Redeemer Issuer Settlement.
Group data by customer number and calculate totals for each store location.
Vendor Discount Calculation:

Extract current vendor discount totals and generate a new Vendor Discount report for future months' settlements.
Data Consolidation:

Combine grouped data with previous vendor discount calculations.
Add vendor discount to the accounts receivable column, creating a new total receivable per customer.
Reporting:

Generate an Excel sheet showing total receivable and payable amounts per customer.


### Instructions
1. Clone the repo to your machine.
2. Create and activate a virtual environment and install the packages llisted in the requirements.txt file (instructions below)
3. Run the main.py script. This script will execute creating two new excel files May_2024_Excentus.xlsx and May_Vendor_Funded_Discounts.xlsx

###  Virutal Environment Instructions

1. After you have cloned the repo to your machine, navigate to the project 
folder in GitBash/Terminal.
1. Create a virtual environment in the project folder. 
1. Activate the virtual environment.
1. Install the required packages. 
1. When you are done working on your repo, deactivate the virtual environment.

Virtual Environment Commands
| Command | Linux/Mac | GitBash |
| ------- | --------- | ------- |
| Create | `python3 -m venv venv` | `python -m venv venv` |
| Activate | `source venv/bin/activate` | `source venv/Scripts/activate` |
| Install | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| Deactivate | `deactivate` | `deactivate` |

