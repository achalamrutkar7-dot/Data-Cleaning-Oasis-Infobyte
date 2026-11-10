
import pandas as pd
import numpy as np
import os

# =========================================================
# TASK 3: DATA CLEANING
# OASIS INFOBYTE - DATA ANALYTICS
# =========================================================

# Create output folder
os.makedirs("output", exist_ok=True)

# =========================================================
# 1. LOAD DATASET
# =========================================================

file_path = "dataset/data_cleaning_sample.csv"

df = pd.read_csv(file_path)

# Keep a copy of the original dataset
original_df = df.copy()

print("=" * 60)
print("DATA CLEANING PROJECT")
print("=" * 60)

print("\nOriginal Dataset:")
print(df.head())

# =========================================================
# 2. ORIGINAL DATA QUALITY REPORT
# =========================================================

original_rows = len(df)
original_columns = len(df.columns)
original_missing = int(df.isnull().sum().sum())
original_duplicates = int(df.duplicated().sum())

print("\nORIGINAL DATA QUALITY REPORT")

print("\nDataset Shape:")
print(df.shape)

print("\nMissing Values Per Column:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(original_duplicates)

print("\nOriginal Data Types:")
print(df.dtypes)

print("\nNumeric Column Statistics:")
print(df.describe())

# =========================================================
# 3. CLEAN COLUMN NAMES
# =========================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
)

# =========================================================
# 4. REMOVE DUPLICATE ROWS
# =========================================================

duplicates_removed = int(df.duplicated().sum())

df = df.drop_duplicates()

print("\nDuplicates Removed:", duplicates_removed)

# =========================================================
# 5. STANDARDIZE TEXT VALUES
# =========================================================

text_columns = df.select_dtypes(include=["object", "string"]).columns

for column in text_columns:

    # Remove leading and trailing spaces
    df[column] = df[column].astype("string").str.strip()

    # Convert empty strings to missing values
    df[column] = df[column].replace("", pd.NA)

# Standardize common categorical columns
categorical_columns = [
    "name",
    "gender",
    "city",
    "department",
    "category"
]

for column in categorical_columns:

    if column in df.columns:
        df[column] = df[column].str.title()

# =========================================================
# 6. CORRECT NUMERIC DATA TYPES
# =========================================================

numeric_columns = [
    "age",
    "salary",
    "experience",
    "marks",
    "quantity",
    "price",
    "amount",
    "attendance",
    "percentage"
]

for column in numeric_columns:

    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

# =========================================================
# 7. CORRECT DATE DATA TYPES
# =========================================================

date_columns = [
    column for column in df.columns
    if "date" in column.lower()
]

for column in date_columns:

    df[column] = pd.to_datetime(
        df[column],
        errors="coerce"
    )

# =========================================================
# 8. HANDLE MISSING VALUES
# =========================================================

print("\nMissing Values Before Imputation:")
print(df.isnull().sum())

# Numeric columns:
# Median is used because it is less affected by outliers
for column in df.select_dtypes(include=["number"]).columns:

    if df[column].isnull().any():

        median_value = df[column].median()

        if pd.notna(median_value):
            df[column] = df[column].fillna(median_value)

# Text columns:
# Mode is used to fill missing categorical values
for column in df.select_dtypes(include=["object", "string"]).columns:

    if df[column].isnull().any():

        mode_values = df[column].mode(dropna=True)

        if not mode_values.empty:
            df[column] = df[column].fillna(mode_values.iloc[0])
        else:
            df[column] = df[column].fillna("Unknown")

# Date columns:
# Missing dates are filled with the most frequent valid date
for column in date_columns:

    if df[column].isnull().any():

        mode_dates = df[column].mode(dropna=True)

        if not mode_dates.empty:
            df[column] = df[column].fillna(mode_dates.iloc[0])

print("\nMissing Values After Imputation:")
print(df.isnull().sum())

# =========================================================
# 9. HANDLE INVALID NUMERIC VALUES
# =========================================================

# Negative values are not valid for these fields
non_negative_columns = [
    "age",
    "salary",
    "experience",
    "quantity",
    "price",
    "amount"
]

for column in non_negative_columns:

    if column in df.columns:
        df = df[df[column] >= 0]

# Marks, attendance, and percentage should be between 0 and 100
percentage_columns = [
    "marks",
    "attendance",
    "percentage"
]

for column in percentage_columns:

    if column in df.columns:

        df = df[
            (df[column] >= 0) &
            (df[column] <= 100)
        ]

# =========================================================
# 10. OUTLIER DETECTION USING IQR
# =========================================================

print("\nOUTLIER DETECTION USING IQR")

