
# *************************************
# 1. LOAD DATA
# *************************************
import pandas as pd 
inventory = pd.read_parquet(
    r"C:\Users\FEYZA KARA\Downloads\surplus-solutions-showcase-main\surplus-solutions-showcase-main\market_data_output_15d\inventory_snapshot.parquet"
)

sales = pd.read_parquet(
    r"C:\Users\FEYZA KARA\Downloads\surplus-solutions-showcase-main\surplus-solutions-showcase-main\market_data_output_15d\sales_3y.parquet"
)
inventory.head() 
# **************************************
# 2. DATETIME
# **************************************
inventory["snapshot_ts"] = pd.to_datetime(inventory["snapshot_ts"])
inventory["expiry_date"] = pd.to_datetime(inventory["expiry_date"])
# *****************************************
# 3. DAYS TO EXPIRY
# ******************************************
inventory["days_to_expiry"] = (inventory["expiry_date"] - inventory["snapshot_ts"]).dt.days 
# ********************************************
# 4. DAILY VELOCITY
# ********************************************
velocity = (
    sales.groupby(["store_id","sku"])["qty"]
    .sum()
    .reset_index()
)

velocity["daily_velocity"] = velocity["qty"] / 15
velocity = velocity.drop(columns=["qty"])

velocity.head()
# *****************************************
# 5. MERGE
# *****************************************
data = inventory.merge(velocity, on=["store_id","sku"], how="left")
data["daily_velocity"] = data["daily_velocity"].fillna(0)

data.head() 
# ******************************************
# 6. COVERAGE
# ******************************************
data["coverage_days"] = data["on_hand_qty"] / (data["daily_velocity"] + 1e-6)
data["coverage_days"] = data["coverage_days"].clip(upper=365)

data[["on_hand_qty","daily_velocity","coverage_days"]].head()
# *****************************************
# 7. RISK SCORE
# *****************************************
data["core_risk"] = ( data["coverage_days"] / (data["days_to_expiry"] + 1))

data["stock_norm"] = (data["on_hand_qty"] / data["on_hand_qty"].max())

data["risk_score"] = (0.8 * data["core_risk"] +0.2 * data["stock_norm"])
data[["coverage_days", "days_to_expiry", "core_risk", "stock_norm", "risk_score"]].head()
# ******************************************
# 8. RISK BUCKETS
# ******************************************
def risk_bucket(x):
    if x < 0.5:
        return "low"
    elif x < 1:
        return "medium"
    else:
        return "high"

data["risk_level"] = data["risk_score"].apply(risk_bucket)

data["risk_level"].value_counts()
# ******************************************
# 9. TOP RISKY INVENTORY
# ******************************************
top20 = (
    data
    .sort_values("risk_score", ascending=False)
    .head(20))

print("\nTop 20 Risky Inventory:\n")

print(top20[[
    "store_id",
    "sku",
    "on_hand_qty",
    "days_to_expiry",
    "coverage_days",
    "risk_score",
    "risk_level"]])

top20.to_csv(
    "top_20_risky_inventory.csv",
    index=False)




