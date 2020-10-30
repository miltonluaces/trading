import numpy as np
import TrendFcst.TrendMethods as tm

def ValidateTrendFcst(ts, var, mw, fMethod):
    tbReal = tm.TrendBreaksMw(ts, var, mw)
    tbFcst = tm.TrendBreaksMwFcst(ts, var, mw, fMethod)
    diff = abs(np.array(tbReal) - np.array(tbFcst))
    mae = sum(diff)/len(tbReal)
    return(diff, mae)
 