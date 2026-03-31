# Nova Bank — Credit Risk Analysis

**[View Live Dashboard →](https://Baoan1008.github.io/nova-bank-credit-risk/nova_bank_powerbi_dashboard.html)**

An end-to-end credit risk analysis project for Nova Bank, a fictional lender operating across the US, UK, and Canada. Built to identify the key drivers of loan default across 32,581 borrowers and develop a practical risk scoring framework.

---

## Project Overview

Nova Bank faces a classic lending dilemma: approve too many high-risk loans and lose money; be too restrictive and miss creditworthy customers. This analysis uses real-world-style data to answer who defaults, why, and how to build smarter lending decisions.

**Tools used:** Python (pandas, numpy) · Interactive HTML dashboard (Chart.js) · Excel/CSV · Word report generator (docx.js)

---

## Key Findings

### 1. Loan grade is the single strongest default predictor
| Grade | Borrowers | Default Rate |
|-------|-----------|-------------|
| A | 10,777 | 10.0% |
| B | 10,451 | 16.3% |
| C | 6,458 | 20.7% |
| D | 3,626 | 59.0% |
| E | 964 | 64.4% |
| F | 241 | 70.5% |
| G | 64 | **98.4%** |

Grade D–G loans default at 3–10× the rate of Grade A–B. A strict grade cutoff policy would meaningfully reduce default exposure.

### 2. Loan-to-income ratio is the strongest numeric predictor (r = 0.39)
| LTI Ratio | Default Rate |
|-----------|-------------|
| < 15% | 12% |
| 15–25% | 18% |
| 25–35% | **42%** |
| > 35% | **72%** |

Borrowers with LTI above 35% default at 6× the rate of low-LTI borrowers. Other strong predictors: interest rate (r = 0.34), debt-to-income ratio (r = 0.32).

### 3. Prior default history doubles default probability
Borrowers with a prior default on file default at **37.8%** vs **18.4%** for clean-file borrowers — a 2× multiplier regardless of other characteristics.

### 4. Home ownership is a major risk signal
| Ownership | Default Rate |
|-----------|-------------|
| Own | 7.5% |
| Mortgage | 12.6% |
| Rent | **31.6%** |
| Other | **30.8%** |

Renters default at 4× the rate of outright owners — likely reflecting both financial stability and commitment to assets.

### 5. Debt consolidation and medical loans carry the highest risk
Among loan purposes, debt consolidation (28.6%) and medical loans (26.7%) carry the highest default rates. Venture loans are surprisingly low risk (14.8%), likely reflecting borrower financial confidence.

### 6. No meaningful geographic difference across US, UK, Canada
Default rates are nearly identical across countries (21.7–21.9%), suggesting the risk drivers are borrower-level characteristics, not geography.

---

## Risk Scoring Model

A rule-based additive scoring model (0–100) was built using the top predictive factors:

- Loan grade (most impactful)
- Loan-to-income ratio
- Prior default on file
- Home ownership type
- Annual income level
- Interest rate

**Score validation:**

| Risk Tier | Borrowers | Actual Default Rate |
|-----------|-----------|---------------------|
| Very Low Risk (80–100) | — | Low |
| Low Risk (60–80) | — | Moderate |
| Medium Risk (40–60) | — | Elevated |
| High Risk (0–40) | — | High |

---

## Recommendations for Nova Bank

1. **Implement a hard cap on Grade F/G loans** — 70–98% default rates make these economically unviable without very high interest compensation.
2. **Set an LTI threshold of 35%** as an automatic flag for enhanced review. Above this level, default probability jumps to 72%.
3. **Price prior-default borrowers differently** — they carry 2× the risk and should either be declined or offered shorter terms with stricter collateral.
4. **Develop a rental assistance product** — renters are 4× riskier than owners, but this may reflect lack of assets rather than irresponsibility. A secured or co-signed product could serve this segment safely.
5. **Use the risk scoring model as a triage tool** — not a final decision, but a fast filter to prioritise manual review on borderline applications.

---

## Repository Structure

```
nova-bank-credit-risk/
├── nova_bank_analysis.py          # Full Python analysis (9 sections)
├── nova_bank_powerbi_dashboard.html  # Interactive dashboard (Chart.js)
├── nova_bank_report_generator.js  # Automated Word report builder (docx.js)
├── credit_risk_enriched.csv       # Enriched dataset with risk scores
├── Credit_Risk_Dataset.xlsx       # Original dataset (32,581 rows, 29 cols)
└── README.md
```

---

## How to Run

```bash
# Install dependencies
pip install pandas numpy openpyxl

# Run full analysis (prints to console)
python nova_bank_analysis.py

# View dashboard — open in any browser
open nova_bank_powerbi_dashboard.html

# Generate Word report
npm install docx
node nova_bank_report_generator.js
```

---

## Dataset

32,581 personal loan records across the US, UK, and Canada with 29 features including borrower demographics, employment, credit history, loan characteristics, and repayment outcome (`loan_status`: 0 = repaid, 1 = defaulted).

Overall default rate: **21.8%** (7,108 defaults)

---

*Project completed as part of the Nova Bank Credit Risk Challenge. All data is synthetic/anonymised.*
