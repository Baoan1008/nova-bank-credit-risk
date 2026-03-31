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

# ─────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────
DATA_PATH = "Credit_Risk_Dataset.xlsx"   # change to your path
SEP = "=" * 60


# ─────────────────────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────────────────────
print(SEP)
print("NOVA BANK CREDIT RISK — FULL ANALYSIS")
print(SEP)

df = pd.read_excel(DATA_PATH)
print(f"\nDataset loaded: {df.shape[0]:,} rows × {df.shape[1]} columns")


# ─────────────────────────────────────────────────────────────
# 2. DATASET OVERVIEW
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 60)
print("SECTION 1 — DATASET OVERVIEW")
print("─" * 60)

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes.to_string())

print("\nMissing values per column:")
missing = df.isnull().sum()
print(missing[missing > 0].to_string() if missing.any() else "None")

print("\nDescriptive statistics (numeric columns):")
print(df.describe().round(2).to_string())

print("\nCategorical value counts:")
cat_cols = df.select_dtypes(include="object").columns.tolist()
for col in cat_cols:
    print(f"\n  {col}:")
    print(df[col].value_counts().to_string())


# ─────────────────────────────────────────────────────────────
# 3. DEFAULT RATE ANALYSIS
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 60)
print("SECTION 2 — DEFAULT RATE ANALYSIS")
print("─" * 60)

total     = len(df)
defaults  = df["loan_status"].sum()
def_rate  = df["loan_status"].mean()
print(f"\nTotal borrowers : {total:,}")
print(f"Total defaults  : {int(defaults):,}")
print(f"Default rate    : {def_rate:.1%}")


def default_table(col):
    """Return a summary table: count, defaults, default_rate per category."""
    return (
        df.groupby(col)["loan_status"]
          .agg(count="count", defaults="sum", default_rate="mean")
          .assign(default_rate=lambda x: x["default_rate"].round(3))
          .sort_values("default_rate", ascending=False)
    )


print("\n--- By loan grade ---")
print(default_table("loan_grade").to_string())

print("\n--- By loan intent ---")
print(default_table("loan_intent").to_string())

print("\n--- By home ownership ---")
print(default_table("person_home_ownership").to_string())

print("\n--- By employment type ---")
print(default_table("employment_type").to_string())

print("\n--- By prior default on file ---")
print(default_table("cb_person_default_on_file").to_string())

print("\n--- By country ---")
print(default_table("country").to_string())

print("\n--- By loan term (months) ---")
print(default_table("loan_term_months").to_string())


# ─────────────────────────────────────────────────────────────
# 4. NUMERIC CORRELATIONS WITH DEFAULT
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 60)
print("SECTION 3 — NUMERIC CORRELATIONS WITH LOAN_STATUS")
print("─" * 60)

numeric_cols = df.select_dtypes(include="number").columns.tolist()
corr = (
    df[numeric_cols]
      .corr()["loan_status"]
      .drop("loan_status")
      .sort_values(key=abs, ascending=False)
      .round(4)
)
print(corr.to_string())


# ─────────────────────────────────────────────────────────────
# 5. BORROWER PROFILE COMPARISON
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 60)
print("SECTION 4 — BORROWER PROFILE: DEFAULT vs NON-DEFAULT")
print("─" * 60)

profile_cols = [
    "person_income", "loan_amnt", "loan_int_rate",
    "loan_to_income_ratio", "debt_to_income_ratio",
    "person_age", "cb_person_cred_hist_length",
    "credit_utilization_ratio", "other_debt"
]
profile = df.groupby("loan_status")[profile_cols].mean().round(2)
profile.index = ["Non-default (0)", "Default (1)"]
print(profile.T.to_string())


# ─────────────────────────────────────────────────────────────
# 6. DEMOGRAPHIC ANALYSIS
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 60)
print("SECTION 5 — DEMOGRAPHIC ANALYSIS")
print("─" * 60)

# Age buckets
df["age_bucket"] = pd.cut(
    df["person_age"],
    bins=[18, 25, 35, 45, 55, 200],
    labels=["18-25", "26-35", "36-45", "46-55", "55+"]
)
print("\n--- By age group ---")
print(
    df.groupby("age_bucket", observed=True)["loan_status"]
      .agg(count="count", default_rate="mean")
      .assign(default_rate=lambda x: x["default_rate"].round(3))
      .to_string()
)

print("\n--- By gender ---")
print(default_table("gender").to_string())

print("\n--- By education level ---")
print(default_table("education_level").to_string())

print("\n--- By marital status ---")
print(default_table("marital_status").to_string())


# ─────────────────────────────────────────────────────────────
# 7. GEOGRAPHIC ANALYSIS
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 60)
print("SECTION 6 — GEOGRAPHIC ANALYSIS")
print("─" * 60)

print("\n--- By state / region ---")
state_df = (
    df.groupby(["state", "country"])["loan_status"]
      .agg(count="count", default_rate="mean")
      .reset_index()
      .sort_values("default_rate", ascending=False)
)
state_df["default_rate"] = state_df["default_rate"].round(3)
print(state_df.to_string(index=False))

