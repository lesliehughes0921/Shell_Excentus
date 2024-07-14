import os
import pandas as pd

def generate_path(file_name_str):
    return os.path.join(".", "data", file_name_str)

def generate_output_path(new_file_name_str):
    output_dir = os.path.join(".", "output_data")
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
    return os.path.join(output_dir, new_file_name_str)

def main():
    # Reading Excel files into DataFrames
    monthly_excentus_source_df = pd.read_excel(generate_path("Site_Redeemer_Issuer_Settlement_3160398.xlsx"), skiprows=1)
    site_list_source_df = pd.read_excel(generate_path("Shell_Site_List.xlsx"))
    previous_vendor_discount_source_df = pd.read_excel(generate_path("March_Vendor_Discount.xlsm"))

    # Output or further processing can be done here
    print(monthly_excentus_source_df.head())
    print(site_list_source_df.head())
    print(previous_vendor_discount_source_df.head())

    # Rename columns in site_list
    site_list_source_df.rename(columns={"Merchant_Id_1": "Site ID"}, inplace=True)

    # Drop specified columns
    site_list_source_df.drop(columns=["Zip Code"], inplace=True)

    # Convert Site ID to string type
    site_list_source_df["Site ID"] = site_list_source_df["Site ID"].astype(str)

    # Drop last two rows with NAN that only show totals
    monthly_excentus_source_df.drop(monthly_excentus_source_df.tail(2).index, inplace=True)

    # Drop specified columns
    columns_to_drop = ["Post Date", "Site Name", "Total Discounted Gallons", "Total Discounts Redeemed", 
                        "Site Funded", "Redemption Fee", "Issuance Fee", "Flat Fee", "Program ID", "Type"]
    monthly_excentus_source_df.drop(columns=columns_to_drop, inplace=True)

    # Convert Site ID to string type
    monthly_excentus_source_df['Site ID'] = monthly_excentus_source_df['Site ID'].astype(str)

    # Remove .0 from Site ID
    monthly_excentus_source_df['Site ID'] = monthly_excentus_source_df['Site ID'].apply(lambda x: x[:-2] if x.endswith('.0') else x)

    # Process previous_vendor_discount: Rename Column Names
    previous_vendor_discount_source_df.rename(columns={"Site ID": "Customer Name", "Site Name": "Customer #"}, inplace=True)

    # Group monthly excentus by site ID and sum
    grouped_monthly_excentus = monthly_excentus_source_df.groupby("Site ID").sum().reset_index()

    # Merge Site List to Grouped Monthly Excentus
    merged_site_list_excentus = pd.merge(site_list_source_df, grouped_monthly_excentus, on="Site ID", how="outer")

    # Sort Grouped Excentus by Customer #
    sorted_merged_excentus = merged_site_list_excentus.sort_values(by="Customer #")

    # Create New DF for Current Vendor Discount
    current_vendor_discount = sorted_merged_excentus[["Site ID", "Customer #", "Vendor Funded Discounts"]]

    # Export vendor_discount_new to Excel
    current_vendor_discount.to_excel(generate_output_path("May_Vendor_Funded_Discounts.xlsx"), index=False)

    # Drop Current Month Vendor Funded Discounts
    current_month_payables_excentus = sorted_merged_excentus.drop(columns=["Vendor Funded Discounts"], inplace=False)

    # Rename columns in Previous Vendor Discount
    previous_vendor_discount_source_df.rename(columns={"Site Name": "Customer #"}, inplace=True)

    # Drop NAN Rows
    previous_vendor_discount_source_df = previous_vendor_discount_source_df.dropna()

    # Merge current_month_payables_excentus with previous_vendor_discount
    merged_excentus_vd = pd.merge(previous_vendor_discount_source_df, current_month_payables_excentus,
                                   on="Customer #", how="outer", suffixes=('_new', '_curr'))

    # Fill in NAN with 0 in Vendor Funded Discounts Column
    merged_excentus_vd["Vendor Funded Discounts"] = merged_excentus_vd["Vendor Funded Discounts"].fillna(0)

    # Round numbers to two decimal points
    columns_to_round = ["Vendor Funded Discounts", "Total Receivable - Daily", "Total Payable - Daily"]
    merged_excentus_vd[columns_to_round] = merged_excentus_vd[columns_to_round].round(2)

    # Drop Duplicate Columns
    merged_excentus_vd_dropped = merged_excentus_vd.drop("Customer Name_new", axis=1, inplace=False)

    # Rename Columns
    merged_excentus_vd_renamed = merged_excentus_vd_dropped.rename(columns={"Customer Name_curr": "Customer Name",
                                                                           "Total Payable - Daily": "Total Payable"}, inplace=False)

    # Add Vendor Funded Discount to Total Receivable
    merged_excentus_vd_renamed["Total Receivable"] = merged_excentus_vd_renamed["Total Receivable - Daily"] + merged_excentus_vd_renamed["Vendor Funded Discounts"]

    # Drop Columns and Create Final Total Sums Sheet
    columns_to_drop = ['Vendor Funded Discounts', 'Total Receivable - Daily']
    total_sum_excentus = merged_excentus_vd_renamed.drop(columns=columns_to_drop, inplace=False)

    # Reorder Columns for Entry
    new_order = ["Site ID", "Customer Name", "Customer #", "Total Receivable", "Total Payable"]
    pre_mas_entry_excentus = total_sum_excentus[new_order]

    # Calculate totals across numerical columns
    totals = pre_mas_entry_excentus.select_dtypes(include=[float, int]).sum()

    # Create DataFrame for totals
    totals_df = pd.DataFrame(totals).T
    totals_df.index = ['Totals']  # Set index label for the totals row

    # Concatenate totals_df with pre_mas_entry_excentus
    df_totals = pd.concat([pre_mas_entry_excentus, totals_df])

    # Export final results to Excel
    df_totals.to_excel(generate_output_path("May_2024_Excentus.xlsx"), index=False)

    print("Files have been saved to the output directory.")

if __name__ == "__main__":
    main()

