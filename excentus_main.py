import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_path(file_name_str):
    """
    Generate the full path to a data file.
    
    Args:
    file_name_str (str): The name of the file.
    
    Returns:
    str: The full path to the file.
    """
    return os.path.join(".", "data", file_name_str)

def generate_output_path(new_file_name_str):
    """
    Generate the full path to an output file and ensure the output directory exists.
    
    Args:
    new_file_name_str (str): The name of the output file.
    
    Returns:
    str: The full path to the output file.
    """
    output_dir = os.path.join(".", "output_data")
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, new_file_name_str)

def create_visualization(df):
    """
    Create a bar plot visualization of total receivable by customer name.
    
    Args:
    df (pd.DataFrame): DataFrame containing the data to be visualized.
    """
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Customer Name', y='Total Receivable', data=df)
    plt.title('Total Receivable by Customer Name')
    plt.xticks(rotation=45)
    plt.ylabel('Total Receivable')
    plt.xlabel('Customer Name')
    plt.tight_layout()
    plt.savefig(generate_output_path("Total_Receivable_by_Customer.png"))  # Save the plot
    plt.show()  # Display the plot

def main():
    """
    Main function to calculate time and cost savings, create visualizations, and process Excentus data.
    """
    # Define metrics for time and cost savings calculation
    manual_time = 4.5  # Average time spent manually (hours)
    automated_time = 0.5  # Time spent with automation (hours)
    hourly_rate = 25  # Cost per hour ($)

    # Calculate savings
    time_saved = manual_time - automated_time
    manual_cost = manual_time * hourly_rate
    automated_cost = automated_time * hourly_rate
    cost_saved = manual_cost - automated_cost

    # Define categories and values for visualizations
    categories = ["Manual Process", "Automated Process"]
    time_spent = [manual_time, automated_time]
    costs = [manual_cost, automated_cost]

    # Create a bar chart for time spent
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.bar(categories, time_spent, color=['red', 'green'])
    plt.title("Time Spent (Hours)")
    plt.ylabel("Hours")
    plt.ylim(0, 5)
    plt.grid(axis='y')

    # Create a bar chart for costs
    plt.subplot(1, 2, 2)
    plt.bar(categories, costs, color=['red', 'green'])
    plt.title("Cost ($)")
    plt.ylabel("Dollars")
    plt.ylim(0, max(costs) + 20)  # Adjust y-limit based on max cost
    plt.grid(axis='y')

    plt.tight_layout()
    plt.savefig("output_data/savings_visualization.png")  # Save the visualization
    plt.show()  # Display the visualization
    print("Savings visualization saved.")

if __name__ == "__main__":
    main()

def main():
    """
    Main function to process Excentus data, generate visualizations, and export results to Excel.
    """
    # Load data from Excel files
    monthly_excentus_source_df = pd.read_excel(generate_path("Site_Redeemer_Issuer_Settlement_3160398.xlsx"), skiprows=1)
    site_list_source_df = pd.read_excel(generate_path("Shell_Site_List.xlsx"))
    previous_vendor_discount_source_df = pd.read_excel(generate_path("March_Vendor_Discount.xlsm"))

    # Data cleaning and processing for site list
    site_list_df = site_list_source_df.copy()
    site_list_df.rename(columns={"Merchant_Id_1": "Site ID"}, inplace=True)
    site_list_df["Site ID"] = site_list_df["Site ID"].astype(str)

    # Data cleaning and processing for monthly Excentus data
    monthly_excentus_df = monthly_excentus_source_df.iloc[: len(monthly_excentus_source_df) - 2].copy()
    columns_to_filter_out = ["Post Date", "Site Name", "Total Discounted Gallons", 
                              "Total Discounts Redeemed", "Site Funded", 
                              "Redemption Fee", "Issuance Fee", "Flat Fee", 
                              "Program ID", "Type"]
    
    monthly_excentus_filtered_df = monthly_excentus_df[~monthly_excentus_df.isin(columns_to_filter_out)]
    monthly_excentus_filtered_df["Site ID"] = monthly_excentus_filtered_df["Site ID"].astype(str).apply(lambda x: x[:-2] if x.endswith(".0") else x)

    # Data cleaning and processing for previous vendor discount data
    previous_vendor_discount_df = previous_vendor_discount_source_df.copy()
    previous_vendor_discount_df.rename(columns={"Site ID": "Customer Name", "Site Name": "Customer #"}, inplace=True)
    grouped_monthly_excentus = monthly_excentus_filtered_df.groupby("Site ID").sum().reset_index()

    # Merge and sort data
    merged_site_list_excentus = pd.merge(site_list_df, grouped_monthly_excentus, on="Site ID", how="outer")
    sorted_merged_excentus = merged_site_list_excentus.sort_values(by="Customer #")
    
    # Prepare data for export and analysis
    current_vendor_discount = sorted_merged_excentus[["Site ID", "Customer #", "Vendor Funded Discounts"]]
    current_vendor_discount.to_excel(generate_output_path("May_Vendor_Funded_Discounts.xlsx"), index=False)

    current_month_payables_excentus = sorted_merged_excentus.drop(columns=["Vendor Funded Discounts"], inplace=False)
    previous_vendor_discount_df = previous_vendor_discount_df.dropna()

    # Merge current and previous vendor discount data
    merged_excentus_vd = pd.merge(previous_vendor_discount_df, current_month_payables_excentus, on="Customer #", how="outer", suffixes=("_new", "_curr"))
    merged_excentus_vd["Vendor Funded Discounts"] = merged_excentus_vd["Vendor Funded Discounts"].fillna(0)

    # Round numerical columns to two decimal places
    columns_to_round = ["Vendor Funded Discounts", "Total Receivable - Daily", "Total Payable - Daily"]
    merged_excentus_vd[columns_to_round] = merged_excentus_vd[columns_to_round].round(2)

    # Prepare final data for export
    merged_excentus_vd_dropped = merged_excentus_vd.drop("Customer Name_new", axis=1, inplace=False)
    merged_excentus_vd_renamed = merged_excentus_vd_dropped.rename(columns={"Customer Name_curr": "Customer Name", "Total Payable - Daily": "Total Payable"}, inplace=False)
    merged_excentus_vd_renamed["Total Receivable"] = merged_excentus_vd_renamed["Total Receivable - Daily"] + merged_excentus_vd_renamed["Vendor Funded Discounts"]
    
    columns_to_drop = ["Vendor Funded Discounts", "Total Receivable - Daily"]
    total_sum_excentus = merged_excentus_vd_renamed.drop(columns=columns_to_drop, inplace=False)

    # Set the order of columns
    new_order = ["Site ID", "Customer Name", "Customer #", "Total Receivable", "Total Payable"]
    pre_mas_entry_excentus = total_sum_excentus[new_order]

    # Calculate totals across numerical columns
    totals = pre_mas_entry_excentus.select_dtypes(include=[float, int]).sum()
    totals_df = pd.DataFrame(totals).T
    totals_df.index = ["Totals"]  # Set index label for the totals row

    # Concatenate totals_df with pre_mas_entry_excentus
    df_totals = pd.concat([pre_mas_entry_excentus, totals_df])

    # Create a visualization
    create_visualization(df_totals)

    # Export final results to Excel
    df_totals.to_excel(generate_output_path("May_2024_Excentus.xlsx"), index=False)

    print("Files have been saved to the output directory.")

if __name__ == "__main__":
    main()
