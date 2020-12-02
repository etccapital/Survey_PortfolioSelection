#Contains functions that are used in multiple modules.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#check if input is a valid portfolio
def isvalidport(port:np.array):
    #round to four digits to prevent slight numerical error from affecting the final result
    return round(sum(port),4) == 1 and sum([round(w,4) >= 0 for w in port]) == len(port)
