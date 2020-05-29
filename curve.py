import pandas as pd
import pathlib
from enum import Enum
from datetime import datetime
import globals


class CurveTypes(Enum):
    Flat = 1
    KVPair = 2

class CurveUndefinedError(Exception):
    pass

class InvalidCurveTypeError(Exception):
    pass

class Curve(object):
    def __init__(self, curve_name):

        curve_config = pd.read_csv(str(pathlib.Path().absolute()) + '/assumptions/curve_config.csv', index_col='Curve Name')
        if curve_config.loc[curve_name]['Curve Type'] == 'Flat':
            self.curve = [curve_config.loc[curve_name]['Curve Value']] * 720
            self.effective_date = datetime.strptime(curve_config.loc[curve_name]['Effective Date'], '%d/%m/%Y')
        elif curve_config.loc[curve_name]['Curve Type'] == 'KVPair':
            curve_instance_name = curve_config.loc[curve_name]['Curve Value']
            self.curve = globals.curve_data.loc[curve_instance_name]['Curve Value'].tolist()
            self.effective_date = datetime.strptime(curve_config.loc[curve_name]['Effective Date'], '%d/%m/%Y')
        else:
            raise InvalidCurveTypeError("'{}' is not a valid curve type.".format(str(curve_config.loc[curve_name]['Curve Type'])))
    def value(self, lookup):
        try:
            return float(self.curve[lookup])
        except IndexError:
            raise CurveUndefinedError("Curve not defined at date.")
