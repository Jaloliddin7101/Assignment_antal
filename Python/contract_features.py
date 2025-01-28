import pandas as pd
import json
from datetime import datetime

def parse_application_date(date_str):
    #Parse a date string with format 'DD.MM.YYYY' into a datetime object
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%d.%m.%Y").replace(tzinfo=None)
    except ValueError as e:
        print(f"Date parsing error: {e} with date string: {date_str}")
        return None

def calculate_features(row):
    contracts_str = row['contracts']

    try:
        contracts = json.loads(contracts_str) if pd.notna(contracts_str) else []
    except json.JSONDecodeError:
        print(f"JSON decode error for row ID {row['id']}: {contracts_str}")
        contracts = []

    
    if isinstance(contracts, dict):  
        contracts = [contracts]
    elif not isinstance(contracts, list):  
        print(f"Error: Contracts data is not a list in row ID {row['id']}. Data: {contracts_str}")
        return pd.Series({
            'tot_claim_cnt_l180d': -3,
            'disb_bank_loan_wo_tbc': -1,  
            'day_sinlastloan': -1        
        })
    
    today = datetime.now().replace(tzinfo=None)
    tot_claim_cnt_l180d = 0
    disbursements_sum = 0
    last_loan_date = None
    has_loans = False  

    for contract in contracts:
        if not isinstance(contract, dict):
            continue  

        claim_date = parse_application_date(contract.get('claim_date'))
        if claim_date and (today - claim_date).days <= 180:
            tot_claim_cnt_l180d += 1

        contract_date = parse_application_date(contract.get('contract_date'))
        loan_summa_str = contract.get('loan_summa', 0)
        summa = contract.get('summa')

        # Check if it's a valid loan
        if summa and contract_date:
            has_loans = True

        
        if contract.get('bank') not in ['LIZ', 'LOM', 'MKO', 'SUG', None] and contract_date:
            try:
                loan_summa = int(loan_summa_str) if str(loan_summa_str).isdigit() else 0
            except ValueError:
                loan_summa = 0  
            disbursements_sum += loan_summa

        if summa and contract_date and (last_loan_date is None or contract_date > last_loan_date):
            last_loan_date = contract_date

    application_date = pd.to_datetime(row['application_date']).replace(tzinfo=None)
    days_since_last_loan = (application_date - last_loan_date).days if last_loan_date else -1

    return pd.Series({
        'tot_claim_cnt_l180d': -3 if tot_claim_cnt_l180d == 0 else tot_claim_cnt_l180d,
        'disb_bank_loan_wo_tbc': -1 if not has_loans else disbursements_sum,
        'day_sinlastloan': -1 if not has_loans else days_since_last_loan
    })

data = pd.read_csv("data.csv")
features = data.apply(calculate_features, axis=1)
data = pd.concat([data[['id']], features], axis=1)
data.to_csv('contract_features.csv', index=False)
