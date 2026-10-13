import pandas as pd
import numpy as np

# --------------------------------------------------
# HEALTHCARE CLAIMS ANALYTICS PROJECT
# --------------------------------------------------

np.random.seed(42)

# --------------------------------------------------
# 1. PATIENTS
# --------------------------------------------------

num_patients = 1000

patients = pd.DataFrame({
    "patient_id": [f"P{10000 + i}" for i in range(1, num_patients + 1)],
    "age": np.random.randint(18, 86, num_patients),
    "gender": np.random.choice(
        ["Female", "Male"],
        num_patients,
        p=[0.55, 0.45]
    ),
    "state": np.random.choice(
        ["NJ", "NY", "PA", "CT", "MA"],
        num_patients
    ),
    "insurance_type": np.random.choice(
        ["Commercial", "Medicare", "Medicaid"],
        num_patients,
        p=[0.55, 0.25, 0.20]
    ),
    "chronic_condition": np.random.choice(
        ["Diabetes", "Hypertension", "Asthma", "None"],
        num_patients,
        p=[0.20, 0.25, 0.15, 0.40]
    )
})

# --------------------------------------------------
# 2. PROVIDERS
# --------------------------------------------------

num_providers = 50

providers = pd.DataFrame({
    "provider_id": [
        f"PR{1000 + i}" for i in range(1, num_providers + 1)
    ],
    "provider_name": [
        f"Provider {i}" for i in range(1, num_providers + 1)
    ],
    "specialty": np.random.choice(
        [
            "Primary Care",
            "Cardiology",
            "Endocrinology",
            "Orthopedics",
            "Emergency Medicine",
            "Pediatrics",
            "Internal Medicine"
        ],
        num_providers
    ),
    "facility_id": np.random.choice(
        [f"F{100 + i}" for i in range(1, 11)],
        num_providers
    ),
    "state": np.random.choice(
        ["NJ", "NY", "PA", "CT", "MA"],
        num_providers
    )
})

# --------------------------------------------------
# 3. DIAGNOSES
# --------------------------------------------------

diagnosis_data = [
    ("E11.9", "Type 2 diabetes mellitus", "Chronic"),
    ("I10", "Essential hypertension", "Chronic"),
    ("J45.909", "Asthma", "Chronic"),
    ("M54.5", "Low back pain", "Musculoskeletal"),
    ("K21.9", "Gastro-esophageal reflux disease", "Chronic"),
    ("N39.0", "Urinary tract infection", "Acute"),
    ("J06.9", "Acute upper respiratory infection", "Acute"),
    ("R51.9", "Headache", "Symptom"),
    ("Z00.00", "Routine health examination", "Preventive"),
    ("E78.5", "Hyperlipidemia", "Chronic"),
    ("G43.909", "Migraine", "Neurological"),
    ("F41.9", "Anxiety disorder", "Behavioral Health"),
    ("F32.A", "Depression", "Behavioral Health"),
    ("M25.561", "Pain in right knee", "Musculoskeletal"),
    ("R10.9", "Abdominal pain", "Symptom"),
    ("J18.9", "Pneumonia", "Acute"),
    ("I25.10", "Coronary artery disease", "Cardiovascular"),
    ("N18.3", "Chronic kidney disease", "Chronic"),
    ("D64.9", "Anemia", "Hematology"),
    ("L03.90", "Cellulitis", "Acute")
]

diagnoses = pd.DataFrame(
    diagnosis_data,
    columns=[
        "diagnosis_code",
        "diagnosis_name",
        "category"
    ]
)

# --------------------------------------------------
# 4. ENCOUNTERS
# --------------------------------------------------

num_encounters = 6000

encounter_types = np.random.choice(
    ["Outpatient", "Emergency", "Telehealth", "Inpatient"],
    num_encounters,
    p=[0.50, 0.20, 0.15, 0.15]
)

encounter_dates = pd.to_datetime(
    np.random.choice(
        pd.date_range("2025-01-01", "2025-12-31"),
        num_encounters
    )
)

encounters = pd.DataFrame({
    "encounter_id": [
        f"E{100000 + i}" for i in range(1, num_encounters + 1)
    ],
    "patient_id": np.random.choice(
        patients["patient_id"],
        num_encounters
    ),
    "provider_id": np.random.choice(
        providers["provider_id"],
        num_encounters
    ),
    "encounter_date": encounter_dates,
    "encounter_type": encounter_types,
    "diagnosis_code": np.random.choice(
        diagnoses["diagnosis_code"],
        num_encounters
    )
})

# --------------------------------------------------
# 5. ADMISSION, DISCHARGE AND LENGTH OF STAY
# --------------------------------------------------

encounters["admission_date"] = pd.NaT
encounters["discharge_date"] = pd.NaT
encounters["length_of_stay"] = 0

inpatient_mask = encounters["encounter_type"] == "Inpatient"

inpatient_count = inpatient_mask.sum()

encounters.loc[inpatient_mask, "admission_date"] = (
    encounters.loc[inpatient_mask, "encounter_date"]
)

los_values = np.random.randint(1, 11, inpatient_count)

encounters.loc[inpatient_mask, "length_of_stay"] = los_values

encounters.loc[inpatient_mask, "discharge_date"] = (
    encounters.loc[inpatient_mask, "admission_date"]
    + pd.to_timedelta(los_values, unit="D")
)

# --------------------------------------------------
# 6. TOTAL CHARGES
# --------------------------------------------------

encounters["total_charge"] = np.where(
    encounters["encounter_type"] == "Inpatient",
    np.random.uniform(8000, 30000, num_encounters),
    np.random.uniform(100, 5000, num_encounters)
).round(2)

