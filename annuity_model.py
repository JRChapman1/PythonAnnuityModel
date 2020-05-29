from mortality import *
from curve import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import globals


class ImmediateAnnuity(object):
    def __init__(self, policy_id, amount_of_annuity, date_of_birth, annuitant_sex, first_benefit_date, assumption_set_id):
        # TODO: Might this be better if contained in a dictionary?
        assumptions = pd.read_csv(str(pathlib.Path().absolute()) + '/assumptions/assumption_sets.csv', index_col='Assumption Set ID')
        curve_basis = pd.read_csv(str(pathlib.Path().absolute()) + '/assumptions/curve_basis.csv', index_col=['Curve Sensitivity', 'Curve Group'])
        mortality_sensitivity = assumptions.loc[assumption_set_id]['Mortality Sensitivity']
        curve_sensitivity = assumptions.loc[assumption_set_id]['Curve Sensitivity']
        self.policy_id = policy_id
        self.amount_of_annuity = amount_of_annuity
        self.date_of_birth = datetime.strptime(date_of_birth, '%d/%m/%Y')
        self.first_benefit_date = datetime.strptime(first_benefit_date, '%d/%m/%Y')
        self.annuitant_sex = annuitant_sex
        self.mortality = Mortality(mortality_sensitivity)
        self.risk_free_rate = Curve(curve_basis.loc[curve_sensitivity, 'interest_rate']['Curve Instance'])
        self.inflation_rate = Curve(curve_basis.loc[curve_sensitivity, 'inflation_rate']['Curve Instance'])

    # Calculates the present value of the annuity at the time of purchase
    def project_value(self, valuation_date, projection_points=700):
        valuation_date = datetime.strptime(valuation_date, '%d/%m/%Y')
        output = pd.DataFrame(columns=['Time Step', 'Projection Date', 'Subtotal Key', 'PH Age', 'Qx', 'Qxpm', 'Prob IF', 'Discount Factor', 'Benefit EPV'])
        prob_in_force = 1
        discount_factor = 1
        for projection_time_step in range(0, projection_points + 1):
            projection_date = valuation_date + relativedelta(months=projection_time_step)
            ph_age = relativedelta(projection_date, self.date_of_birth).years
            output = output.append({'Time Step': projection_time_step,
                                    'Projection Date': projection_date,
                                    'Subtotal Key': 'policy_' + str(self.policy_id),
                                    'PH Age': ph_age,
                                    'Qx': self.mortality.qxpa(ph_age, self.annuitant_sex, ProductTypes.ImmAnn, 0),
                                    'Qxpm': self.mortality.qxpm(ph_age, self.annuitant_sex, ProductTypes.ImmAnn, 0),
                                    'Prob IF': prob_in_force,
                                    'Discount Factor': discount_factor,
                                    'Benefit EPV': self.payment_amount(projection_date) * discount_factor * prob_in_force},
                                   ignore_index=True)
            prob_in_force *= 1 - self.mortality.qxpm(ph_age, self.annuitant_sex, ProductTypes.ImmAnn, 0)
            discount_factor /= (1 + self.risk_free_rate.value(projection_time_step))
        return output

    # Returns the amount of the annuity payment made on a specified payment date
    def payment_amount(self, date):
        if date >= self.first_benefit_date:
            return self.amount_of_annuity / 12
        else:
            return 0