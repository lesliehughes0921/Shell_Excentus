# Shell_Excentus
Monthly Shell excentus report calculations based on three reports.  
First report: Shell Site List provides shell merchant id, customer name, customer number, and zip code
Second report: Site Redeemer Issuer Settlement provided on a monthly basis for each store location and their daily rewards activities. All information is provided through Shell and has no customer specific information in relationship to their customer account.
Third report: Vendor Discount - Vendor Discount payable/receivable is for a previous month
Merging of data from site list to site redeemer settlement, grouping by customer number and calculating totals for each store.
Extracting the current vendor discount totals from the dataframe and creating a new Vendor Discount report to use in the future calcuations in upcoming months for settlement.
Merging of data from the grouped and total df with the vendor discount from the previous calculations 
Adding vendor discount to accounts receivable column, creating a new total receivable column per customer 
Creating a new excel sheet showing the total receivable and payable amounts per customer 


# NOTE: write walk through on how to install venv, how to activate it, then how to install everythingfrom requirments