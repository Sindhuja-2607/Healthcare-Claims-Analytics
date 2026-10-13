
# Healthcare Claims Analytics

## Project Overview

Healthcare Claims Analytics is an end-to-end data analytics project that examines healthcare encounter volume, medical charges, claim status, patient utilization, diagnoses, readmissions, and provider and facility activity.

The project uses SQLite and SQL for data analysis, Python and Pandas to execute queries and review results, and Power BI to develop an interactive dashboard.

## Business Problem

Healthcare organizations need reliable reporting to understand healthcare utilization, identify major cost drivers, monitor claim outcomes, and investigate high-utilization and high-cost patient populations.

This project analyzes healthcare data to answer questions such as:

- Which encounter types have the highest volume and charges?
- What proportion of claims are paid, pending, or denied?
- Which diagnoses account for the most encounters?
- Which patients have high utilization or high total charges?
- What is the average inpatient length of stay?
- How do encounter volumes vary across providers and facilities?
- Do claims and diagnosis records pass basic data-quality checks?

## Tools and Technologies

- SQL
- SQLite
- Python
- Pandas
- Microsoft Power BI
- Data Analysis and Visualization

## Project Workflow

1. Stored the project dataset in a local SQLite database.
2. Wrote SQL queries to analyze encounters, costs, diagnoses, claims, providers, and patient utilization.
3. Used Python and Pandas to execute SQL queries and review results.
4. Built a Power BI dashboard to visualize key metrics and analytical findings.
5. Developed business insights and recommendations based on the analysis results.

## Key Metrics

| Metric | Result |
|---|---:|
| Total Patients | 998 |
| Total Encounters | 6,000 |
| Total Charges | $29.26 million |
| High-Utilization Patients | 74 |
| High-Cost Patients | 23 |
| Inpatient Encounters | 861 |
| Average Inpatient Length of Stay | 5.5 days |
| Orphan Claims Found | 0 |
| Invalid Diagnosis Codes Found | 0 |

## Key Findings

### 1. Inpatient Care Is the Largest Cost Driver

Inpatient encounters accounted for 861 of the 6,000 encounters, approximately 14.35% of encounter volume. However, they generated approximately $16.29 million in charges, representing about 55.7% of total charges.

The average inpatient charge was $18,925.14.

**Business implication:** Inpatient services are an important focus for further cost, utilization, and length-of-stay analysis.

### 2. Outpatient Care Has the Highest Encounter Volume

Outpatient care accounted for 2,991 encounters, approximately 49.85% of all encounters. Emergency care accounted for 1,206 encounters, telehealth for 942, and inpatient care for 861.

**Business implication:** Outpatient care drives encounter volume, while inpatient care has a much greater average charge per encounter.

### 3. Most Claims Were Paid

The SQL results showed:

- Paid: 5,134 claims (85.57%)
- Pending: 568 claims (9.47%)
- Denied: 298 claims (4.97%)

**Business implication:** Pending and denied claims warrant further review to identify potential follow-up and revenue-cycle improvement opportunities.

### 4. High-Utilization Patients Were Identified

The analysis identified 74 patients with 10 or more encounters.

**Business implication:** This group may warrant further investigation of recurring conditions, care coordination needs, and encounter patterns.

### 5. High-Cost Patients Were Identified

The analysis identified 23 patients with total charges of at least $75,000. The highest total charge among the displayed results was $98,269.23.

**Business implication:** Reviewing diagnoses, encounter types, and inpatient utilization for high-cost patients can help explain the factors associated with greater spending.

### 6. Inpatient Length of Stay Was Analyzed

The dataset contained 861 inpatient encounters. The average length of stay was 5.5 days, with a minimum of 1 day and a maximum of 10 days.

**Business implication:** Length-of-stay analysis can support further investigation of inpatient resource utilization and associated charges.

### 7. Basic Data-Quality Checks Passed

The SQL checks returned zero orphan claims and zero invalid diagnosis-code references for the tested relationships.

**Business implication:** These checks did not identify the specific relationship-integrity issues tested. Additional validation would be required to assess overall data quality.

## SQL Analysis

The Python SQL analysis script includes these 11 analyses:

1. Encounters by Type
2. Monthly Encounter Volume
3. Cost by Encounter Type
4. Top 10 Diagnoses by Utilization
5. Claim Status Analysis
6. Top 10 Providers by Utilization
7. Inpatient Length of Stay
8. High-Utilization Patients
9. High-Cost Patients
10. Orphan Claims Validation
11. Invalid Diagnosis-Code Validation

## Power BI Dashboard

The dashboard presents the following metrics and analyses:

- Total Patients
- Total Encounters
- Total Charges
- Visits by Encounter Type
- Total Charges by Encounter Type
- High-Utilization Patients
- High-Cost Patients
- Total Charges by Diagnosis
- Claim Status Distribution
- Length of Stay Distribution
- Readmissions by Diagnosis
- Inpatient Readmission Analysis
- Provider Utilization
- Facility Utilization
- Patient Utilization — Top 10 Patients

## Recommendations

- Investigate inpatient cost drivers and length-of-stay patterns.
- Review high-utilization patients to understand recurring encounter patterns.
- Analyze pending and denied claims to identify possible process-improvement opportunities.
- Monitor provider and facility encounter volumes to understand workload distribution.
- Continue validating claims relationships, diagnosis references, and report totals.
- Compare SQL outputs against dashboard metrics to maintain consistency.

## Project Files

- `Sql/run_sql.py` — Python script that executes the SQL analyses.
- `Sql/healthcare_analysis.sql` — SQL analysis queries.
- `healthcare_project.py` — Main Python project script.
- Power BI dashboard file and dashboard screenshot will be added to the repository.

## Important Note

The SQLite database is maintained locally and excluded from Git tracking by the root `.gitignore`. Do not publish patient-level or otherwise sensitive data. Only share data that is appropriate for public distribution.

## Author

Sindhuja Nimballi

Healthcare Data Analytics | SQL | Python | Power BI
