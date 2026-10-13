import sqlite3
import pandas as pd

conn = sqlite3.connect("healthcare_claims.db")

print("\n" + "=" * 70)
print("HEALTHCARE CLAIMS SQL ANALYSIS")
print("=" * 70)


# ============================================================
# 1. ENCOUNTERS BY TYPE
# ============================================================

query1 = """
SELECT
    encounter_type,
    COUNT(*) AS encounter_count,
    ROUND(AVG(total_charge), 2) AS average_charge
FROM encounters
GROUP BY encounter_type
ORDER BY encounter_count DESC;
"""

print("\n1. ENCOUNTERS BY TYPE")
print("-" * 70)
print(pd.read_sql_query(query1, conn).to_string(index=False))


# ============================================================
# 2. MONTHLY ENCOUNTER VOLUME
# ============================================================

query2 = """
SELECT
    strftime('%Y-%m', encounter_date) AS encounter_month,
    COUNT(*) AS encounter_count
FROM encounters
GROUP BY encounter_month
ORDER BY encounter_month;
"""

print("\n2. MONTHLY ENCOUNTER VOLUME")
print("-" * 70)
print(pd.read_sql_query(query2, conn).to_string(index=False))


# ============================================================
# 3. COST BY ENCOUNTER TYPE
# ============================================================

query3 = """
SELECT
    encounter_type,
    COUNT(*) AS encounter_count,
    ROUND(SUM(total_charge), 2) AS total_charges,
    ROUND(AVG(total_charge), 2) AS average_charge
FROM encounters
GROUP BY encounter_type
ORDER BY total_charges DESC;
"""

print("\n3. COST BY ENCOUNTER TYPE")
print("-" * 70)
print(pd.read_sql_query(query3, conn).to_string(index=False))


# ============================================================
# 4. TOP 10 DIAGNOSES BY UTILIZATION
# ============================================================

query4 = """
SELECT
    e.diagnosis_code,
    d.diagnosis_name,
    COUNT(*) AS encounter_count
FROM encounters e
JOIN diagnoses d
    ON e.diagnosis_code = d.diagnosis_code
GROUP BY
    e.diagnosis_code,
    d.diagnosis_name
ORDER BY encounter_count DESC
LIMIT 10;
"""

print("\n4. TOP 10 DIAGNOSES BY UTILIZATION")
print("-" * 70)
print(pd.read_sql_query(query4, conn).to_string(index=False))


# ============================================================
# 5. CLAIM STATUS ANALYSIS
# ============================================================

query5 = """
SELECT
    claim_status,
    COUNT(*) AS claim_count,
    ROUND(
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims),
        2
    ) AS percentage,
    ROUND(SUM(billed_amount), 2) AS total_billed,
    ROUND(SUM(paid_amount), 2) AS total_paid
FROM claims
GROUP BY claim_status
ORDER BY claim_count DESC;
"""

print("\n5. CLAIM STATUS ANALYSIS")
print("-" * 70)
print(pd.read_sql_query(query5, conn).to_string(index=False))


# ============================================================
# 6. TOP 10 PROVIDERS
# ============================================================

query6 = """
SELECT
    p.provider_id,
    p.provider_name,
    p.specialty,
    COUNT(e.encounter_id) AS encounter_count,
    COUNT(DISTINCT e.patient_id) AS unique_patients,
    ROUND(SUM(e.total_charge), 2) AS total_charges
FROM providers p
LEFT JOIN encounters e
    ON p.provider_id = e.provider_id
GROUP BY
    p.provider_id,
    p.provider_name,
    p.specialty
ORDER BY encounter_count DESC
LIMIT 10;
"""

print("\n6. TOP 10 PROVIDERS BY UTILIZATION")
print("-" * 70)
print(pd.read_sql_query(query6, conn).to_string(index=False))


# ============================================================
# 7. INPATIENT LENGTH OF STAY
# ============================================================

query7 = """
SELECT
    COUNT(*) AS inpatient_encounters,
    ROUND(AVG(length_of_stay), 2) AS average_los,
    MIN(length_of_stay) AS minimum_los,
    MAX(length_of_stay) AS maximum_los
FROM encounters
WHERE encounter_type = 'Inpatient';
"""

print("\n7. INPATIENT LENGTH OF STAY")
print("-" * 70)
print(pd.read_sql_query(query7, conn).to_string(index=False))


# ============================================================
# 8. HIGH-UTILIZATION PATIENTS
# ============================================================

query8 = """
SELECT
    patient_id,
    COUNT(*) AS encounter_count,
    ROUND(SUM(total_charge), 2) AS total_cost
FROM encounters
GROUP BY patient_id
HAVING COUNT(*) >= 10
ORDER BY encounter_count DESC;
"""

print("\n8. HIGH-UTILIZATION PATIENTS")
print("-" * 70)

high_utilization = pd.read_sql_query(query8, conn)

print(high_utilization.head(20).to_string(index=False))

print("\nTotal high-utilization patients:",
      len(high_utilization))


# ============================================================
# 9. HIGH-COST PATIENTS
# ============================================================

query9 = """
SELECT
    patient_id,
    COUNT(*) AS encounter_count,
    ROUND(SUM(total_charge), 2) AS total_cost
FROM encounters
GROUP BY patient_id
HAVING SUM(total_charge) >= 75000
ORDER BY total_cost DESC;
"""

print("\n9. HIGH-COST PATIENTS")
print("-" * 70)

high_cost = pd.read_sql_query(query9, conn)

print(high_cost.head(20).to_string(index=False))

print("\nTotal high-cost patients:",
      len(high_cost))


# ============================================================
# 10. DATA QUALITY - ORPHAN CLAIMS
# ============================================================

query10 = """
SELECT
    COUNT(*) AS orphan_claims
FROM claims c
LEFT JOIN encounters e
    ON c.encounter_id = e.encounter_id
WHERE e.encounter_id IS NULL;
"""

print("\n10. DATA QUALITY - ORPHAN CLAIMS")
print("-" * 70)
print(pd.read_sql_query(query10, conn).to_string(index=False))


# ============================================================
# 11. DATA QUALITY - INVALID DIAGNOSIS CODES
# ============================================================

query11 = """
SELECT
    COUNT(*) AS invalid_diagnosis_codes
FROM encounters e
LEFT JOIN diagnoses d
    ON e.diagnosis_code = d.diagnosis_code
WHERE d.diagnosis_code IS NULL;
"""

print("\n11. DATA QUALITY - INVALID DIAGNOSIS CODES")
print("-" * 70)
print(pd.read_sql_query(query11, conn).to_string(index=False))


# ============================================================
# CLOSE DATABASE
# ============================================================

conn.close()

print("\n" + "=" * 70)
print("SQL ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 70)