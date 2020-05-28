import pandas as pd
import pathlib
from enum import Enum
from datetime import datetime


class CurveTypes(Enum):
    Flat = 1
    KVPair = 2

class CurveUndefinedError(Exception):
    pass

class InvalidCurveTypeError(Exception):
    pass

class Curve(object):
    def __init__(self, curve_name):

        curve_config = pd.read_csv(str(pathlib.Path().absolute()) + '/assumptions/curve_config.csv')
        # TODO: Refactor code used below to get curve type
        if curve_config.loc[curve_config['Curve Name'] == curve_name]['Curve Type'].to_string(index=False)[1:] == 'Flat':
            self.curve = [float(curve_config.loc[curve_config['Curve Name'] == curve_name]['Curve Value'])] * 720
            self.effective_date = datetime.strptime(curve_config.loc[curve_config['Curve Name'] == curve_name]['Effective Date'].to_string(index=False)[1:], '%d/%m/%Y')
        else:
            raise InvalidCurveTypeError("'{}' is not a valid curve type.".format(str(curve_config.loc[curve_config['Curve Name'] == curve_name]['Curve Type'])))
    def value(self, lookup):
        try:
            return self.curve[lookup]
        except IndexError:
            raise CurveUndefinedError("Curve not defined at date.")