print("\n--- By city (min 200 borrowers) ---")
city_df = (
    df.groupby(["city", "country"])["loan_status"]
      .agg(count="count", default_rate="mean")
      .reset_index()
)
city_df["default_rate"] = city_df["default_rate"].round(3)
city_df = city_df[city_df["count"] >= 200].sort_values("default_rate", ascending=False)
print(city_df.to_string(index=False))


# ─────────────────────────────────────────────────────────────
# 8. INTEREST RATE & LOAN AMOUNT BUCKETS
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 60)
print("SECTION 7 — INTEREST RATE & LOAN SIZE BUCKETS")
print("─" * 60)

df["rate_bucket"] = pd.cut(
    df["loan_int_rate"],
    bins=[0, 8, 11, 14, 17, 30],
    labels=["<8%", "8-11%", "11-14%", "14-17%", ">17%"]
)
print("\n--- Default rate by interest rate bucket ---")
print(
    df.groupby("rate_bucket", observed=True)["loan_status"]
      .agg(count="count", default_rate="mean")
      .assign(default_rate=lambda x: x["default_rate"].round(3))
      .to_string()
)

df["loan_size_bucket"] = pd.cut(
    df["loan_amnt"],
    bins=[0, 5000, 10000, 20000, 50000, 1e9],
    labels=["<$5K", "$5-10K", "$10-20K", "$20-50K", ">$50K"]
)
print("\n--- Default rate by loan amount bucket ---")
print(
    df.groupby("loan_size_bucket", observed=True)["loan_status"]
      .agg(count="count", default_rate="mean")
      .assign(default_rate=lambda x: x["default_rate"].round(3))
      .to_string()
)

df["income_bucket"] = pd.cut(
    df["person_income"],
    bins=[0, 30000, 50000, 80000, 150000, 1e9],
    labels=["<$30K", "$30-50K", "$50-80K", "$80-150K", ">$150K"]
)
print("\n--- Default rate by income bucket ---")
print(
    df.groupby("income_bucket", observed=True)["loan_status"]
      .agg(count="count", default_rate="mean")
      .assign(default_rate=lambda x: x["default_rate"].round(3))
      .to_string()
)


# ─────────────────────────────────────────────────────────────
# 9. RISK SCORING MODEL
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 60)
print("SECTION 8 — RISK SCORING MODEL")
print("─" * 60)

def score_borrower(row):
    """
    Additive risk score (0–100). Higher = safer borrower.
    Factors: loan grade, loan-to-income ratio, prior default,
             home ownership, income level, interest rate.
    """
    score = 100

    # Loan grade (most impactful)
    grade_penalty = {"A": 0, "B": 5, "C": 15, "D": 40, "E": 55, "F": 65, "G": 80}
    score -= grade_penalty.get(row["loan_grade"], 0)

    # Loan-to-income ratio
    lti = row["loan_to_income_ratio"]
    if   lti >= 0.35: score -= 25
    elif lti >= 0.25: score -= 16
    elif lti >= 0.15: score -= 8

    # Prior default on file
    if row["cb_person_default_on_file"] == "Y":
        score -= 20

    # Home ownership
    own_bonus = {"OWN": 10, "MORTGAGE": 5, "RENT": 0, "OTHER": -2}
    score += own_bonus.get(row["person_home_ownership"], 0)

    # Annual income
    inc = row["person_income"]
    if   inc >= 80000: score += 5
    elif inc >= 50000: score += 2
    elif inc <  30000: score -= 8

    # Interest rate
    rate = row["loan_int_rate"]
    if   rate >= 18: score -= 10
    elif rate >= 14: score -= 5

    return max(0, min(100, score))


df["risk_score"] = df.apply(score_borrower, axis=1)
df["risk_tier"]  = pd.cut(
    df["risk_score"],
    bins=[0, 40, 60, 80, 100],
    labels=["High Risk", "Medium Risk", "Low Risk", "Very Low Risk"]
)

print("\nRisk score summary statistics:")
print(df["risk_score"].describe().round(2))

print("\nRisk tier distribution & actual default rates:")
tier_summary = (
    df.groupby("risk_tier", observed=True)["loan_status"]
      .agg(borrowers="count", defaults="sum", actual_default_rate="mean")
      .assign(actual_default_rate=lambda x: x["actual_default_rate"].round(3))
)
print(tier_summary.to_string())

print("\nDefault rate by score decile:")
df["score_decile"] = pd.qcut(df["risk_score"], q=10, duplicates="drop")
print(
    df.groupby("score_decile", observed=True)["loan_status"]
      .mean().round(3).to_string()
)


# ─────────────────────────────────────────────────────────────
# 10. EXPORT ENRICHED DATASET
# ─────────────────────────────────────────────────────────────
print("\n" + "─" * 60)
print("SECTION 9 — EXPORT ENRICHED DATASET")
print("─" * 60)

export_cols = df.columns.tolist()
out_path = "credit_risk_enriched.csv"
df.to_csv(out_path, index=False)
print(f"\nEnriched dataset (with risk_score, risk_tier, age_bucket, etc.)")
print(f"Saved to: {out_path}")
print(f"Rows: {len(df):,}  |  Columns: {len(df.columns)}")

print("\n" + SEP)
print("ANALYSIS COMPLETE")
print(SEP)
