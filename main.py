import pandas as pd
import os


def main():

    def generate_path(file_name_str):
        """Helper function that generates correct path based on user's OS system"""
        return os.path.join(".", "data", file_name_str)
    
    def generate_output_path(new_file_name_str):
        """Make a note here"""
        return os.path.join(".", "output_data", new_file_name_str)
    ##########################
    #####   LOAD DATA    #####
    ##########################
    
    
    monthly_excentus_source_df = pd.read_excel(generate_path("Site_Redeemer_Issuer_Settlement_3160398.xlsx"), skiprows=1)
    site_list_source_df = pd.read_excel(generate_path("Shell_Site_List.xlsx"))
    vendor_discount_source_df = pd.read_excel(generate_path("March_Vendor_Discount.xlsm"))


    #########################################
    ###   ANALYSIS 1: Monthly Excentus    ###
    #########################################
    
    # GOAL: write a small thing explaining what this first analysis is doing. You're telling a story through your code
    
    
    #########################
    # Task 1: Data Cleaning #
    #########################
    
    # OK Note: Either use double quotes or single throughout your code
    columns_to_filter_out = ["Post Date", "Site Name", "Total Discounted Gallons", "Total Discounts Redeemed", 
    "Site Funded", "Redemption Fee", "Issuance Fee", "Flat Fee", "Program ID", "Type"]

    site_list_df= site_list_source_df.copy()
    site_list_df.rename(columns={"Merchant_Id_1":"Site ID"}, inplace=True)
    site_list_df["Site ID"] = site_list_df["Site ID"].astype(str)
    

    #OK Note: rather than delete data in place, which could lead to things happening that you can't account for, just filter
    monthly_excentus_df= monthly_excentus_source_df.iloc[: len(monthly_excentus_source_df) - 2].copy() #OK Note: makes copy of this data in memory so if you alter the monthly_execentus_df, it won't effect this df
    
    #look at pandas method isin, this allows you to filter. That little make (~) means here return all elements that are NOT in the list
    monthly_excentus_filtered_df = monthly_excentus_df[~monthly_excentus_df.isin(columns_to_filter_out)]
    

    monthly_excentus_filtered_df['Site ID'] = monthly_excentus_filtered_df['Site ID'].astype(str)
    monthly_excentus_filtered_df['Site ID'] = monthly_excentus_filtered_df['Site ID'].astype(str).apply(lambda x: x[:-2] if x.endswith('.0') else x)


    previous_vendor_discount_df = vendor_discount_source_df.copy() #makes copy so you don't overwrite the original data
    previous_vendor_discount_df.rename(columns={"Site ID": "Customer Name", "Site Name": "Customer #"}, inplace=True)
    grouped_monthly_excentus = monthly_excentus_filtered_df.groupby("Site ID").sum().reset_index()

    
    merged_site_list_excentus = pd.merge(site_list_df, grouped_monthly_excentus, on= "Site ID", how="outer")


    #notice i group together some elemtns that go togehter
    sorted_merged_excentus = merged_site_list_excentus.sort_values(by="Customer #")
    current_vendor_discount = sorted_merged_excentus[["Site ID", "Customer #", "Vendor Funded Discounts"]]
    current_vendor_discount.to_excel(generate_output_path("May_Vendor_Funded_Discounts.xlsx"), index=False)

    print("Done")


    # LEAVING YOU SOME HINTS ABOVE, now practice with the bottom


    # current_month_payables_excentus = sorted_merged_excentus.drop(columns=["Vendor Funded Discounts"], inplace=False)

    # previous_vendor_discount.rename(columns={"Site Name": "Customer #"}, inplace=True)

    # previous_vendor_discount = previous_vendor_discount.dropna()

    # merged_excentus_vd = pd.merge(previous_vendor_discount,current_month_payables_excentus,on="Customer #",how="outer",suffixes=('_new', '_curr'))

    # merged_excentus_vd["Vendor Funded Discounts"] = merged_excentus_vd["Vendor Funded Discounts"].fillna(0)

    # columns_to_round = ["Vendor Funded Discounts", "Total Receivable - Daily", "Total Payable - Daily"]
    # merged_excentus_vd[columns_to_round] = merged_excentus_vd[columns_to_round].round(2)

    # merged_excentus_vd_dropped = merged_excentus_vd.drop("Customer Name_new", axis=1, inplace=False)

    # merged_excentus_vd_renamed = merged_excentus_vd_dropped.rename(columns={"Customer Name_curr": "Customer Name",  "Total Payable - Daily": "Total Payable"}, inplace=False)

    # merged_excentus_vd_renamed["Total Receivable"] = merged_excentus_vd_renamed["Total Receivable - Daily"] + merged_excentus_vd_renamed["Vendor Funded Discounts"]


    # columns_to_drop = ['Vendor Funded Discounts', 'Total Receivable - Daily']
    # total_sum_excentus = merged_excentus_vd_renamed.drop(columns=columns_to_drop, inplace=False)

    # new_order = ["Site ID", "Customer Name", "Customer #", "Total Receivable", "Total Payable"]
    # pre_mas_entry_excentus = total_sum_excentus[new_order]
    # pre_mas_entry_excentus


    # totals = pre_mas_entry_excentus.select_dtypes(include=[float, int]).sum()

    # totals_df = pd.DataFrame(totals).T
    # totals_df.index = ['Totals']  # Set index label for the totals row


    # df_totals = pd.concat([pre_mas_entry_excentus, totals_df])

    # df_totals.to_excel("May_2024_Excentus.xlsx", index=False)


    # df = pd.read_excel(r"C:\Users\lesli\github-classroom\Testing\Shell Site List 06-05-2024.xlsx")
    # print(df.head())  # Print first few rows of DataFrame

    # print("Script completed.")
    
    
# PROGRAM BEGINS HERE WHEN SCRIPT IS RUN

if __name__ == "__main__":
    main()