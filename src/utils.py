import pandas as pd
import numpy as np
import re
from pandas.api.types import is_string_dtype
from pandas.core.dtypes.common import is_numeric_dtype

#funções do modulo structured do fast.ai

def add_datepart(df, fldname, drop=True, time=False):
        "Helper function that adds columns relevant to a date."
        fld = df[fldname]
        fld_dtype = fld.dtype
        if isinstance(fld_dtype, pd.core.dtypes.dtypes.DatetimeTZDtype):
            fld_dtype = np.datetime64

        if not np.issubdtype(fld_dtype, np.datetime64):
            df[fldname] = fld = pd.to_datetime(fld, infer_datetime_format=True)
        targ_pre = re.sub('[Dd]ate$', '', fldname)
        attr = ['Year', 'Month', 'Week', 'Day', 'Dayofweek', 'Dayofyear',
                'Is_month_end', 'Is_month_start', 'Is_quarter_end', 'Is_quarter_start', 'Is_year_end', 'Is_year_start']
        if time: attr = attr + ['Hour', 'Minute', 'Second']
        for n in attr: df[targ_pre + n] = getattr(fld.dt, n.lower())
        df[targ_pre + 'Elapsed'] = fld.astype(np.int64) // 10 ** 9
        if drop: df.drop(fldname, axis=1, inplace=True)

def train_cats(df):
    for n,c in df.items():
        if is_string_dtype(c): df[n] = c.astype('category').cat.as_ordered()


def apply_cats(df, trn):
    for n,c in df.items():
        if trn[n].dtype.name=='category':
            df[n] = pd.Categorical(c, categories=trn[n].cat.categories, ordered=True)


def proc_df(df, y_fld, skip_flds=None, do_scale=False, max_n_cat=None):

    if not skip_flds: skip_flds=[]
    df = df.copy()
    y=df[y_fld].values
    df.drop(skip_flds + [y_fld], axis=1, inplace=True)
    for n,c in df.items(): fix_missing(df, c, n)
    for n,c in df.items(): numericalize(df, c,n, max_n_cat)
    res = [pd.get_dummies(df, dummy_na=True), y]
    return res


def fix_missing(df, col, name):
    if is_numeric_dtype(col):
        if pd.isnull(col).sum():
            df[name+'_na'] = pd.isnull(col)
        df[name] = col.fillna(col.median())

def numericalize(df, col, name, max_n_cat=None):
    if not is_numeric_dtype(col) and (max_n_cat is None or col.nunique()>max_n_cat):
        df[name] = col.cat.codes+1
