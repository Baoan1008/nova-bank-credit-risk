"""
=============================================================
NOVA BANK — Credit Risk Analysis Script
=============================================================
Author  : Credit Risk Analytics Team
Dataset : Credit_Risk_Dataset.xlsx  (32,581 rows, 29 columns)
Output  : Prints full analysis results to console
=============================================================
"""

import pandas as pd
import numpy as np

DATA_PATH = "Credit_Risk_Dataset.xlsx"
SEP = "=" * 60

print(SEP)
print("NOVA BANK CREDIT RISK — FULL ANALYSIS")
print(SEP)

df = pd.read_excel(DATA_PATH)
print(f"\nDataset loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")

# ─────────────────────────────────────────────────────────────
# SECTION 1 — DATASET OVERVIEW
# ─────────────────────────────────────────────────────────────
print("\n" + "─"*60)
print("SECTION 1 — DATASET OVERVIEW")
print("─"*60)

print("\nColumns:", df.columns.tolist())
print("\nData types:\n", df.dtypes.to_string())

missing = df.isnull().sum()
print("\nMissing values:")
print(missing[missing > 0].to_string() if missing.any() else "None")
print(f"  Note: loan_int_rate has {missing.get('loan_int_rate',0):,} missing ({missing.get('loan_int_rate',0)/len(df)*100:.1f}%)")

print("\nDescriptive statistics:\n", df.describe().round(2).to_string())

for col in df.select_dtypes(include="object").columns:
    print(f"\n  {col}: {df[col].value_counts().to_dict()}")

# ─────────────────────────────────────────────────────────────
# SECTION 2 — DEFAULT RATE ANALYSIS
# ─────────────────────────────────────────────────────────────
print("\n" + "─"*60)
print("SECTION 2 — DEFAULT RATE ANALYSIS")
print("─"*60)

print(f"\nTotal borrowers : {len(df):,}")
print(f"Total defaults  : {df.loan_status.sum():,}")
print(f"Default rate    : {df.loan_status.mean()*100:.2f}%")

def default_table(col):
    return (df.groupby(col)["loan_status"]
              .agg(count="count", defaults="sum", default_rate="mean")
              .assign(default_rate=lambda x: (x["default_rate"]*100).round(2))
              .sort_values("default_rate", ascending=False))

for label, col in [
    ("Loan Grade",          "loan_grade"),
    ("Loan Intent",         "loan_intent"),
    ("Home Ownership",      "person_home_ownership"),
    ("Employment Type",     "employment_type"),
    ("Prior Default",       "cb_person_default_on_file"),
    ("Country",             "country"),
    ("Loan Term (months)",  "loan_term_months"),
]:
    print(f"\n--- By {label} ---")
    print(default_table(col).to_string())

# ─────────────────────────────────────────────────────────────
# SECTION 3 — NUMERIC CORRELATIONS
# ─────────────────────────────────────────────────────────────
print("\n" + "─"*60)
print("SECTION 3 — NUMERIC CORRELATIONS WITH LOAN_STATUS")
print("─"*60)

num_cols = df.select_dtypes(include="number").columns.tolist()
corr = (df[num_cols].corr()["loan_status"]
          .drop("loan_status")
          .reindex(lambda s: s.abs().sort_values(ascending=False).index, axis=0)
          .round(4))
print(corr.to_string())

# ─────────────────────────────────────────────────────────────
# SECTION 4 — BORROWER PROFILE: DEFAULT vs NON-DEFAULT
# ─────────────────────────────────────────────────────────────
print("\n" + "─"*60)
print("SECTION 4 — BORROWER PROFILE: DEFAULT vs NON-DEFAULT")
print("─"*60)

profile_cols = ["person_income","loan_amnt","loan_int_rate","loan_to_income_ratio",
                "debt_to_income_ratio","person_age","cb_person_cred_hist_length",
                "credit_utilization_ratio","other_debt"]
profile = df.groupby("loan_status")[profile_cols].mean().round(2)
profile.index = ["Non-default","Default"]
print(profile.T.to_string())

# ─────────────────────────────────────────────────────────────
# SECTION 5 — DEMOGRAPHIC ANALYSIS
# ─────────────────────────────────────────────────────────────
print("\n" + "─"*60)
print("SECTION 5 — DEMOGRAPHIC ANALYSIS")
print("─"*60)

df["age_bucket"] = pd.cut(df["person_age"], bins=[18,25,35,45,55,200],
                           labels=["18-25","26-35","36-45","46-55","55+"])
print("\n--- By age group ---")
print(df.groupby("age_bucket", observed=True)["loan_status"]
        .agg(count="count", default_rate="mean")
        .assign(default_rate=lambda x: (x["default_rate"]*100).round(2)).to_string())

for label, col in [("Gender","gender"),("Education","education_level"),("Marital Status","marital_status")]:
    print(f"\n--- By {label} ---")
    print(default_table(col).to_string())

# ─────────────────────────────────────────────────────────────
# SECTION 6 — GEOGRAPHIC ANALYSIS
# ─────────────────────────────────────────────────────────────
print("\n" + "─"*60)
print("SECTION 6 — GEOGRAPHIC ANALYSIS")
print("─"*60)

