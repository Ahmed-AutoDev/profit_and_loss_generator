# Automated Profit & Loss(P&L) Generator

This project automates generating Profit & Loss statements trial balance data from an Excel or CSV file as input. It validates the input file for certain requirements, categorizes accounts, and performs necessary calculations.

## Features

- **File Upload and Data Validation:** This takes input file as Excel or CSV, it then checks the uploaded file to ensure it meets the requirements of the tool. It then raises errors based on the file's missing requirements (s).
- **Profit & Loss Calculation:** This feature automatically calculates Net Profit after determining the totals of the revenue and expenses.


## Getting Started

### Prerequisites

- Python 3.8 or later
- Required libraries:
  - `pandas`  `openpyxl`

### Input Data Requirements

The input data file must be an Excel or a CSV file with the following structure:

- **Required Columns**: Account Name, Debit Amount, Credit Amount  

