-- ============================================================
-- HEALTHCARE CLAIMS ANALYTICS - SQL ANALYSIS
-- ============================================================


-- 1. TOTAL PATIENTS
SELECT COUNT(*) AS total_patients
FROM patients;


-- 2. TOTAL ENCOUNTERS
SELECT COUNT(*) AS total_encounters
FROM encounters;


-- 3. TOTAL CLAIMS
SELECT COUNT(*) AS total_claims
FROM claims;


-- 4. ENCOUNTERS BY TYPE
SELECT
    encounter_type,
    COUNT(*) AS encounter_count,
    ROUND(
        COUNT(*) * 100.0 / (SELECT COUNT(*) FROM encounters),
        2
    ) AS percentage
FROM encounters
GROUP BY encounter_type
ORDER BY encounter_count DESC;


-- 5. MONTHLY ENCOUNTER VOLUME
SELECT
    strftime('%Y-%m', encounter_date) AS encounter_month,
    COUNT(*) AS encounter_count
FROM encounters
GROUP BY encounter_month
ORDER BY encounter_month;


-- 6. COST BY ENCOUNTER TYPE
SELECT
    encounter_type,
    COUNT(*) AS encounter_count,
    ROUND(SUM(total_charge), 2) AS total_charges,
    ROUND(AVG(total_charge), 2) AS average_charge
FROM encounters
GROUP BY encounter_type
ORDER BY total_charges DESC;


-- 7. TOP 10 DIAGNOSES BY ENCOUNTER COUNT
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


-- 8. CLAIM STATUS ANALYSIS
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


-- 9. PROVIDER UTILIZATION
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


-- 10. INPATIENT LENGTH OF STAY
SELECT
    ROUND(AVG(length_of_stay), 2) AS average_los,
    MIN(length_of_stay) AS minimum_los,
    MAX(length_of_stay) AS maximum_los
FROM encounters
WHERE encounter_type = 'Inpatient';


-- 11. HIGH-UTILIZATION PATIENTS
SELECT
    patient_id,
    COUNT(*) AS encounter_count
FROM encounters
GROUP BY patient_id
HAVING COUNT(*) >= 10
ORDER BY encounter_count DESC;


-- 12. HIGH-COST PATIENTS
SELECT
    patient_id,
    COUNT(*) AS encounter_count,
    ROUND(SUM(total_charge), 2) AS total_cost
FROM encounters
GROUP BY patient_id
HAVING SUM(total_charge) >= 75000
ORDER BY total_cost DESC;


-- 13. DATA QUALITY - ORPHAN CLAIMS
SELECT
    COUNT(*) AS orphan_claims
FROM claims c
LEFT JOIN encounters e
    ON c.encounter_id = e.encounter_id
WHERE e.encounter_id IS NULL;


-- 14. DATA QUALITY - INVALID DIAGNOSIS CODES
SELECT
    COUNT(*) AS invalid_diagnosis_codes
FROM encounters e
LEFT JOIN diagnoses d
    ON e.diagnosis_code = d.diagnosis_code
WHERE d.diagnosis_code IS NULL;


-- 15. PATIENT UTILIZATION SUMMARY
SELECT
    p.patient_id,
    p.age,
    p.gender,
    p.insurance_type,
    p.chronic_condition,
    COUNT(e.encounter_id) AS total_encounters,
    SUM(
        CASE
            WHEN e.encounter_type = 'Emergency'
            THEN 1 ELSE 0
        END
    ) AS emergency_visits,
    SUM(
        CASE
            WHEN e.encounter_type = 'Inpatient'
            THEN 1 ELSE 0
        END
    ) AS inpatient_visits,
    SUM(
        CASE
            WHEN e.encounter_type = 'Telehealth'
            THEN 1 ELSE 0
        END
    ) AS telehealth_visits,
    ROUND(SUM(e.total_charge), 2) AS total_cost
FROM patients p
LEFT JOIN encounters e
    ON p.patient_id = e.patient_id
GROUP BY
    p.patient_id,
    p.age,
    p.gender,
    p.insurance_type,
    p.chronic_condition
ORDER BY total_encounters DESC;