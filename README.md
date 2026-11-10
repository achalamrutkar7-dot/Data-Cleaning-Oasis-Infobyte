# Oasis Infobyte Internship — Data Cleaning Project

## Project Overview
This project is part of the Oasis Infobyte Data Analytics Internship (Level 1, Task 3). The main objective is to clean and preprocess a raw dataset to improve its quality and make it ready for further analysis.

## Objective
To identify and handle missing values, duplicate records, inconsistent formatting, incorrect data types, invalid values, and potential outliers.

## Tools and Technologies
- Python
- Pandas
- NumPy
- Visual Studio Code

## Project Structure
```text
Data_Cleaning_Project/
├── dataset/
│   └── data_cleaning_sample.csv
├── output/
│   ├── cleaned_data.csv
│   ├── cleaning_report.csv
│   ├── outlier_report.csv
│   ├── before_after_comparison.csv
│   └── cleaning_decisions.csv
├── data_cleaning.py
└── README.md
```

## Data Cleaning Steps
1. Loaded the raw dataset.
2. Generated a data-quality report.
3. Identified and handled missing values.
4. Removed duplicate records.
5. Standardized text and categorical values.
6. Corrected data types.
7. Checked invalid numeric values and ranges.
8. Detected potential outliers using the IQR method.
9. Compared the dataset before and after cleaning.
10. Exported the cleaned dataset and supporting reports.

## Output Files
- **cleaned_data.csv** — Final cleaned dataset.
- **cleaning_report.csv** — Data quality report.
- **outlier_report.csv** — Potential outlier details.
- **before_after_comparison.csv** — Comparison of the dataset before and after cleaning.
- **cleaning_decisions.csv** — Documentation of cleaning decisions.

## How to Run the Project

Install the required libraries:

```bash
python -m pip install pandas numpy
```

Run the Python script:

```bash
python data_cleaning.py
```

## Conclusion
This project demonstrates practical data cleaning and preprocessing techniques using Python, Pandas, and NumPy. The cleaned dataset and reports provide a better-quality dataset for future data analysis.

## Internship
Oasis Infobyte — Data Analytics Internship