import pandas as pd

def convert_units(series, target_unit):
    """
    Convert production from e3m3/d to target unit.
    Input: pandas Series
    Output: pandas Series
    """

    if target_unit == "e3m3d":
        return series

    elif target_unit == "mmcfd":
        return series * 35.3147

    elif target_unit == "bcm/year":
        return series * 365 / 1e6

    elif target_unit == "mtpa":
        return series * 365 / 1e6 * 0.73

    else:
        raise ValueError("Unsupported unit")