state_df = (df.groupby(["state","country"])["loan_status"]
              .agg(count="count", default_rate="mean").reset_index()
              .assign(default_rate=lambda x: (x["default_rate"]*100).round(2))
              .sort_values("default_rate", ascending=False))
print("\n--- By state/region ---")
print(state_df.to_string(index=False))

city_df = (df.groupby(["city","country"])["loan_status"]
             .agg(count="count", default_rate="mean").reset_index()
             .assign(default_rate=lambda x: (x["default_rate"]*100).round(2)))
city_df = city_df[city_df["count"] >= 200].sort_values("default_rate", ascending=False)
print("\n--- By city (min 200 borrowers) ---")
print(city_df.to_string(index=False))

# ─────────────────────────────────────────────────────────────
# SECTION 7 — INTEREST RATE & LOAN SIZE BUCKETS
# ─────────────────────────────────────────────────────────────
print("\n" + "─"*60)
print("SECTION 7 — INTEREST RATE & LOAN SIZE BUCKETS")
print("─"*60)

df_r = df.dropna(subset=["loan_int_rate"]).copy()
df_r["rate_bucket"] = pd.cut(df_r["loan_int_rate"], bins=[0,8,11,14,17,100],
                               labels=["<8%","8-11%","11-14%","14-17%",">17%"])
print("\n--- Default rate by interest rate band ---")
print(df_r.groupby("rate_bucket", observed=True)["loan_status"]
          .agg(count="count", default_rate="mean")
          .assign(default_rate=lambda x: (x["default_rate"]*100).round(2)).to_string())

df["loan_size_bucket"] = pd.cut(df["loan_amnt"], bins=[0,5000,10000,20000,50000,1e9],
                                 labels=["<$5K","$5-10K","$10-20K","$20-50K",">$50K"])
print("\n--- Default rate by loan amount ---")
print(df.groupby("loan_size_bucket", observed=True)["loan_status"]
        .agg(count="count", default_rate="mean")
        .assign(default_rate=lambda x: (x["default_rate"]*100).round(2)).to_string())

df["income_bucket"] = pd.cut(df["person_income"], bins=[0,30000,50000,80000,150000,1e9],
                               labels=["<$30K","$30-50K","$50-80K","$80-150K",">$150K"])
print("\n--- Default rate by income band ---")
print(df.groupby("income_bucket", observed=True)["loan_status"]
        .agg(count="count", default_rate="mean")
        .assign(default_rate=lambda x: (x["default_rate"]*100).round(2)).to_string())

# ─────────────────────────────────────────────────────────────
# SECTION 8 — RISK SCORING MODEL
# ─────────────────────────────────────────────────────────────
print("\n" + "─"*60)
print("SECTION 8 — RISK SCORING MODEL")
print("─"*60)

def score_borrower(row):
    """
    Additive risk score (0-100). Higher = safer borrower.
    Factors: loan grade, LTI, prior default, home ownership, income, interest rate.
    """
    s = 100
    s -= {"A":0,"B":5,"C":15,"D":40,"E":55,"F":65,"G":80}.get(row["loan_grade"], 0)
    lti = row["loan_to_income_ratio"]
    if lti >= 0.35:   s -= 25
    elif lti >= 0.25: s -= 16
    elif lti >= 0.15: s -= 8
    if row["cb_person_default_on_file"] == "Y": s -= 20
    s += {"OWN":10,"MORTGAGE":5,"RENT":0,"OTHER":-2}.get(row["person_home_ownership"], 0)
    inc = row["person_income"]
    if inc >= 80000:   s += 5
    elif inc >= 50000: s += 2
    elif inc < 30000:  s -= 8
    rate = row["loan_int_rate"] if pd.notna(row["loan_int_rate"]) else 12
    if rate >= 18:   s -= 10
    elif rate >= 14: s -= 5
    return max(0, min(100, s))

df["risk_score"] = df.apply(score_borrower, axis=1)
df["risk_tier"] = pd.cut(df["risk_score"], bins=[0,40,60,80,100],
                          labels=["High Risk","Medium Risk","Low Risk","Very Low Risk"],
                          include_lowest=True)

print("\nRisk score statistics:")
print(df["risk_score"].describe().round(2))

print("\nRisk tier distribution & actual default rates:")
tier = (df.groupby("risk_tier", observed=True)["loan_status"]
          .agg(borrowers="count", defaults="sum", actual_default_rate="mean")
          .assign(actual_default_rate=lambda x: (x["actual_default_rate"]*100).round(2)))
print(tier.to_string())

df["score_decile"] = pd.qcut(df["risk_score"], q=10, duplicates="drop")
print("\nDefault rate by score decile:")
print((df.groupby("score_decile", observed=True)["loan_status"].mean()*100).round(2).to_string())

# ─────────────────────────────────────────────────────────────
# SECTION 9 — EXPORT
# ─────────────────────────────────────────────────────────────
print("\n" + "─"*60)
print("SECTION 9 — EXPORT ENRICHED DATASET")
print("─"*60)

out_path = "credit_risk_enriched.csv"
df.to_csv(out_path, index=False)
print(f"\nSaved to: {out_path}")
print(f"Rows: {len(df):,}  Columns: {len(df.columns)}")

print("\n" + SEP)
print("ANALYSIS COMPLETE")
print(SEP)
