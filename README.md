# Shell Excentus
Code Kentucky Data Analysis

## Overview
This project automates the monthly report calculations for Shell Excentus based on three primary reports using Python and Pandas. It includes visual presentations of store location reward totals and a comparison of time spent processing information manually versus code implementation.

## Tableau Visualization
Check out my Tableau visualization https://public.tableau.com/views/MayExcentusCustomerAccountsPayablevsReceivable/Sheet1?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link

## Instructions
1. Clone the repo to your machine.
2. Create and activate a virtual environment:
   - Linux/Mac: `python3 -m venv venv` followed by `source venv/bin/activate`
   - GitBash/Windows: `python -m venv venv` followed by `source venv/Scripts/activate`
3. Install the required packages: `pip install -r requirements.txt`
4. Run the excentus_main.py script to generate two Excel files: `May_2024_Excentus.xlsx` and `May_Vendor_Funded_Discounts.xlsx`.

## Virtual Environment Commands
| Command    | Linux/Mac                          | GitBash/Windows                   |
|------------|------------------------------------|-----------------------------------|
| Create     | `python3 -m venv venv`              | `python -m venv venv`             |
| Activate   | `source venv/bin/activate`          | `source venv/Scripts/activate`    |
| Install    | `pip install -r requirements.txt`   | `pip install -r requirements.txt`|
| Deactivate | `deactivate`                        | `deactivate`                      |

## Reports Description

### Shell Site List
Provides Shell merchant ID, customer name, customer number, and zip code.

### Site Redeemer Issuer Settlement
Monthly report detailing each store location's daily rewards activities. Contains information from Shell without customer-specific details related to their accounts.

### Vendor Discount
Provides Site ID, Site Name/Customer #, Vendor Funded Discount from the previous month.

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
- Generate visualization_savings to view the total hours saved and salary saved by automating the process to calculate Shell Excentus Rewards
- Generate Total_Receivable_by_Customer for visulization of total AR per customer number.
