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

def upload_file(request):
    if request.method == 'POST' and 'trial_balance_file' in request.FILES:
        form = TrialBalanceForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['trial_balance_file']
            # Check the file extension (Excel or CSV)
            if file.name.endswith('.csv'):
                # Read CSV file into a DataFrame
                df = pd.read_csv(file)
            elif file.name.endswith('.xlsx'):
                # Read Excel file into a DataFrame
                df = pd.read_excel(file)
            else:
                return HttpResponse("Invalid file type. Please upload a CSV or Excel file.")
            
            # Validate and process the data (example: check columns for trial balance)
            # Assuming 'account_name', 'debit', and 'credit' are columns in the file
            if all(col in df.columns for col in ['account_name', 'debit', 'credit']):
                # You can now process the data (e.g., store it, perform calculations)
                return HttpResponse("File processed successfully!")
            else:
                return HttpResponse("File does not have the required columns: account_name, debit, credit.")
    else:
        form = TrialBalanceForm()

    return render(request, 'file_upload/upload.html', {'form': form})

