

"""
file_path = "data/processed/usd_egp_monthly.csv"
df = pd.read_csv(file_path)

df = df[df['month'] != '2026-10']
df.to_csv(file_path,index=False)
print("Done !")
"""

"""
data_processing("data/raw/frankfurter_usd_egp.csv", "data/processed/usd_egp_monthly.csv")

data = fetch_data(start_date="2016-10-01",end_date="2026-03-31",quote="EGP",base="USD")

file_path = "data/raw/frankfurter_usd_egp.csv"
save_data_csv(data, file_path)
"""


"""
data = fetch_data(start_date="2026-04-01",end_date="2026-10-25",quote="EGP",base="USD")

file_path = "data/raw/frankfurter_usd_egp_missing.csv"
save_data_csv(data, file_path)

data_processing("data/raw/frankfurter_usd_egp_missing.csv", "data/processed/usd_egp_monthly_were_missing.csv")
"""

"""
main_file_path = "data/processed/usd_egp_monthly.csv"
missing_file_path = "data/processed/usd_egp_monthly_were_missing.csv"

concat_missing_and_main(main_file_path, missing_file_path)
"""
