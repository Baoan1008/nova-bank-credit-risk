Nova Bank — Credit Risk Analysis
View Live Dashboard →
An end-to-end credit risk analysis for Nova Bank, a lender operating across the US, UK, and Canada. Built to identify who defaults, why, and how to make smarter lending decisions — while keeping lending fair and accessible.
Tools: Python (pandas, numpy) · Interactive HTML Dashboard (Chart.js) · Excel/CSV · Word report generator (docx.js)

Key Findings
1. Loan grade is the single strongest default predictor
GradeBorrowersDefault RateA10,77710.0%B10,45116.3%C6,45820.7%D3,62659.0%E96464.4%F24170.5%G6498.4%
Grade D–G loans default at 3–10× the rate of Grade A–B.
2. Loan-to-income ratio is the strongest numeric predictor (r = 0.39)
LTI RatioDefault Rate< 15%12%15–25%18%25–35%42%> 35%72%
Borrowers with LTI above 35% default at 6× the rate of low-LTI borrowers.
3. Prior default history doubles default probability
Borrowers with a prior default on file: 37.8% vs 18.4% for clean-file borrowers.
4. Home ownership is a major risk signal
OwnershipDefault RateOwn7.5%Mortgage12.6%Rent31.6%Other30.8%
Renters default at 4× the rate of outright owners.
5. Loan purpose matters
Debt consolidation (28.6%) and medical loans (26.7%) carry the highest default rates. Venture loans are the lowest risk (14.8%).
6. No meaningful geographic difference across US, UK, Canada
Default rates: USA 21.9%, UK 21.7%, Canada 21.9%. Risk is in the borrower, not the country.
7. Demographics show no bias
Gender, education, and marital status show no meaningful difference in default rates (all within 1%). The model is fair.

Risk Scoring Model
A rule-based additive scoring model (0–100, higher = safer) built on the top predictive factors:
Risk TierScoreBorrowersActual Default RateVery Low Risk81–10020,6387.4%Low Risk61–805,83735.8%Medium Risk41–602,95642.4%High Risk0–403,15070.8%

Recommendations for Nova Bank
1. Cut Grade D–G exposure immediately
Grade D–G is only 15% of the portfolio but generates 42% of all defaults — 2,995 bad loans on $34.2M of capital. A hard cap on Grade F/G (where default rates hit 70–98%) and tighter underwriting for Grade D/E would remove the highest-cost segment with minimal impact on approved loan volume. The trade-off is clear: these 4,895 borrowers cost more in defaults than they generate in interest.
2. Make LTI > 35% a hard stop, not a soft flag
Just 7.1% of borrowers have a loan-to-income ratio above 35%, but they account for 23% of all defaults and $26.6M in defaulted loan value. Their 72% default rate is 6× the rate of borrowers below 15% LTI. This is the single most actionable policy lever available — a hard cutoff at 35% LTI removes disproportionate risk with minimal loan volume lost.
3. Use combined risk signals, not single factors
Individual factors are useful, but combinations are devastating:

Prior default + Renter → 46.9% default rate (3,278 borrowers)
Prior default + Grade D–G → 61.5% default rate (2,489 borrowers)
Clean file + Homeowner/Mortgage → 9.3% default rate (13,590 borrowers)

Nova Bank should score applicants on combined signals. The clean-file homeowner segment is nearly as safe as Grade A loans and represents a large, underserved opportunity.
4. Stop treating "renters" as one risk category
The 31.6% default rate for renters masks a critical split: renters who are Grade A/B with LTI below 20% default at just 7.6% — comparable to mortgage holders. Meanwhile, renters with LTI above 35% default at 100% in this dataset. Rejecting all renters loses 6,403 creditworthy borrowers. The fix is to approve renters on grade + LTI, not tenure status.
5. Loan purpose risk is driven by grade, not purpose
Debt consolidation (28.6%) and medical loans (26.7%) appear risky — but when filtered to Grade A/B borrowers, their default rates drop to 14.8% and 14.3% respectively. The purpose is not the risk driver; the grade is. Nova Bank should not restrict loan purpose but should apply grade and LTI standards uniformly across all purposes.
6. Deploy the risk scoring model as a first-pass filter
Rejecting the bottom 9.7% of applicants (High Risk score 0–40) would eliminate 31.4% of all defaults and protect $27.4M in loan value. The Very Low Risk tier (81–100) — 63% of the portfolio — defaults at just 7.4% and represents $183M in safe loan volume. A tiered approval policy (auto-approve Very Low, review Low/Medium, require collateral for High) would make the process faster and more defensible.

Repository Structure
nova-bank-credit-risk/
├── nova_bank_powerbi_dashboard.html  # Interactive dashboard (Chart.js)
├── nova_bank_analysis.py             # Full Python analysis (9 sections)
├── nova_bank_report_generator.js     # Automated Word report builder (docx.js)
├── credit_risk_enriched.csv          # Dataset enriched with risk scores
├── Credit_Risk_Dataset.xlsx          # Original dataset (32,581 rows, 29 cols)
└── README.md

How to Run
bash# Install dependencies
pip install pandas numpy openpyxl

# Run full analysis
python nova_bank_analysis.py

# Open dashboard in any browser
open nova_bank_powerbi_dashboard.html

# Generate Word report
npm install docx
node nova_bank_report_generator.js

Dataset
32,581 personal loan records · US, UK, Canada · 29 features
Overall default rate: 21.8% (7,108 defaults) · Missing: loan_int_rate (9.6%), person_emp_length (2.7%)
All data is synthetic/anonymised. Project completed as part of the Nova Bank Credit Risk Challenge.
