import pandas as pd
import math

def adjust_elev(data, delta):
    df = data.copy()
    df["Z"] = df["Z"].apply(float)
    df.Z += delta
    return df

def read_txt(filepath):
    columns = ["Name", "X", "Y", "Z", "Desc", "Date", "Time"]
    return pd.read_csv(filepath, names=columns)

def get_data_by_elev_range(data, lower, upper):
    mask = data.Z.apply(lambda z: (z > lower) and (z < upper))
    return data.loc[mask]

def split_by_level(data, divs):
    dfs = []
    if len(divs) > 0:
        for i in range(len(divs) -1):
            dfs.append(get_data_by_elev_range(data, divs[i], divs[i+1]))
    return dfs

def get_feet_inches_str(dist, fraction):
    ft = abs(math.trunc(dist))
    dec_in = 12 * math.modf(dist)[0]
    inch = abs(math.trunc(dec_in))
    frac = abs(round(fraction * math.modf(dec_in)[0]))
    return f"""{"-" if dist < 0 else ""}{ft}' {inch}-{frac}/{fraction}\""""

def get_feet_inches(data, fraction=8, adjust=0):
    df = data.copy()
    df["adj_elev"] = adjust_elev(df, adjust).Z
    df["ft_in"] = df.adj_elev.apply(lambda z: get_feet_inches_str(z, fraction))
    return df