outlier_report = []

numeric_columns = df.select_dtypes(include=["number"]).columns

for column in numeric_columns:

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[
        (df[column] < lower_bound) |
        (df[column] > upper_bound)
    ]

    outlier_count = len(outliers)

    outlier_report.append({
        "Column": column,
        "Q1": Q1,
        "Q3": Q3,
        "IQR": IQR,
        "Lower Bound": lower_bound,
        "Upper Bound": upper_bound,
        "Outlier Count": outlier_count,
        "Decision": "Retained for review"
    })

    print(f"\nColumn: {column}")
    print("Lower Bound:", lower_bound)
    print("Upper Bound:", upper_bound)
    print("Outlier Count:", outlier_count)

# Save outlier report
outlier_df = pd.DataFrame(outlier_report)

outlier_df.to_csv(
    "output/outlier_report.csv",
    index=False
)

# =========================================================
# 11. FINAL DATA QUALITY REPORT
# =========================================================

final_rows = len(df)
final_columns = len(df.columns)
final_missing = int(df.isnull().sum().sum())
final_duplicates = int(df.duplicated().sum())

print("\nFINAL DATA QUALITY REPORT")

print("\nFinal Dataset Shape:")
print(df.shape)

print("\nFinal Missing Values:")
print(df.isnull().sum())

print("\nFinal Duplicate Rows:")
print(final_duplicates)

print("\nFinal Data Types:")
print(df.dtypes)

# =========================================================
# 12. BEFORE AND AFTER COMPARISON
# =========================================================

comparison = pd.DataFrame({
    "Metric": [
        "Rows",
        "Columns",
        "Missing Values",
        "Duplicate Rows"
    ],

    "Before Cleaning": [
        original_rows,
        original_columns,
        original_missing,
        original_duplicates
    ],

    "After Cleaning": [
        final_rows,
        final_columns,
        final_missing,
        final_duplicates
    ]
})

print("\nBEFORE AND AFTER COMPARISON")
print(comparison)

comparison.to_csv(
    "output/before_after_comparison.csv",
    index=False
)

# =========================================================
# 13. SAVE CLEANED DATASET
# =========================================================

df.to_csv(
    "output/cleaned_data.csv",
    index=False
)

print("\nCleaned dataset saved:")
print("output/cleaned_data.csv")

# =========================================================
# 14. SAVE CLEANING REPORT
# =========================================================

cleaning_report = pd.DataFrame({
    "Metric": [
        "Original Rows",
        "Original Columns",
        "Final Rows",
        "Final Columns",
        "Missing Values Before Cleaning",
        "Missing Values After Cleaning",
        "Duplicate Rows Removed",
        "Final Duplicate Rows"
    ],

    "Value": [
        original_rows,
        original_columns,
        final_rows,
        final_columns,
        original_missing,
        final_missing,
        duplicates_removed,
        final_duplicates
    ]
})

cleaning_report.to_csv(
    "output/cleaning_report.csv",
    index=False
)

print("\nCleaning report saved:")
print("output/cleaning_report.csv")

# =========================================================
# 15. SAVE CLEANING DECISIONS
# =========================================================

cleaning_decisions = pd.DataFrame({
    "Cleaning Step": [
        "Missing numeric values",
        "Missing categorical values",
        "Missing date values",
        "Duplicate records",
        "Text standardization",
        "Invalid numeric values",
        "Outlier detection",
        "Data type correction"
    ],

    "Decision": [
        "Filled with median",
        "Filled with mode",
        "Filled with most frequent valid date",
        "Removed exact duplicate rows",
        "Removed spaces and standardized capitalization",
        "Removed records outside valid ranges",
        "Detected using IQR; retained for review",
        "Converted numeric and date columns to appropriate types"
    ],

    "Reason": [
        "Median is less sensitive to extreme values",
        "Mode preserves the most common category",
        "Uses the most common valid date",
        "Duplicate records can distort analysis",
        "Improves consistency",
        "Ensures values follow valid ranges",
        "Outliers may be valid observations and should be reviewed",
        "Ensures correct analysis and calculations"
    ]
})

cleaning_decisions.to_csv(
    "output/cleaning_decisions.csv",
    index=False
)

print("\nCleaning decisions saved:")
print("output/cleaning_decisions.csv")

# =========================================================
# 16. COMPLETION MESSAGE
# =========================================================

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETED SUCCESSFULLY!")
print("=" * 60)

print("\nFiles created in the output folder:")
print("1. cleaned_data.csv")
print("2. cleaning_report.csv")
print("3. outlier_report.csv")
print("4. before_after_comparison.csv")
print("5. cleaning_decisions.csv")
