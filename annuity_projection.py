import pathlib
from annuity_model import *
import pandas as pd
import globals


globals.init()

inputs = pd.read_csv(str(pathlib.Path().absolute()) + '/policy data/annuity_policy_data.csv')
assumption_set_id = 10003
valuation_date = '01/12/2018'
output_location = str(pathlib.Path().absolute()) + '/output'

output = pd.DataFrame(columns=['Time Step', 'Projection Date', 'Subtotal Key', 'PH Age', 'Qx', 'Qxpm', 'Prob IF',
                               'Discount Factor', 'Benefit EPV'])

for index, row in inputs.iterrows():
    annuity = ImmediateAnnuity(row['Policy ID'],
                               row['Amount of annuity'],
                               row['Annuitant Date of Birth'],
                               row['Annuitant sex'],
                               row['First Payment Date'],
                               assumption_set_id)
    output = output.append(annuity.project_value(valuation_date))

output['Benefit EPV'].fillna(0, inplace=True)
print(output)

grand_totals = output.groupby(['Time Step', 'Projection Date'], as_index=False).sum()
grand_totals['Subtotal Key'] = 'grand_totals'
grand_totals['PH Age'] = ''
grand_totals['Qx'] = ''
grand_totals['Qxpm'] = ''
grand_totals['Prob IF'] = ''
grand_totals['Discount Factor'] = ''

output = output.append(grand_totals)
print(output)

if output_location != '':
    output.to_csv(output_location + '/grand_totals_test.csv')

print('\n--------------------------------------------------------------------------------')
print('EPV of Liabilities at valuation date ({}): £{:,.2f}'.format(valuation_date, output['Benefit EPV'].sum(), 2))
print('\n--------------------------------------------------------------------------------')