# --------------------------------------------------
# 7. DISPLAY BASIC RESULTS
# --------------------------------------------------

print("Patients:", len(patients))
print("Providers:", len(providers))
print("Diagnoses:", len(diagnoses))
print("Encounters:", len(encounters))

print("\nEncounter types:")
print(encounters["encounter_type"].value_counts())

print("\nProject data created successfully!")

# --------------------------------------------------
# 5. CLAIMS DATA
# --------------------------------------------------

np.random.seed(42)

num_claims = len(encounters)
procedure_codes = [
    "99213",
    "99214",
    "99285",
    "99223",
    "93000",
    "80053",
    "85025",
    "71046",
    "36415",
    "99441"
]

claim_statuses = ["Paid", "Pending", "Denied"]
claims = pd.DataFrame({
    "claim_id": [
        f"C{100000 + i}" for i in range(1, num_claims + 1)
    ],
    "patient_id": encounters["patient_id"].values,
    "encounter_id": encounters["encounter_id"].values,
    "claim_date": (
        encounters["encounter_date"].values
        + pd.to_timedelta(
            np.random.randint(1, 8, num_claims),
            unit="D"
        )
    ),
    "diagnosis_code": encounters["diagnosis_code"].values,
    "procedure_code": np.random.choice(
        procedure_codes,
        num_claims
    ),
    "billed_amount": encounters["total_charge"].values,
    "allowed_amount": 0,
    "paid_amount": 0,
    "claim_status": np.random.choice(
        claim_statuses,
        num_claims,
        p=[0.85, 0.10, 0.05]
    )
})
claims["allowed_amount"] = (
    claims["billed_amount"]
    * np.random.uniform(0.70, 0.95, num_claims)
).round(2)

claims["paid_amount"] = np.where(
    claims["claim_status"] == "Paid",
    (
        claims["allowed_amount"]
        * np.random.uniform(0.80, 1.00, num_claims)
    ).round(2),
    0
)
print("\nClaims:", len(claims))

print("\nClaim status:")
print(claims["claim_status"].value_counts())

print("\nSample claims:")
print(claims.head())

print("\nClaims data created successfully!")

# --------------------------------------------------
# 6. DATA QUALITY CHECKS
# --------------------------------------------------

print("\nDATA QUALITY CHECKS")

# Check for missing patient IDs
missing_patient_ids = claims["patient_id"].isna().sum()

print("\nMissing patient IDs:", missing_patient_ids)
# Check for duplicate claim IDs
duplicate_claim_ids = claims["claim_id"].duplicated().sum()

print("Duplicate claim IDs:", duplicate_claim_ids)
# --------------------------------------------------
# 6. DATA QUALITY CHECKS
# --------------------------------------------------

print("\nDATA QUALITY CHECKS")

# 1. Check for missing patient IDs
missing_patient_ids = claims["patient_id"].isna().sum()

print("\nMissing patient IDs:", missing_patient_ids)


# 2. Check for duplicate claim IDs
duplicate_claim_ids = claims["claim_id"].duplicated().sum()

print("Duplicate claim IDs:", duplicate_claim_ids)


# 3. Check for missing diagnosis codes
missing_diagnosis_codes = claims["diagnosis_code"].isna().sum()

print("Missing diagnosis codes:", missing_diagnosis_codes)


# 4. Check for missing encounter IDs
missing_encounter_ids = claims["encounter_id"].isna().sum()

print("Missing encounter IDs:", missing_encounter_ids)


# 5. Check for invalid billed amounts
invalid_billed_amounts = (
    claims["billed_amount"] <= 0
).sum()

print("Invalid billed amounts:", invalid_billed_amounts)


# 6. Check for invalid allowed amounts
invalid_allowed_amounts = (
    claims["allowed_amount"] <= 0
).sum()

print("Invalid allowed amounts:", invalid_allowed_amounts)


# 7. Check whether allowed amount exceeds billed amount
allowed_greater_than_billed = (
    claims["allowed_amount"] > claims["billed_amount"]
).sum()

print(
    "Allowed amount greater than billed amount:",
    allowed_greater_than_billed
)


# 8. Check whether paid amount exceeds allowed amount
paid_greater_than_allowed = (
    claims["paid_amount"] > claims["allowed_amount"]
).sum()

print(
    "Paid amount greater than allowed amount:",
    paid_greater_than_allowed
)


# 9. Check for invalid claim status values
valid_statuses = ["Paid", "Pending", "Denied"]

invalid_claim_statuses = (
    ~claims["claim_status"].isin(valid_statuses)
).sum()

print("Invalid claim statuses:", invalid_claim_statuses)


# 10. Check whether claims have matching encounters
matching_encounters = claims["encounter_id"].isin(
    encounters["encounter_id"]
).sum()

unmatched_claims = len(claims) - matching_encounters

print("Claims without matching encounters:", unmatched_claims)


# 11. Check for duplicate encounter IDs
duplicate_encounter_ids = encounters["encounter_id"].duplicated().sum()

print(
    "Duplicate encounter IDs:",
    duplicate_encounter_ids
)


# 12. Check for missing provider IDs
missing_provider_ids = encounters["provider_id"].isna().sum()

print(
    "Missing provider IDs:",
    missing_provider_ids
)


# 13. Check for invalid inpatient length of stay
invalid_los = (
    (encounters["encounter_type"] == "Inpatient")
    & (encounters["length_of_stay"] <= 0)
).sum()

print(
    "Invalid inpatient length of stay:",
    invalid_los
)


