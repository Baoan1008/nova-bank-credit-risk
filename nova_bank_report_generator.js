const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, AlignmentType, BorderStyle, WidthType, ShadingType,
  LevelFormat, PageNumber, Footer, Header
} = require('docx');
const fs = require('fs');

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const hBorder = { style: BorderStyle.SINGLE, size: 1, color: "1F4E79" };
const hBorders = { top: hBorder, bottom: hBorder, left: hBorder, right: hBorder };

const cm = (n) => n; // pass-through since we're just using cell margin
const cellMargins = { top: 100, bottom: 100, left: 140, right: 140 };

function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    children: [new TextRun({ text, bold: true, size: 32, font: "Arial", color: "1F4E79" })],
    spacing: { before: 360, after: 160 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "1F4E79", space: 1 } }
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    children: [new TextRun({ text, bold: true, size: 26, font: "Arial", color: "2E75B6" })],
    spacing: { before: 240, after: 120 }
  });
}

function body(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun({ text, size: 22, font: "Arial", ...opts })],
    spacing: { before: 60, after: 60 },
    alignment: AlignmentType.JUSTIFIED
  });
}

function bullet(text) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    children: [new TextRun({ text, size: 22, font: "Arial" })],
    spacing: { before: 40, after: 40 }
  });
}

function spacer() {
  return new Paragraph({ children: [new TextRun("")], spacing: { before: 80, after: 80 } });
}

function makeTable(headers, rows, colWidths) {
  const totalW = colWidths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: totalW, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [
      new TableRow({
        tableHeader: true,
        children: headers.map((h, i) => new TableCell({
          borders: hBorders,
          width: { size: colWidths[i], type: WidthType.DXA },
          shading: { fill: "1F4E79", type: ShadingType.CLEAR },
          margins: cellMargins,
          children: [new Paragraph({ children: [new TextRun({ text: h, bold: true, size: 20, font: "Arial", color: "FFFFFF" })], alignment: AlignmentType.CENTER })]
        }))
      }),
      ...rows.map((row, ri) => new TableRow({
        children: row.map((cell, ci) => new TableCell({
          borders,
          width: { size: colWidths[ci], type: WidthType.DXA },
          shading: { fill: ri % 2 === 0 ? "EBF3FB" : "FFFFFF", type: ShadingType.CLEAR },
          margins: cellMargins,
          children: [new Paragraph({ children: [new TextRun({ text: String(cell), size: 20, font: "Arial" })], alignment: ci === 0 ? AlignmentType.LEFT : AlignmentType.CENTER })]
        }))
      }))
    ]
  });
}

