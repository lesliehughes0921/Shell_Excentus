# %%
# import pandas

import pandas as pd

# %%
# Load Data

site_list = pd.read_excel(r"C:\Users\lesli\github-classroom\Testing\Shell Site List 06-05-2024.xlsx")
monthly_excentus_download = pd.read_excel(r"C:\Users\lesli\github-classroom\Testing\Emailing_ Shell Site List 06-05-2024\Site_Redeemer_Issuer_Settlement_3160398.xlsx", skiprows=1)
previous_vendor_discount = pd.read_excel(r"C:\Users\lesli\github-classroom\Testing\Emailing_ Shell Site List 06-05-2024\March 2024 Excentus.xlsm")

# %%
# Raname Columns

site_list.rename(columns={"Merchant_Id_1":"Site ID"}, inplace=True)

# %%
# Drop specified columns

site_list.drop(columns={"Zip Code", "Column1"}, inplace=True)

# %%
# Convert Site ID to string type

site_list["Site ID"] = site_list["Site ID"].astype(str)

# %%
# Drop last two rows with NAN that only show totals

monthly_excentus_download.drop(monthly_excentus_download.tail(2).index, inplace=True)

# %%
# Drop specified columns
columns_to_drop = ["Post Date", "Site Name", "Total Discounted Gallons", "Total Discounts Redeemed", 
"Site Funded", "Redemption Fee", "Issuance Fee", "Flat Fee", "Program ID", "Type"]
monthly_excentus_download.drop(columns=columns_to_drop, inplace=True)

# %%
# Convert Site ID to string type

monthly_excentus_download['Site ID'] = monthly_excentus_download['Site ID'].astype(str)

# %%
# Remove .0 from Site ID

monthly_excentus_download['Site ID'] = monthly_excentus_download['Site ID'].astype(str).apply(lambda x: x[:-2] if x.endswith('.0') else x)

# %%
# Process previous_vendor_discount :  Rename Column Names Previous Vendor Funded Discount

previous_vendor_discount.rename(columns={"Site ID": "Customer Name", "Site Name": "Customer #"}, inplace=True)

# %%
# Group monthly excentus by site ID and sum

grouped_monthly_excentus = monthly_excentus_download.groupby("Site ID").sum().reset_index()

# %%
# Merge Site List to Grouped Monthly Excentus

merged_site_list_excentus = pd.merge(site_list, grouped_monthly_excentus, on= "Site ID", how="outer")

# %%
# Sort Grouped Excentus by Customer #
sorted_merged_excentus = merged_site_list_excentus.sort_values(by="Customer #")

# %%
# Create New DF for Current Vendor Discount
current_vendor_discount = sorted_merged_excentus[["Site ID", "Customer #", "Vendor Funded Discounts"]]

# %%
# Export vendor_discount_new to Excel

current_vendor_discount.to_excel("May_Vendor_Funded_Discounts.xlsx", index=False)

# %%
# Drop Current Month Vendor Funded Discounts

current_month_payables_excentus = sorted_merged_excentus.drop(columns=["Vendor Funded Discounts"], inplace=False)

# %%
# Rename columns in Previous Vendor Discount

previous_vendor_discount.rename(columns={"Site Name": "Customer #"}, inplace=True)

# %%
# Drop NAN Rows

previous_vendor_discount = previous_vendor_discount.dropna()

# %%
# Merge current_month_payables_excentus with previous_vendor_discount

merged_excentus_vd = pd.merge(previous_vendor_discount,current_month_payables_excentus,on="Customer #",how="outer",suffixes=('_new', '_curr'))

# %%
# Fill in NAN with 0 in Vendor Funded Discounts Column

merged_excentus_vd["Vendor Funded Discounts"] = merged_excentus_vd["Vendor Funded Discounts"].fillna(0)

# %%
# Round numbers to two decimal points
columns_to_round = ["Vendor Funded Discounts", "Total Receivable - Daily", "Total Payable - Daily"]
merged_excentus_vd[columns_to_round] = merged_excentus_vd[columns_to_round].round(2)

# %%
# Drop Duplicate Columns

merged_excentus_vd_dropped = merged_excentus_vd.drop("Customer Name_new", axis=1, inplace=False)

# %%
# Rename Columns
merged_excentus_vd_renamed = merged_excentus_vd_dropped.rename(columns={"Customer Name_curr": "Customer Name",  "Total Payable - Daily": "Total Payable"}, inplace=False)

# %% [markdown]
# 

# %%
# Add Vendor Funded Discount to Total Receivable
merged_excentus_vd_renamed["Total Receivable"] = merged_excentus_vd_renamed["Total Receivable - Daily"] + merged_excentus_vd_renamed["Vendor Funded Discounts"]

# %%
# Drop Columns and Create Final Total Sums Sheet
columns_to_drop = ['Vendor Funded Discounts', 'Total Receivable - Daily']
total_sum_excentus = merged_excentus_vd_renamed.drop(columns=columns_to_drop, inplace=False)


# %%
# Reorder Columns for Entry
new_order = ["Site ID", "Customer Name", "Customer #", "Total Receivable", "Total Payable"]
pre_mas_entry_excentus = total_sum_excentus[new_order]
pre_mas_entry_excentus

# %%
# Calculate totals across numerical columns
totals = pre_mas_entry_excentus.select_dtypes(include=[float, int]).sum()
totals

# %%
totals_df = pd.DataFrame(totals).T
totals_df.index = ['Totals']  # Set index label for the totals row

# Concatenate totals_df with pre_mas_entry_excentus
df_totals = pd.concat([pre_mas_entry_excentus, totals_df])

# %%
df_totals.to_excel("May_2024_Excentus.xlsx", index=False)