# 14. Check whether discharge date is before admission date
invalid_dates = (
    encounters["discharge_date"]
    < encounters["admission_date"]
).sum()

print(
    "Discharge date before admission date:",
    invalid_dates
)


print("\nData quality checks completed successfully!")

# --------------------------------------------------
# 7. HEALTHCARE UTILIZATION ANALYSIS
# --------------------------------------------------

print("\n" + "=" * 50)
print("HEALTHCARE UTILIZATION ANALYSIS")
print("=" * 50)

# 1. Total encounters
total_encounters = len(encounters)

print("\nTotal encounters:", total_encounters)


# 2. Unique patients who used healthcare services
unique_patients = encounters["patient_id"].nunique()

print("Unique patients:", unique_patients)


# 3. Average encounters per patient
average_encounters_per_patient = (
    total_encounters / unique_patients
)

print(
    "Average encounters per patient:",
    round(average_encounters_per_patient, 2)
)


# 4. Encounters by type
encounters_by_type = (
    encounters["encounter_type"]
    .value_counts()
    .reset_index()
)

encounters_by_type.columns = [
    "encounter_type",
    "encounter_count"
]

encounters_by_type["percentage"] = (
    encounters_by_type["encounter_count"]
    / total_encounters
    * 100
).round(2)

print("\nEncounters by type:")
print(encounters_by_type)


