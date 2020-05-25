from mortality import *
from curve import *

class ImmediateAnnuity(object):
    def __init__(self, amount_of_annuity, age_at_purchase, annuitant_sex, purchase_date, base_mortality_file_name):
        self.amount_of_annuity = amount_of_annuity
        self.age_at_purchase = age_at_purchase
        self.purchase_date = purchase_date
        self.annuitant_sex = annuitant_sex
        self.mortality = Mortality(base_mortality_file_name)
        self.risk_free_rate = Curve(CurveTypes.Flat, 0.01)

    # Calculates the present value of the annuity at the time of purchase
    def project_value(self, write_output=False):
        # Probability of policy being in force at time 0 is 1
        prob_in_force = 1
        # Discount factor applied to first payment taken to be 1, since annuity paid (annually) in advance (from
        # purchase date)
        discount_factor = 1
        # Calculate cumulative expected present value of annuity payments
        cumulative_epv_of_payments = 0
        for t_proj in range(0, self.mortality.age_cap - self.age_at_purchase + 1):
            age = self.age_at_purchase + t_proj
            discount_factor /= 1 + self.risk_free_rate.value(t_proj)
            epv_of_payment = self.amount_of_annuity * discount_factor * prob_in_force
            cumulative_epv_of_payments += epv_of_payment
            if write_output:
                print('{} -- {} -- {} -- {}'.format(age, prob_in_force, epv_of_payment, cumulative_epv_of_payments))
            prob_in_force *= 1 - self.mortality.value(age, self.annuitant_sex, ProductTypes.ImmAnn, t_proj)
        return cumulative_epv_of_payments




