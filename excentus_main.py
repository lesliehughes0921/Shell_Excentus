# Import necessary libraries
import os
import pandas as pd

# Define helper functions to generate paths
def generate_path(file_name_str):
    """Generate the path to the data directory."""
    return os.path.join(".", "data", file_name_str)
    
def generate_output_path(new_file_name_str):
    """Generate the path to the output_data directory."""
    return os.path.join(".", "output_data", new_file_name_str)

def main():
    # Reading Excel files into DataFrames
    monthly_excentus_source_df = pd.read_excel(generate_path("Site_Redeemer_Issuer_Settlement_3160398.xlsx"), skiprows=1)
    site_list_source_df = pd.read_excel(generate_path("Shell_Site_List.xlsx"))
    previous_vendor_discount_source_df = pd.read_excel(generate_path("March_Vendor_Discount.xlsm"))

    # Data Cleaning and Processing
    site_list_df = site_list_source_df.copy()
    site_list_df.rename(columns={"Merchant_Id_1": "Site ID"}, inplace=True)
    site_list_df["Site ID"] = site_list_df["Site ID"].astype(str)

    # Remove the last two rows with NaN values that only show totals
    monthly_excentus_df = monthly_excentus_source_df.iloc[:-2].copy()

    # Drop unnecessary columns
    columns_to_filter_out = ["Post Date", "Site Name", "Total Discounted Gallons", "Total Discounts Redeemed", "Site Funded", "Redemption Fee", "Issuance Fee", "Flat Fee", "Program ID", "Type"]
    monthly_excentus_filtered_df = monthly_excentus_df.drop(columns=columns_to_filter_out)

    # Convert Site ID to string type and remove '.0'
    monthly_excentus_filtered_df['Site ID'] = monthly_excentus_filtered_df['Site ID'].astype(str).apply(lambda x: x[:-2] if x.endswith('.0') else x)

    # Process previous_vendor_discount
    previous_vendor_discount_df = previous_vendor_discount_source_df.copy()
    previous_vendor_discount_df.rename(columns={"Site ID": "Customer Name", "Site Name": "Customer #"}, inplace=True)

    # Group monthly excentus by Site ID and sum
    grouped_monthly_excentus = monthly_excentus_filtered_df.groupby("Site ID").sum().reset_index()

    # Merge Site List with Grouped Monthly Excentus
    merged_site_list_excentus = pd.merge(site_list_df, grouped_monthly_excentus, on="Site ID", how="outer")

    # Sort merged data by Customer #
    sorted_merged_excentus = merged_site_list_excentus.sort_values(by="Customer #")

    # Create new DataFrame for Current Vendor Discount
    current_vendor_discount = sorted_merged_excentus[["Site ID", "Customer #", "Vendor Funded Discounts"]]
    current_vendor_discount.to_excel(generate_output_path("May_Vendor_Funded_Discounts.xlsx"), index=False)

    # Continue with further processing as needed
    current_month_payables_excentus = sorted_merged_excentus.drop(columns=["Vendor Funded Discounts"], inplace=False)
    previous_vendor_discount_df.rename(columns={"Site Name": "Customer #"}, inplace=True)
    previous_vendor_discount_df.dropna(inplace=True)

    merged_excentus_vd = pd.merge(previous_vendor_discount_df, current_month_payables_excentus, on="Customer #", how="outer", suffixes=('_new', '_curr'))
    merged_excentus_vd["Vendor Funded Discounts"] = merged_excentus_vd["Vendor Funded Discounts"].fillna(0)

    columns_to_round = ["Vendor Funded Discounts", "Total Receivable - Daily", "Total Payable - Daily"]
    merged_excentus_vd[columns_to_round] = merged_excentus_vd[columns_to_round].round(2)

    merged_excentus_vd_dropped = merged_excentus_vd.drop("Customer Name_new", axis=1)
    merged_excentus_vd_renamed = merged_excentus_vd_dropped.rename(columns={"Customer Name_curr": "Customer Name", "Total Payable - Daily": "Total Payable"})

    merged_excentus_vd_renamed["Total Receivable"] = merged_excentus_vd_renamed["Total Receivable - Daily"] + merged_excentus_vd_renamed["Vendor Funded Discounts"]
    columns_to_drop = ['Vendor Funded Discounts', 'Total Receivable - Daily']
    total_sum_excentus = merged_excentus_vd_renamed.drop(columns=columns_to_drop)

    new_order = ["Site ID", "Customer Name", "Customer #", "Total Receivable", "Total Payable"]
    pre_mas_entry_excentus = total_sum_excentus[new_order]

    totals = pre_mas_entry_excentus.select_dtypes(include=[float, int]).sum()
    totals_df = pd.DataFrame(totals).T
    totals_df.index = ['Totals']  # Set index label for the totals row

    df_totals = pd.concat([pre_mas_entry_excentus, totals_df])
    df_totals.to_excel(generate_output_path("May_2024_Excentus.xlsx"), index=False)

    print("Script completed.")

if __name__ == "__main__":
    main()