# 5. Monthly utilization
encounters["month"] = (
    encounters["encounter_date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_utilization = (
    encounters.groupby("month")
    .size()
    .reset_index(name="encounter_count")
)

print("\nMonthly utilization:")
print(monthly_utilization)


# 6. Emergency department utilization
emergency_encounters = (
    encounters["encounter_type"] == "Emergency"
).sum()

emergency_percentage = (
    emergency_encounters
    / total_encounters
    * 100
)

print(
    "\nEmergency encounters:",
    emergency_encounters
)

print(
    "Emergency utilization:",
    round(emergency_percentage, 2),
    "%"
)


# 7. Inpatient utilization
inpatient_encounters = (
    encounters["encounter_type"] == "Inpatient"
).sum()

inpatient_percentage = (
    inpatient_encounters
    / total_encounters
    * 100
)

print(
    "\nInpatient encounters:",
    inpatient_encounters
)

print(
    "Inpatient utilization:",
    round(inpatient_percentage, 2),
    "%"
)


# 8. Telehealth utilization
telehealth_encounters = (
    encounters["encounter_type"] == "Telehealth"
).sum()

telehealth_percentage = (
    telehealth_encounters
    / total_encounters
    * 100
)

print(
    "\nTelehealth encounters:",
    telehealth_encounters
)

print(
    "Telehealth utilization:",
    round(telehealth_percentage, 2),
    "%"
)


print("\nHealthcare utilization analysis completed successfully!")

# ============================================================
# COST & CLAIMS ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("COST & CLAIMS ANALYSIS")
print("=" * 60)

# ------------------------------------------------------------
# 1. Total financial amounts
# ------------------------------------------------------------

total_billed = claims["billed_amount"].sum()
total_allowed = claims["allowed_amount"].sum()
total_paid = claims["paid_amount"].sum()

print(f"\nTotal billed amount: ${total_billed:,.2f}")
print(f"Total allowed amount: ${total_allowed:,.2f}")
print(f"Total paid amount: ${total_paid:,.2f}")


# ------------------------------------------------------------
# 2. Average claim amounts
# ------------------------------------------------------------

average_billed = claims["billed_amount"].mean()
average_allowed = claims["allowed_amount"].mean()
average_paid = claims["paid_amount"].mean()

print(f"\nAverage billed per claim: ${average_billed:,.2f}")
print(f"Average allowed per claim: ${average_allowed:,.2f}")
print(f"Average paid per claim: ${average_paid:,.2f}")


# ------------------------------------------------------------
# 3. Claim status analysis
# ------------------------------------------------------------

claim_status_summary = (
    claims["claim_status"]
    .value_counts()
    .reset_index()
)

claim_status_summary.columns = [
    "claim_status",
    "claim_count"
]

claim_status_summary["percentage"] = (
    claim_status_summary["claim_count"]
    / len(claims)
    * 100
).round(2)

print("\nClaim status summary:")
print(claim_status_summary)


# ------------------------------------------------------------
# 4. Cost by encounter type
# ------------------------------------------------------------

cost_by_encounter = (
    encounters.groupby("encounter_type")
    .agg(
        encounter_count=("encounter_id", "count"),
        total_charge=("total_charge", "sum"),
        average_charge=("total_charge", "mean")
    )
    .reset_index()
)

cost_by_encounter["total_charge"] = (
    cost_by_encounter["total_charge"].round(2)
)

cost_by_encounter["average_charge"] = (
    cost_by_encounter["average_charge"].round(2)
)

print("\nCost by encounter type:")
print(cost_by_encounter)


# ------------------------------------------------------------
# 5. Cost by diagnosis
# ------------------------------------------------------------

cost_by_diagnosis = (
    encounters.groupby("diagnosis_code")
    .agg(
        encounter_count=("encounter_id", "count"),
        total_charge=("total_charge", "sum"),
        average_charge=("total_charge", "mean")
    )
    .reset_index()
)

cost_by_diagnosis = cost_by_diagnosis.merge(
    diagnoses[["diagnosis_code", "diagnosis_name", "category"]],
    on="diagnosis_code",
    how="left"
)

cost_by_diagnosis["total_charge"] = (
    cost_by_diagnosis["total_charge"].round(2)
)

cost_by_diagnosis["average_charge"] = (
    cost_by_diagnosis["average_charge"].round(2)
)

cost_by_diagnosis = cost_by_diagnosis.sort_values(
    "total_charge",
    ascending=False
)

print("\nTop diagnoses by total charge:")
print(
    cost_by_diagnosis[
        [
            "diagnosis_code",
            "diagnosis_name",
            "category",
            "encounter_count",
            "total_charge",
            "average_charge"
        ]
    ].head(10)
)


# ------------------------------------------------------------
# 6. Cost by claim status
# ------------------------------------------------------------

cost_by_status = (
    claims.groupby("claim_status")
    .agg(
        claim_count=("claim_id", "count"),
        billed_amount=("billed_amount", "sum"),
        allowed_amount=("allowed_amount", "sum"),
        paid_amount=("paid_amount", "sum")
    )
    .reset_index()
)

cost_by_status[
    ["billed_amount", "allowed_amount", "paid_amount"]
] = cost_by_status[
    ["billed_amount", "allowed_amount", "paid_amount"]
].round(2)

print("\nCost by claim status:")
print(cost_by_status)


# ------------------------------------------------------------
# 7. Claim payment rate
# ------------------------------------------------------------

paid_claims = (claims["claim_status"] == "Paid").sum()
total_claims = len(claims)

claim_payment_rate = (
    paid_claims / total_claims * 100
)

print(
    f"\nClaim payment rate: "
    f"{claim_payment_rate:.2f}%"
)


# ------------------------------------------------------------
# 8. Denied claim analysis
# ------------------------------------------------------------

denied_claims = claims[
    claims["claim_status"] == "Denied"
]

denied_count = len(denied_claims)

denied_billed_amount = denied_claims[
    "billed_amount"
].sum()

print(f"\nDenied claims: {denied_count}")
print(
    f"Total billed amount associated with denied claims: "
    f"${denied_billed_amount:,.2f}"
)


# ------------------------------------------------------------
# 9. Highest-cost encounter types
# ------------------------------------------------------------

highest_cost_type = cost_by_encounter.loc[
    cost_by_encounter["total_charge"].idxmax(),
    "encounter_type"
]

highest_cost_amount = cost_by_encounter.loc[
    cost_by_encounter["total_charge"].idxmax(),
    "total_charge"
]

print(
    f"\nHighest total cost encounter type: "
    f"{highest_cost_type}"
)

print(
    f"Total charges for {highest_cost_type}: "
    f"${highest_cost_amount:,.2f}"
)


# ------------------------------------------------------------
# 10. Claims analysis completed
# ------------------------------------------------------------

print("\nCost and claims analysis completed successfully!")

# ============================================================
# PROVIDER & FACILITY ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("PROVIDER & FACILITY ANALYSIS")
print("=" * 60)


# ------------------------------------------------------------
# 1. Encounter volume by provider
# ------------------------------------------------------------

provider_utilization = (
    encounters.groupby("provider_id")
    .agg(
        encounter_count=("encounter_id", "count"),
        total_charge=("total_charge", "sum"),
        average_charge=("total_charge", "mean"),
        unique_patients=("patient_id", "nunique")
    )
    .reset_index()
)

provider_utilization = provider_utilization.merge(
    providers[
        [
            "provider_id",
            "provider_name",
            "specialty",
            "facility_id",
            "state"
        ]
    ],
    on="provider_id",
    how="left"
)

provider_utilization["total_charge"] = (
    provider_utilization["total_charge"].round(2)
)

provider_utilization["average_charge"] = (
    provider_utilization["average_charge"].round(2)
)

provider_utilization = provider_utilization.sort_values(
    "encounter_count",
    ascending=False
)

print("\nTop providers by encounter volume:")
print(
    provider_utilization[
        [
            "provider_id",
            "provider_name",
            "specialty",
            "facility_id",
            "encounter_count",
            "unique_patients",
            "total_charge",
            "average_charge"
        ]
    ].head(10)
)


# ------------------------------------------------------------
# 2. Provider utilization summary by specialty
# ------------------------------------------------------------

specialty_summary = (
    provider_utilization.groupby("specialty")
    .agg(
        provider_count=("provider_id", "nunique"),
        encounter_count=("encounter_count", "sum"),
        total_charge=("total_charge", "sum"),
        average_charge=("average_charge", "mean")
    )
    .reset_index()
)

specialty_summary["total_charge"] = (
    specialty_summary["total_charge"].round(2)
)

specialty_summary["average_charge"] = (
    specialty_summary["average_charge"].round(2)
)

specialty_summary = specialty_summary.sort_values(
    "encounter_count",
    ascending=False
)

print("\nProvider utilization by specialty:")
print(specialty_summary)


# ------------------------------------------------------------
# 3. Facility utilization
# ------------------------------------------------------------

facility_utilization = (
    encounters.merge(
        providers[
            [
                "provider_id",
                "facility_id"
            ]
        ],
        on="provider_id",
        how="left"
    )
    .groupby("facility_id")
    .agg(
        encounter_count=("encounter_id", "count"),
        unique_patients=("patient_id", "nunique"),
        total_charge=("total_charge", "sum"),
        average_charge=("total_charge", "mean"),
        provider_count=("provider_id", "nunique")
    )
    .reset_index()
)

facility_utilization["total_charge"] = (
    facility_utilization["total_charge"].round(2)
)

facility_utilization["average_charge"] = (
    facility_utilization["average_charge"].round(2)
)

facility_utilization = facility_utilization.sort_values(
    "encounter_count",
    ascending=False
)

print("\nTop facilities by encounter volume:")
print(facility_utilization.head(10))


# ------------------------------------------------------------
# 4. Facility cost analysis
# ------------------------------------------------------------

facility_cost = facility_utilization.sort_values(
    "total_charge",
    ascending=False
)

print("\nTop facilities by total charges:")
print(
    facility_cost[
        [
            "facility_id",
            "encounter_count",
            "unique_patients",
            "provider_count",
            "total_charge",
            "average_charge"
        ]
    ].head(10)
)


# ------------------------------------------------------------
# 5. Provider encounter type analysis
# ------------------------------------------------------------

provider_encounter_types = (
    encounters.groupby(
        ["provider_id", "encounter_type"]
    )
    .size()
    .reset_index(name="encounter_count")
)

provider_encounter_types = provider_encounter_types.merge(
    providers[
        [
            "provider_id",
            "provider_name",
            "specialty"
        ]
    ],
    on="provider_id",
    how="left"
)

print("\nProvider encounter type distribution:")
print(
    provider_encounter_types[
        [
            "provider_id",
            "provider_name",
            "specialty",
            "encounter_type",
            "encounter_count"
        ]
    ].head(20)
)


# ------------------------------------------------------------
# 6. Highest-volume provider
# ------------------------------------------------------------

highest_volume_provider = provider_utilization.iloc[0]

print("\nHighest-volume provider:")
print(
    f"Provider: {highest_volume_provider['provider_name']}"
)

print(
    f"Specialty: {highest_volume_provider['specialty']}"
)

print(
    f"Encounter volume: "
    f"{int(highest_volume_provider['encounter_count'])}"
)

print(
    f"Unique patients: "
    f"{int(highest_volume_provider['unique_patients'])}"
)

print(
    f"Total charges: "
    f"${highest_volume_provider['total_charge']:,.2f}"
)


# ------------------------------------------------------------
# 7. Highest-cost facility
# ------------------------------------------------------------

highest_cost_facility = facility_cost.iloc[0]

print("\nHighest-cost facility:")

print(
    f"Facility: "
    f"{highest_cost_facility['facility_id']}"
)

print(
    f"Encounter volume: "
    f"{int(highest_cost_facility['encounter_count'])}"
)

print(
    f"Provider count: "
    f"{int(highest_cost_facility['provider_count'])}"
)

print(
    f"Total charges: "
    f"${highest_cost_facility['total_charge']:,.2f}"
)


# ------------------------------------------------------------
# 8. Provider & facility analysis completed
# ------------------------------------------------------------

print("\nProvider and facility analysis completed successfully!")

# ============================================================
# INPATIENT, LENGTH OF STAY & READMISSION ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("INPATIENT, LENGTH OF STAY & READMISSION ANALYSIS")
print("=" * 60)


# ------------------------------------------------------------
# 1. Select inpatient encounters
# ------------------------------------------------------------

inpatient = encounters[
    encounters["encounter_type"] == "Inpatient"
].copy()

print(f"\nTotal inpatient encounters: {len(inpatient)}")


# ------------------------------------------------------------
# 2. Length of Stay analysis
# ------------------------------------------------------------

average_los = inpatient["length_of_stay"].mean()
median_los = inpatient["length_of_stay"].median()
minimum_los = inpatient["length_of_stay"].min()
maximum_los = inpatient["length_of_stay"].max()

print(f"Average length of stay: {average_los:.2f} days")
print(f"Median length of stay: {median_los:.2f} days")
print(f"Minimum length of stay: {minimum_los} days")
print(f"Maximum length of stay: {maximum_los} days")


# ------------------------------------------------------------
# 3. Length of Stay distribution
# ------------------------------------------------------------

los_distribution = (
    inpatient["length_of_stay"]
    .value_counts()
    .sort_index()
    .reset_index()
)

los_distribution.columns = [
    "length_of_stay",
    "encounter_count"
]

los_distribution["percentage"] = (
    los_distribution["encounter_count"]
    / len(inpatient)
    * 100
).round(2)

print("\nLength of stay distribution:")
print(los_distribution)


# ------------------------------------------------------------
# 4. Long-stay inpatient encounters
# ------------------------------------------------------------

long_stays = inpatient[
    inpatient["length_of_stay"] >= 7
].copy()

long_stay_count = len(long_stays)

long_stay_percentage = (
    long_stay_count / len(inpatient) * 100
)

print(
    f"\nLong-stay encounters (7+ days): "
    f"{long_stay_count}"
)

print(
    f"Long-stay percentage: "
    f"{long_stay_percentage:.2f}%"
)


# ------------------------------------------------------------
# 5. Inpatient cost by length of stay
# ------------------------------------------------------------

los_cost_analysis = (
    inpatient.groupby("length_of_stay")
    .agg(
        encounter_count=("encounter_id", "count"),
        total_charge=("total_charge", "sum"),
        average_charge=("total_charge", "mean")
    )
    .reset_index()
)

los_cost_analysis["total_charge"] = (
    los_cost_analysis["total_charge"].round(2)
)

los_cost_analysis["average_charge"] = (
    los_cost_analysis["average_charge"].round(2)
)

print("\nCost by length of stay:")
print(los_cost_analysis)


# ------------------------------------------------------------
# 6. Identify patients with multiple inpatient encounters
# ------------------------------------------------------------

patient_inpatient_summary = (
    inpatient.groupby("patient_id")
    .agg(
        inpatient_encounters=("encounter_id", "count"),
        total_inpatient_days=("length_of_stay", "sum"),
        total_inpatient_charge=("total_charge", "sum")
    )
    .reset_index()
)

patient_inpatient_summary["total_inpatient_charge"] = (
    patient_inpatient_summary["total_inpatient_charge"].round(2)
)

repeat_inpatient_patients = patient_inpatient_summary[
    patient_inpatient_summary["inpatient_encounters"] > 1
].copy()

print(
    f"\nPatients with multiple inpatient encounters: "
    f"{len(repeat_inpatient_patients)}"
)


# ------------------------------------------------------------
# 7. Prepare encounters for readmission analysis
# ------------------------------------------------------------

readmission_data = encounters[
    [
        "encounter_id",
        "patient_id",
        "encounter_date",
        "encounter_type",
        "admission_date",
        "discharge_date",
        "length_of_stay",
        "diagnosis_code",
        "total_charge"
    ]
].copy()

readmission_data = readmission_data[
    readmission_data["encounter_type"] == "Inpatient"
].copy()

readmission_data = readmission_data.sort_values(
    ["patient_id", "admission_date"]
)


# ------------------------------------------------------------
# 8. Calculate next admission date
# ------------------------------------------------------------

readmission_data["next_admission_date"] = (
    readmission_data
    .groupby("patient_id")["admission_date"]
    .shift(-1)
)


# ------------------------------------------------------------
# 9. Calculate days until next admission
# ------------------------------------------------------------

readmission_data["days_to_next_admission"] = (
    readmission_data["next_admission_date"]
    - readmission_data["discharge_date"]
).dt.days


# ------------------------------------------------------------
# 10. Identify 30-day readmissions
# ------------------------------------------------------------

readmission_data["readmission_30_day"] = (
    (readmission_data["days_to_next_admission"] >= 0)
    &
    (readmission_data["days_to_next_admission"] <= 30)
)


# ------------------------------------------------------------
# 11. Readmission summary
# ------------------------------------------------------------

eligible_discharges = len(readmission_data)

readmissions_30_day = (
    readmission_data["readmission_30_day"].sum()
)

readmission_rate = (
    readmissions_30_day
    / eligible_discharges
    * 100
)

print(
    f"\nEligible inpatient discharges: "
    f"{eligible_discharges}"
)

print(
    f"30-day readmissions: "
    f"{readmissions_30_day}"
)

print(
    f"30-day readmission rate: "
    f"{readmission_rate:.2f}%"
)


# ------------------------------------------------------------
# 12. Patients with 30-day readmissions
# ------------------------------------------------------------

readmitted_patients = readmission_data[
    readmission_data["readmission_30_day"] == True
]["patient_id"].nunique()

print(
    f"Unique patients with 30-day readmissions: "
    f"{readmitted_patients}"
)


# ------------------------------------------------------------
# 13. Readmission detail
# ------------------------------------------------------------

readmission_details = readmission_data[
    readmission_data["readmission_30_day"] == True
][
    [
        "patient_id",
        "encounter_id",
        "discharge_date",
        "next_admission_date",
        "days_to_next_admission",
        "diagnosis_code",
        "total_charge"
    ]
].copy()

print("\nSample 30-day readmissions:")

print(
    readmission_details.head(10)
)


# ------------------------------------------------------------
# 14. Readmission analysis by diagnosis
# ------------------------------------------------------------

readmission_by_diagnosis = (
    readmission_data.groupby("diagnosis_code")
    .agg(
        inpatient_discharges=("encounter_id", "count"),
        readmissions_30_day=("readmission_30_day", "sum")
    )
    .reset_index()
)

readmission_by_diagnosis["readmission_rate"] = (
    readmission_by_diagnosis["readmissions_30_day"]
    / readmission_by_diagnosis["inpatient_discharges"]
    * 100
).round(2)

readmission_by_diagnosis = readmission_by_diagnosis.merge(
    diagnoses[
        [
            "diagnosis_code",
            "diagnosis_name",
            "category"
        ]
    ],
    on="diagnosis_code",
    how="left"
)

readmission_by_diagnosis = readmission_by_diagnosis.sort_values(
    "readmission_rate",
    ascending=False
)

print("\nReadmission analysis by diagnosis:")
print(
    readmission_by_diagnosis[
        [
            "diagnosis_code",
            "diagnosis_name",
            "category",
            "inpatient_discharges",
            "readmissions_30_day",
            "readmission_rate"
        ]
    ]
)


# ------------------------------------------------------------
# 15. Inpatient analysis completed
# ------------------------------------------------------------

print(
    "\nInpatient, LOS, and readmission analysis "
    "completed successfully!"
)

# ============================================================
# HIGH-UTILIZATION & HIGH-COST PATIENT ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("HIGH-UTILIZATION & HIGH-COST PATIENT ANALYSIS")
print("=" * 60)


# ------------------------------------------------------------
# 1. Patient utilization summary
# ------------------------------------------------------------

patient_utilization = (
    encounters.groupby("patient_id")
    .agg(
        total_encounters=("encounter_id", "count"),
        total_charges=("total_charge", "sum"),
        average_charge=("total_charge", "mean"),
        unique_providers=("provider_id", "nunique"),
        emergency_visits=(
            "encounter_type",
            lambda x: (x == "Emergency").sum()
        ),
        inpatient_visits=(
            "encounter_type",
            lambda x: (x == "Inpatient").sum()
        ),
        outpatient_visits=(
            "encounter_type",
            lambda x: (x == "Outpatient").sum()
        ),
        telehealth_visits=(
            "encounter_type",
            lambda x: (x == "Telehealth").sum()
        )
    )
    .reset_index()
)


# ------------------------------------------------------------
# 2. Add patient demographic information
# ------------------------------------------------------------

patient_utilization = patient_utilization.merge(
    patients[
        [
            "patient_id",
            "age",
            "gender",
            "state",
            "insurance_type",
            "chronic_condition"
        ]
    ],
    on="patient_id",
    how="left"
)


# ------------------------------------------------------------
# 3. Add total inpatient days
# ------------------------------------------------------------

inpatient_days = (
    inpatient.groupby("patient_id")
    ["length_of_stay"]
    .sum()
    .reset_index()
)

inpatient_days.columns = [
    "patient_id",
    "total_inpatient_days"
]

patient_utilization = patient_utilization.merge(
    inpatient_days,
    on="patient_id",
    how="left"
)

patient_utilization["total_inpatient_days"] = (
    patient_utilization["total_inpatient_days"]
    .fillna(0)
)


# ------------------------------------------------------------
# 4. Round financial metrics
# ------------------------------------------------------------

patient_utilization["total_charges"] = (
    patient_utilization["total_charges"].round(2)
)

patient_utilization["average_charge"] = (
    patient_utilization["average_charge"].round(2)
)


# ------------------------------------------------------------
# 5. High-utilization patients
# ------------------------------------------------------------

high_utilization = patient_utilization[
    (
        patient_utilization["total_encounters"] >= 10
    )
    |
    (
        patient_utilization["emergency_visits"] >= 3
    )
    |
    (
        patient_utilization["inpatient_visits"] >= 2
    )
].copy()

print(
    f"\nHigh-utilization patients: "
    f"{len(high_utilization)}"
)

print(
    f"High-utilization percentage: "
    f"{len(high_utilization) / len(patient_utilization) * 100:.2f}%"
)


# ------------------------------------------------------------
# 6. High-cost patients
# ------------------------------------------------------------

cost_threshold = patient_utilization[
    "total_charges"
].quantile(0.90)

high_cost_patients = patient_utilization[
    patient_utilization["total_charges"] >= cost_threshold
].copy()

print(
    f"\n90th percentile patient cost threshold: "
    f"${cost_threshold:,.2f}"
)

print(
    f"High-cost patients: "
    f"{len(high_cost_patients)}"
)


# ------------------------------------------------------------
# 7. Combined high-utilization and high-cost patients
# ------------------------------------------------------------

high_utilization_cost = patient_utilization[
    (
        patient_utilization["patient_id"].isin(
            high_utilization["patient_id"]
        )
    )
    &
    (
        patient_utilization["patient_id"].isin(
            high_cost_patients["patient_id"]
        )
    )
].copy()

print(
    f"\nPatients who are both high-utilization "
    f"and high-cost: "
    f"{len(high_utilization_cost)}"
)


# ------------------------------------------------------------
# 8. Sort high-utilization patients
# ------------------------------------------------------------

high_utilization_ranked = high_utilization.sort_values(
    [
        "total_encounters",
        "total_charges"
    ],
    ascending=False
)

print("\nTop high-utilization patients:")

print(
    high_utilization_ranked[
        [
            "patient_id",
            "age",
            "gender",
            "insurance_type",
            "chronic_condition",
            "total_encounters",
            "emergency_visits",
            "inpatient_visits",
            "total_inpatient_days",
            "total_charges"
        ]
    ].head(15)
)


# ------------------------------------------------------------
# 9. Highest-cost patients
# ------------------------------------------------------------

highest_cost_patients = high_cost_patients.sort_values(
    "total_charges",
    ascending=False
)

print("\nTop high-cost patients:")

print(
    highest_cost_patients[
        [
            "patient_id",
            "age",
            "gender",
            "insurance_type",
            "chronic_condition",
            "total_encounters",
            "emergency_visits",
            "inpatient_visits",
            "total_inpatient_days",
            "total_charges"
        ]
    ].head(15)
)


# ------------------------------------------------------------
# 10. High-utilization patients by insurance type
# ------------------------------------------------------------

high_utilization_by_insurance = (
    high_utilization.groupby("insurance_type")
    .agg(
        patient_count=("patient_id", "count"),
        average_encounters=("total_encounters", "mean"),
        total_charges=("total_charges", "sum"),
        average_charges=("total_charges", "mean")
    )
    .reset_index()
)

high_utilization_by_insurance["average_encounters"] = (
    high_utilization_by_insurance["average_encounters"]
    .round(2)
)

high_utilization_by_insurance["total_charges"] = (
    high_utilization_by_insurance["total_charges"]
    .round(2)
)

high_utilization_by_insurance["average_charges"] = (
    high_utilization_by_insurance["average_charges"]
    .round(2)
)

print("\nHigh-utilization patients by insurance type:")

print(high_utilization_by_insurance)


# ------------------------------------------------------------
# 11. High-utilization patients by chronic condition
# ------------------------------------------------------------

high_utilization_by_condition = (
    high_utilization.groupby("chronic_condition")
    .agg(
        patient_count=("patient_id", "count"),
        average_encounters=("total_encounters", "mean"),
        average_emergency_visits=("emergency_visits", "mean"),
        average_inpatient_visits=("inpatient_visits", "mean"),
        total_charges=("total_charges", "sum")
    )
    .reset_index()
)

high_utilization_by_condition[
    [
        "average_encounters",
        "average_emergency_visits",
        "average_inpatient_visits"
    ]
] = high_utilization_by_condition[
    [
        "average_encounters",
        "average_emergency_visits",
        "average_inpatient_visits"
    ]
].round(2)

high_utilization_by_condition["total_charges"] = (
    high_utilization_by_condition["total_charges"]
    .round(2)
)

print("\nHigh-utilization patients by chronic condition:")

print(high_utilization_by_condition)


# ------------------------------------------------------------
# 12. Overall patient utilization statistics
# ------------------------------------------------------------

print("\nOverall patient utilization statistics:")

print(
    f"Patients with encounters: "
    f"{len(patient_utilization)}"
)

print(
    f"Average encounters per patient: "
    f"{patient_utilization['total_encounters'].mean():.2f}"
)

print(
    f"Average emergency visits per patient: "
    f"{patient_utilization['emergency_visits'].mean():.2f}"
)

print(
    f"Average inpatient visits per patient: "
    f"{patient_utilization['inpatient_visits'].mean():.2f}"
)

print(
    f"Average total charges per patient: "
    f"${patient_utilization['total_charges'].mean():,.2f}"
)


# ------------------------------------------------------------
# 13. Analysis completed
# ------------------------------------------------------------

print(
    "\nHigh-utilization and high-cost patient analysis "
    "completed successfully!"
)

# ============================================================
# EXPORT DATASETS FOR SQL, EXCEL & POWER BI
# ============================================================

print("\n" + "=" * 60)
print("EXPORTING DATASETS")
print("=" * 60)

# Create folders for exported data
import os

os.makedirs("data", exist_ok=True)
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/cleaned", exist_ok=True)

# ------------------------------------------------------------
# Export raw datasets
# ------------------------------------------------------------

patients.to_csv(
    "data/raw/patients.csv",
    index=False
)

providers.to_csv(
    "data/raw/providers.csv",
    index=False
)

diagnoses.to_csv(
    "data/raw/diagnoses.csv",
    index=False
)

encounters.to_csv(
    "data/raw/encounters.csv",
    index=False
)

claims.to_csv(
    "data/raw/claims.csv",
    index=False
)


# ------------------------------------------------------------
# Export cleaned/analysis-ready datasets
# ------------------------------------------------------------

patient_utilization.to_csv(
    "data/cleaned/patient_utilization.csv",
    index=False
)

provider_utilization.to_csv(
    "data/cleaned/provider_utilization.csv",
    index=False
)

facility_utilization.to_csv(
    "data/cleaned/facility_utilization.csv",
    index=False
)

readmission_data.to_csv(
    "data/cleaned/inpatient_readmission_analysis.csv",
    index=False
)

high_utilization.to_csv(
    "data/cleaned/high_utilization_patients.csv",
    index=False
)

high_cost_patients.to_csv(
    "data/cleaned/high_cost_patients.csv",
    index=False
)


# ------------------------------------------------------------
# Export summary tables
# ------------------------------------------------------------

cost_by_encounter.to_csv(
    "data/cleaned/cost_by_encounter_type.csv",
    index=False
)

cost_by_diagnosis.to_csv(
    "data/cleaned/cost_by_diagnosis.csv",
    index=False
)

claim_status_summary.to_csv(
    "data/cleaned/claim_status_summary.csv",
    index=False
)

los_distribution.to_csv(
    "data/cleaned/length_of_stay_distribution.csv",
    index=False
)

readmission_by_diagnosis.to_csv(
    "data/cleaned/readmission_by_diagnosis.csv",
    index=False
)


# ------------------------------------------------------------
# Confirm exported files
# ------------------------------------------------------------

print("\nRaw datasets exported:")
print("  data/raw/patients.csv")
print("  data/raw/providers.csv")
print("  data/raw/diagnoses.csv")
print("  data/raw/encounters.csv")
print("  data/raw/claims.csv")

print("\nAnalysis datasets exported:")
print("  data/cleaned/patient_utilization.csv")
print("  data/cleaned/provider_utilization.csv")
print("  data/cleaned/facility_utilization.csv")
print("  data/cleaned/inpatient_readmission_analysis.csv")
print("  data/cleaned/high_utilization_patients.csv")
print("  data/cleaned/high_cost_patients.csv")

print("\nSummary datasets exported:")
print("  data/cleaned/cost_by_encounter_type.csv")
print("  data/cleaned/cost_by_diagnosis.csv")
print("  data/cleaned/claim_status_summary.csv")
print("  data/cleaned/length_of_stay_distribution.csv")
print("  data/cleaned/readmission_by_diagnosis.csv")

print("\nAll datasets exported successfully!")

# ============================================================
# CREATE SQL DATABASE FROM EXPORTED CSV FILES
# ============================================================

import sqlite3
import pandas as pd

print("\n" + "=" * 60)
print("CREATING SQL DATABASE")
print("=" * 60)

# Create SQLite database
conn = sqlite3.connect("healthcare_claims.db")

# Load CSV files into SQLite tables
patients_sql = pd.read_csv("data/raw/patients.csv")
providers_sql = pd.read_csv("data/raw/providers.csv")
diagnoses_sql = pd.read_csv("data/raw/diagnoses.csv")
encounters_sql = pd.read_csv("data/raw/encounters.csv")
claims_sql = pd.read_csv("data/raw/claims.csv")

# Write data into SQL tables
patients_sql.to_sql("patients", conn, if_exists="replace", index=False)
providers_sql.to_sql("providers", conn, if_exists="replace", index=False)
diagnoses_sql.to_sql("diagnoses", conn, if_exists="replace", index=False)
encounters_sql.to_sql("encounters", conn, if_exists="replace", index=False)
claims_sql.to_sql("claims", conn, if_exists="replace", index=False)

# Check table counts
print("\nSQL tables created successfully!")

print("Patients:", len(patients_sql))
print("Providers:", len(providers_sql))
print("Diagnoses:", len(diagnoses_sql))
print("Encounters:", len(encounters_sql))
print("Claims:", len(claims_sql))

conn.close()

print("\nDatabase created:")
print("healthcare_claims.db")

print("\nSQL database setup completed successfully!")