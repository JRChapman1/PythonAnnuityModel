from annuity_model import *
import pandas as pd
import pathlib


inputs = pd.read_csv(str(pathlib.Path().absolute()) + '/policy data/annuity_policy_data_single_policy.csv')
valuation_date = '31/12/2020'
output_location = str(pathlib.Path().absolute()) + '/output'

output = pd.DataFrame(columns=['Time Step', 'Projection Date', 'Subtotal Key', 'PH Age', 'Qx', 'Qxpm', 'Prob IF',
                               'Discount Factor', 'Benefit EPV'])

for index, row in inputs.iterrows():
    annuity = ImmediateAnnuity(row['Policy ID'],
                               row['Amount of annuity'],
                               row['Annuitant Date of Birth'],
                               row['Annuitant sex'],
                               row['First Payment Date'],
                               'base_mortality')
    output = output.append(annuity.project_value(valuation_date))

if output_location != '':
    output.to_csv(output_location + '/foo.csv')

print(output)

print('\n--------------------------------------------------------------------------------')
print('EPV of Liabilities at valuation date ({}): £{:,.2f}'.format(valuation_date, output['Benefit EPV'].sum(), 2))
print('\n--------------------------------------------------------------------------------')


