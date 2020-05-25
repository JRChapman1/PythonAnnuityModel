from annuity_model import *
import pandas as pd



inputs = pd.read_csv('/Users/joshchapman/PycharmProjects/IC/venv/policy data/annuity_policy_data.csv')

for index, row in inputs.iterrows():
    annuity = ImmediateAnnuity(row['Amount of annuity'],
                               row['Annuitant age at purchase'],
                               row['Annuitant sex'],
                               row['Purchase date'],
                               'base_mortality')
    print(annuity.project_value())