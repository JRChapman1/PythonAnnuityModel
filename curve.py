import pandas as pd
from enum import Enum

class CurveTypes(Enum):
    Flat = 1
    KVPair = 2

class Curve(object):
    def __init__(self, curve_type, curve_value):
        if curve_type == CurveTypes.Flat:
            self.curve = [curve_value] * 720
        else:
            print('unsupported curve type')

    def value(self, lookup):
        return self.curve[lookup]