const doc = new Document({
  numbering: {
    config: [{
      reference: "bullets",
      levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } }]
    }]
  },
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } }
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1080, bottom: 1440, left: 1080 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          children: [new TextRun({ text: "NOVA BANK  |  Credit Risk Analysis Report  |  Confidential", size: 18, font: "Arial", color: "666666" })],
          alignment: AlignmentType.RIGHT,
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC", space: 1 } }
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          children: [
            new TextRun({ text: "Nova Bank Credit Risk Analysis  |  March 2026  |  Page ", size: 18, font: "Arial", color: "888888" }),
            new TextRun({ children: [PageNumber.CURRENT], size: 18, font: "Arial", color: "888888" })
          ],
          alignment: AlignmentType.CENTER,
          border: { top: { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC", space: 1 } }
        })]
      })
    },
    children: [
      // COVER
      spacer(), spacer(),
      new Paragraph({
        children: [new TextRun({ text: "NOVA BANK", size: 64, bold: true, font: "Arial", color: "1F4E79" })],
        alignment: AlignmentType.CENTER, spacing: { before: 480, after: 80 }
      }),
      new Paragraph({
        children: [new TextRun({ text: "Credit Risk Analysis Report", size: 40, font: "Arial", color: "2E75B6" })],
        alignment: AlignmentType.CENTER, spacing: { before: 80, after: 80 }
      }),
      new Paragraph({
        children: [new TextRun({ text: "USA \u2022 United Kingdom \u2022 Canada", size: 24, font: "Arial", color: "666666" })],
        alignment: AlignmentType.CENTER, spacing: { before: 80, after: 80 }
      }),
      new Paragraph({
        children: [new TextRun({ text: "March 2026  |  32,581 Borrowers", size: 22, font: "Arial", color: "888888" })],
        alignment: AlignmentType.CENTER, spacing: { before: 80, after: 480 }
      }),
      spacer(), spacer(), spacer(),

      // EXECUTIVE SUMMARY
      heading1("1. Executive Summary"),
      body("This report presents a comprehensive analysis of credit risk across Nova Bank's loan portfolio of 32,581 borrowers in the United States, United Kingdom, and Canada. The analysis examines default patterns, key risk drivers, borrower profiles, and actionable recommendations to help Nova Bank balance responsible lending with business growth."),
      spacer(),
      body("Key findings at a glance:", { bold: true }),
      bullet("Overall default rate: 21.8% (7,108 borrowers out of 32,581)"),
      bullet("Loan grade is the most powerful single predictor — Grade G loans default at 98.4%"),
      bullet("Loan-to-income ratio is the top quantitative risk indicator (correlation: 0.386)"),
      bullet("Home ownership creates a 4x difference in default rates (7.5% own vs. 31.6% rent)"),
      bullet("Prior default on file doubles risk (37.8% vs. 18.4%)"),
      bullet("No meaningful geographic difference across the three countries (~21.9% each)"),
      bullet("Demographics (gender, education, marital status) have virtually no predictive power"),
      spacer(),

      // PORTFOLIO OVERVIEW
      heading1("2. Portfolio Overview"),
      body("Nova Bank's portfolio covers 32,581 borrowers across three countries with nearly equal representation. The loan purposes span personal, medical, education, debt consolidation, home improvement, and venture/business use cases. Loan grades range from A (lowest risk) through G (highest risk)."),
      spacer(),
      makeTable(
        ["Metric", "Value"],
        [
          ["Total borrowers", "32,581"],
          ["Overall default rate", "21.8%"],
          ["Borrowers in USA", "10,852 (33.3%)"],
          ["Borrowers in UK", "10,944 (33.6%)"],
          ["Borrowers in Canada", "10,785 (33.1%)"],
          ["Average income (non-default)", "$70,804"],
          ["Average income (default)", "$49,126"],
          ["Average loan-to-income ratio (non-default)", "0.149"],
          ["Average loan-to-income ratio (default)", "0.249"],
          ["Average interest rate (non-default)", "10.44%"],
          ["Average interest rate (default)", "13.06%"],
        ],
        [5200, 4160]
      ),
      spacer(),

      // KEY RISK FACTORS
      heading1("3. Key Risk Factors"),
      heading2("3.1 Loan Grade"),
      body("Loan grade is the most decisive predictor of default in the portfolio, showing near-deterministic outcomes at the extremes. Grade A borrowers default at just 10.0%, while Grade G borrowers default at 98.4% — essentially a guaranteed loss. Grades D through G collectively represent catastrophic risk and should trigger mandatory additional underwriting controls."),
      spacer(),
      makeTable(
        ["Grade", "Total Loans", "Defaults", "Default Rate", "Risk Level"],
        [
          ["A", "10,777", "1,073", "10.0%", "Very Low"],
          ["B", "10,451", "1,701", "16.3%", "Low"],
          ["C", "6,458", "1,339", "20.7%", "Moderate"],
          ["D", "3,626", "2,141", "59.0%", "High"],
          ["E", "964", "621", "64.4%", "Very High"],
          ["F", "241", "170", "70.5%", "Critical"],
          ["G", "64", "63", "98.4%", "Critical"],
        ],
        [1560, 1872, 1872, 2184, 1872]
      ),
      spacer(),
      heading2("3.2 Loan-to-Income and Debt Ratios"),
      body("Financial leverage ratios are the strongest quantitative predictors of default. The loan-to-income ratio (correlation 0.386) and loan as a percentage of income (correlation 0.379) are the top two factors. Borrowers who default carry an average loan-to-income ratio of 0.249, compared to 0.149 for repayers — a 67% difference. Debt-to-income ratio shows a similarly strong signal (correlation 0.322)."),
      spacer(),
      makeTable(
        ["Factor", "Non-Default (Mean)", "Default (Mean)", "Correlation with Default"],
        [
          ["Loan-to-income ratio", "0.149", "0.249", "0.386"],
          ["Loan as % of income", "14.9%", "24.9%", "0.379"],
          ["Interest rate", "10.44%", "13.06%", "0.335"],
          ["Debt-to-income ratio", "lower", "higher", "0.322"],
          ["Annual income", "$70,804", "$49,126", "-0.144"],
          ["Loan amount", "$9,237", "$10,851", "0.105"],
        ],
        [3400, 1900, 1900, 2160]
      ),
      spacer(),
      heading2("3.3 Home Ownership"),
      body("Home ownership status is the strongest demographic risk differentiator. Outright homeowners default at just 7.5%, while renters default at 31.6% — a 4x gap. Mortgage holders also perform well at 12.6%, suggesting that financial commitment to property correlates strongly with loan repayment discipline."),
      spacer(),
      makeTable(
        ["Ownership Status", "Default Rate", "Relative Risk"],
        [
          ["Own outright", "7.5%", "Baseline"],
          ["Mortgage", "12.6%", "1.7x"],
          ["Rent", "31.6%", "4.2x"],
          ["Other", "30.8%", "4.1x"],
        ],
        [3500, 2400, 3460]
      ),
      spacer(),
      heading2("3.4 Loan Purpose"),
      body("Loan purpose provides a meaningful secondary signal. Debt consolidation loans carry the highest default rate at 28.6%, followed by medical (26.7%) and home improvement (26.1%). These higher-risk categories often indicate borrowers who are already under financial stress before taking out the loan. Venture and business loans are the safest at 14.8%, possibly because borrowers have clearer repayment plans."),
      spacer(),
      makeTable(
        ["Loan Purpose", "Default Rate", "Relative Risk"],
        [
          ["Venture / Business", "14.8%", "Lowest"],
          ["Education", "17.2%", "Low"],
          ["Personal", "19.9%", "Moderate"],
          ["Home improvement", "26.1%", "Elevated"],
          ["Medical", "26.7%", "Elevated"],
          ["Debt consolidation", "28.6%", "Highest"],
        ],
        [3500, 2400, 3460]
      ),
      spacer(),
      heading2("3.5 Prior Default History"),
      body("Borrowers with a prior default on file (field: cb_person_default_on_file = Y) default at 37.8%, more than double the 18.4% rate for borrowers with a clean record. This binary flag should carry significant weight in any scoring model or approval workflow."),
      spacer(),
      heading2("3.6 Employment Type"),
      body("Employment type has a surprisingly weak relationship with default outcomes. The difference between full-time employed (21.6%) and unemployed (22.7%) borrowers is only 1.1 percentage points. This suggests that income level and debt structure matter far more than employment status alone. Nova Bank should avoid over-relying on employment type as a gatekeeping criterion, as doing so could unfairly exclude contractors and self-employed individuals with strong finances."),
      spacer(),

      // DEMOGRAPHIC ANALYSIS
      heading1("4. Demographic Analysis"),
      body("A key finding of this analysis is that standard demographic variables provide almost no predictive power for default. This has important implications for fair lending policy."),
      spacer(),
      makeTable(
        ["Demographic Factor", "Variation in Default Rate", "Conclusion"],
        [
          ["Gender (Male vs Female)", "21.8% vs 21.9%", "No predictive power"],
          ["Marital status (range)", "21.4% - 22.0%", "No predictive power"],
          ["Education (range)", "21.2% - 22.2%", "No predictive power"],
          ["Age (range)", "20.7% - 23.9%", "Minimal — young/old slightly higher"],
          ["Country (USA/UK/Canada)", "21.7% - 21.9%", "No meaningful difference"],
        ],
        [3200, 2400, 3760]
      ),
      spacer(),
      body("The near-identical default rates across gender, education level, and marital status strongly suggest that Nova Bank should not use these factors as lending criteria. Doing so would create unjustified barriers for certain groups without improving credit quality. Age shows a minor U-shaped pattern (slightly higher defaults in the youngest 18-25 and oldest 55+ groups), which may reflect income volatility rather than age itself."),
      spacer(),

      // GEOGRAPHIC ANALYSIS
      heading1("5. Geographic Analysis"),
      body("The three countries in Nova Bank's portfolio show virtually identical default rates: USA at 21.9%, UK at 21.7%, and Canada at 21.9%. This uniformity allows Nova Bank to apply a single global credit policy framework rather than country-specific approaches."),
      spacer(),
      body("At the city level, a narrow spread of ~4 percentage points exists across the 18 cities analysed. Vancouver leads at 24.2%, while Swansea and Quebec City are the safest at around 20.4-20.5%. These differences are modest and unlikely to justify city-specific underwriting policies. However, they could inform regional marketing or outreach strategies."),
      spacer(),
      makeTable(
        ["City", "Country", "Borrowers", "Default Rate"],
        [
          ["Vancouver", "Canada", "1,827", "24.2%"],
          ["Dallas", "USA", "1,797", "23.6%"],
          ["Edinburgh", "UK", "1,807", "23.5%"],
          ["Los Angeles", "USA", "1,838", "22.9%"],
          ["Manchester", "UK", "1,803", "22.5%"],
          ["Toronto", "Canada", "1,751", "21.9%"],
          ["London", "UK", "1,851", "21.1%"],
          ["Houston", "USA", "1,811", "20.9%"],
          ["Victoria", "Canada", "1,852", "20.8%"],
          ["Swansea", "UK", "1,811", "20.4%"],
        ],
        [2600, 1800, 1800, 3160]
      ),
      spacer(),

      // RISK SCORING MODEL
      heading1("6. Risk Scoring Model"),
      body("Based on the analysis, a simple additive risk scoring model has been developed. Scores range from 0 (highest risk) to 100 (lowest risk). The model is calibrated to the observed data and validated against actual default rates by decile."),
      spacer(),
      makeTable(
        ["Factor", "Scoring Logic", "Max Impact"],
        [
          ["Loan grade", "A: 0 pts, B: -5, C: -15, D: -40, E: -55, F: -65, G: -80", "-80 pts"],
          ["Loan-to-income ratio", "<0.15: 0, 0.15-0.25: -8, 0.25-0.35: -16, >0.35: -25", "-25 pts"],
          ["Prior default on file", "Yes: -20 pts, No: 0", "-20 pts"],
          ["Home ownership", "Own: +10, Mortgage: +5, Rent: 0, Other: -2", "+10 pts"],
          ["Annual income", ">$80K: +5, >$50K: +2, <$30K: -8", "+5 pts"],
          ["Interest rate", ">18%: -10, >14%: -5, else: 0", "-10 pts"],
        ],
        [2200, 4760, 2400]
      ),
      spacer(),
      body("Model validation — default rate by risk tier:", { bold: true }),
      spacer(),
      makeTable(
        ["Risk Tier", "Score Range", "Borrower Count", "Actual Default Rate"],
        [
          ["Very Low Risk", "81-100", "20,638", "7.4%"],
          ["Low Risk", "61-80", "5,837", "35.8%"],
          ["Medium Risk", "41-60", "2,956", "42.4%"],
          ["High Risk", "0-40", "2,979", "69.7%"],
        ],
        [2800, 1800, 2400, 2360]
      ),
      spacer(),
      body("The model effectively separates the portfolio: Very Low Risk borrowers (63% of the book) default at just 7.4%, while High Risk borrowers (9% of the book) default at nearly 70%. A score cutoff at 60 would eliminate the two highest-risk tiers while retaining 63% of the portfolio."),
      spacer(),

      // RECOMMENDATIONS
      heading1("7. Policy Recommendations"),
      heading2("7.1 Loan Grade Controls"),
      bullet("Implement mandatory co-signer or collateral requirements for all Grade D loans and above."),
      bullet("Consider declining Grade F and G loans outright, or pricing them with substantially higher rates to reflect actual risk (70-98% default rates make most pricing models unviable)."),
      bullet("Use Grade C as the threshold for enhanced underwriting review."),
      spacer(),
      heading2("7.2 Loan-to-Income Cap"),
      bullet("Introduce a hard cap: new loans should not exceed 25% of a borrower's annual income as a standalone policy."),
      bullet("For borrowers with loan-to-income ratios above 0.20, require additional income verification and debt documentation before approval."),
      spacer(),
      heading2("7.3 Prior Default Flag"),
      bullet("Weight prior default history heavily in automated scoring — a borrower with a default on file should require a compensating factor (strong income, excellent loan grade, full home ownership) to be approved."),
      bullet("Consider a mandatory manual review for any borrower with cb_person_default_on_file = Y and a loan-to-income ratio above 0.20."),
      spacer(),
      heading2("7.4 Debt Consolidation Loans"),
      bullet("Treat debt consolidation loans as a higher-risk category requiring additional documentation of the debts being consolidated."),
      bullet("Require a post-consolidation debt-to-income ratio below a defined threshold (e.g., 40%) before approval."),
      spacer(),
      heading2("7.5 Fair Lending Practices"),
      bullet("Do not use gender, education level, or marital status in lending decisions — the data shows these have no predictive power and using them would constitute unjustified discrimination."),
      bullet("Be cautious about using employment type as a strong signal — the data shows a minimal 1.1pp difference between full-time and unemployed borrowers. Income verification is more meaningful."),
      bullet("Age shows only a minor signal and should not be used as a primary factor."),
      spacer(),
      heading2("7.6 Geographic Policy"),
      bullet("Maintain a single global credit policy framework across USA, UK, and Canada — the near-identical default rates (all ~21.9%) do not justify country-specific scoring."),
      bullet("City-level differences are too small to justify geographic underwriting differences, but could inform targeted financial education or outreach programs in higher-risk cities such as Vancouver and Dallas."),
      spacer(),

      // APPENDIX
      heading1("8. Appendix: Data Summary"),
      body("Dataset: Credit_Risk_Dataset.xlsx | 32,581 rows | 29 columns"),
      body("Analysis date: March 2026"),
      body("Key columns used: loan_status (target), loan_grade, loan_to_income_ratio, loan_percent_income, loan_int_rate, debt_to_income_ratio, person_income, person_home_ownership, loan_intent, cb_person_default_on_file, employment_type, country, city, person_age, gender, education_level, marital_status"),
      spacer(),
      body("Correlation with loan_status (default = 1):", { bold: true }),
      makeTable(
        ["Variable", "Correlation"],
        [
          ["loan_to_income_ratio", "0.386"],
          ["loan_percent_income", "0.379"],
          ["loan_int_rate", "0.335"],
          ["debt_to_income_ratio", "0.322"],
          ["loan_amnt", "0.105"],
          ["person_income", "-0.144"],
          ["other_debt", "-0.118"],
          ["person_emp_length", "-0.082"],
          ["person_age", "-0.022"],
          ["past_delinquencies", "0.000"],
        ],
        [6240, 3120]
      ),
    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync('/home/claude/Nova_Bank_Credit_Risk_Report.docx', buf);
  console.log('Done');
});
