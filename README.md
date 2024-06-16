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
3. Run the 

Set up a virtual environment:

bash
Copy code
python -m venv venv
Activate the virtual environment:

Windows:
bash
Copy code
venv\Scripts\activate
Unix or MacOS:
bash
Copy code
source venv/bin/activate
Install dependencies from requirements.txt:

bash
Copy code
pip install -r requirements.txt
Execute the project scripts as needed.

