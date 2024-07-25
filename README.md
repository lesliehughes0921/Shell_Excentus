# Shell Excentus
Code Kentucky Data Analysis

## Overview
This project automates the monthly report calculations for Shell Excentus based on three primary reports using Python and Pandas. It includes visual presentations of store location reward totals and a comparison of time spent processing information manually versus code implementation. Automating the calculation of monthly reports for Shell Excentus, providing visual insights into rewards and discounts

## Instructions
1. Clone the repo to your machine.
2. Create and activate a virtual environment:
   - Linux/Mac: `python3 -m venv venv` followed by `source venv/bin/activate`
   - GitBash/Windows: `python -m venv venv` followed by `source venv/Scripts/activate`
3. Install the required packages: `pip install -r requirements.txt`
4. Run the `excentus_main.py` script to generate two Excel files: `May_2024_Excentus.xlsx` and `May_Vendor_Funded_Discounts.xlsx`. The script will also generate visualizations of salary saved by automated process vs. manual completion and total receivable by customer.

## Virtual Environment Commands
| Command    | Linux/Mac                          | GitBash/Windows                   |
|------------|------------------------------------|-----------------------------------|
| Create     | `python3 -m venv venv`             | `python -m venv venv`             |
| Activate   | `source venv/bin/activate`         | `source venv/Scripts/activate`    |
| Install    | `pip install -r requirements.txt`  | `pip install -r requirements.txt` |
| Deactivate | `deactivate`                       | `deactivate`                      |

## Reports Description

### Shell Site List
Provides Shell merchant ID, customer name, customer number, and zip code.

### Site Redeemer Issuer Settlement
Monthly report detailing each store location's daily rewards activities. Contains information from Shell without customer-specific details related to their accounts.

### Vendor Discount
Provides Site ID, Site Name/Customer #, and Vendor Funded Discount from the previous month.

## Process
### Data Integration
- Merge data from the Shell Site List with the Site Redeemer Issuer Settlement.
- Group data by customer number and calculate totals for each store location.

### Vendor Discount Calculation
- Extract current vendor discount totals and generate a new Vendor Discount report for future months' settlements.

### Data Consolidation
- Combine grouped data with previous vendor discount calculations.
- Add vendor discount to the accounts receivable column, creating a new total receivable per customer.

### Reporting
- Generate an Excel sheet showing total receivable and payable amounts per customer.
- Generate visualizations to view the total hours saved and salary saved by automating the process to calculate Shell Excentus Rewards.
- Generate visualizations of total accounts receivable per customer number.

## Tableau Visualization
Check out my Tableau visualization [here](https://public.tableau.com/views/MayExcentusCustomerAccountsPayablevsReceivable/Sheet1?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link). This visualization compares customer accounts payable and receivable, providing insights into account balances and transaction trends.

## Running Unit Tests
To ensure that the functions in this project work correctly, you can run the unit tests:

1. **Navigate to the test script directory**:
   Make sure you are in the directory where `test_script.py` is located.

2. **Run the tests**:
   Execute the following command in your terminal:

   ```bash
   python -m unittest test_script.py
