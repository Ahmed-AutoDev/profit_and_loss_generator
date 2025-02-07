from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse
from django import forms

# Create your views here.
def home(request):
    return render(request, "file_upload/home.html", {})


class TrialBalanceForm(forms.Form):
    trial_balance_file = forms.FileField(label='Upload Trial Balance (Excel/CSV)', 
                                         help_text="Upload your trial balance as an Excel or CSV file.")

def validate_trial_balance(df):
    errors = []
    required_columns = ['Account Name', 'Debit Amount', 'Credit Amount']
    
    # Check for required columns
    if not all(col in df.columns for col in required_columns):
        errors.append("File does not contain the required columns: Account Name', 'Debit Amount', 'Credit Amount. Kindly edit your file to include required columns")
        return errors  # No need to check further if columns are missing
    
    # Drop completely empty rows
    df.dropna(how='all', inplace=True)
    
    # Check for missing values
    missing_values = df.isnull().sum()
    for col in required_columns:
        if missing_values[col] > 0:
            errors.append(f"Column '{col}' contains {missing_values[col]} missing values.")
    
    # Validate debit and credit columns contain only numbers
    if not pd.to_numeric(df['debit'], errors='coerce').notna().all():
        errors.append("Column 'debit' contains non-numeric values.")
    if not pd.to_numeric(df['credit'], errors='coerce').notna().all():
        errors.append("Column 'credit' contains non-numeric values.")
    
    return errors

def upload_file(request):
    if request.method == 'POST' and 'trial_balance_file' in request.FILES:
        form = TrialBalanceForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['trial_balance_file']
            
            # Read file into DataFrame
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.name.endswith('.xlsx'):
                    df = pd.read_excel(file)
                else:
                    return HttpResponse("Invalid file type. Please upload a CSV or Excel file.")
            except Exception as e:
                return HttpResponse(f"Error reading file: {str(e)}")
            
            # Validate the data
            errors = validate_trial_balance(df)
            if errors:
                return HttpResponse("Errors detected:<br>" + "<br>".join(errors))
            
            return HttpResponse("File processed successfully!")
    else:
        form = TrialBalanceForm()
    
    return render(request, 'file_upload/upload.html', {'form': form})


def calculate_profit_and_loss(df):
    revenue_accounts = ['Sales', 'Service Revenue', 'Interest Income']  
    expense_accounts = ['Rent Expense', 'Salary Expense', 'Utilities Expense', 'Cost of Goods Sold']  
    
    df['debit'] = pd.to_numeric(df['debit'], errors='coerce').fillna(0)
    df['credit'] = pd.to_numeric(df['credit'], errors='coerce').fillna(0)
    
    revenue = df[df['account_name'].isin(revenue_accounts)]['credit'].sum()
    expenses = df[df['account_name'].isin(expense_accounts)]['debit'].sum()
    
    net_profit_loss = revenue - expenses
    
    return pd.DataFrame({
        "Category": ["Total Revenue", "Total Expenses", "Net Profit/Loss"],
        "Amount": [revenue, expenses, net_profit_loss]
    })

