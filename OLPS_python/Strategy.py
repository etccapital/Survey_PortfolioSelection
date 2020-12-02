import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Abstract Interface for all Strategy subclasses
#may become more useful in the future
class Strategy():
    #returns an OLPS result object
    def run(self, df:pd.DataFrame):
        pass
    def name(self):
        pass
