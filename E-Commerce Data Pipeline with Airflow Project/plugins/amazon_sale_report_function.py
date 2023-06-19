import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# Function
## Histogram and Boxplot with Stats
def hist_boxplot(df, x, bins, title, x_label, y_label):
    fig, ax = plt.subplots(2, 1, figsize=(8, 6), gridspec_kw={'height_ratios': [3, 0.5]}, sharex=True)
    sns.histplot(df[x], ax=ax[0], kde=True, kde_kws={'bw_adjust': 4}, bins=bins)
    ax[0].set_ylabel(y_label)
    sns.boxplot(x=df[x], ax=ax[1])
    
    mean = df[x].mean()
    median = df[x].median()
    mode = df[x].mode().values[0]
    q1 = df[x].quantile(0.25)
    q3 = df[x].quantile(0.75)
    iqr = q3 - q1
    upper_limit = q3 + 1.5 * iqr
    if df['amount'].min(skipna=True) == 0:
        lower_limit = 0
    else:
        lower_limit = q1 - 1.5 * iqr

    stats_dict = {'parameter': x,
                  'mean': mean,
                  'median': median,
                  'mode': mode,
                  'q1': q1,
                  'q3': q3,
                  'upper limit': upper_limit,
                  'lower limit': lower_limit
                 }
    stats = pd.DataFrame(stats_dict, index=[0])

    for i in range(2):
        ax[i].axvline(mean, color='red', linestyle='--', label=f'Mean: {round(mean, 1)}', alpha=0.5)
        ax[i].axvline(median, color='green', linestyle='--', label=f'Median: {round(median, 1)}', alpha=0.5)
        ax[i].axvline(mode, color='blue', linestyle='--', label=f'Mode: {mode}', alpha=0.5)
        ax[i].axvline(upper_limit, color='orange', linestyle='--', label=f'Upper Limit: {round(upper_limit, 1)}', alpha=0.5)
        ax[i].axvline(lower_limit, color='purple', linestyle='--', label=f'Lower Limit: {round(lower_limit, 1)}', alpha=0.5)
    
    ax[0].legend()
    plt.suptitle(title)
    plt.xlabel(x_label)
    plt.tight_layout()

    return stats

## Split outlier from dataset function
def split_outlier(df, x):
    mean = df[x].mean()
    median = df[x].median()
    mode = df[x].mode().values[0]
    q1 = df[x].quantile(0.25)
    q3 = df[x].quantile(0.75)
    iqr = q3 - q1
    upper_limit = q3 + 1.5 * iqr
    if df['amount'].min(skipna=True) == 0:
        lower_limit = 0
    else:
        lower_limit = q1 - 1.5 * iqr

    stats_dict = {'parameter': x,
                  'mean': mean,
                  'median': median,
                  'mode': mode,
                  'q1': q1,
                  'q3': q3,
                  'upper limit': upper_limit,
                  'lower limit': lower_limit
                 }
    stats = pd.DataFrame(stats_dict, index=[0])
    
    df_nan = df[df[x].isna()==True]
    df_no_outlier = df[(df[x]<=upper_limit)]
    df_no_outlier = pd.concat([df_nan, df_no_outlier], axis=0)
    df_outlier = df[df[x]>upper_limit]

    return df_no_outlier, df_outlier, stats

## Columns name standardization
def column_standardization(df):
    columns_list = df.columns
    modified_columns_list = []
    for i in columns_list:
        modified_column = i.lower().replace(" ", "_").replace("-", "_").replace(":", "")
        modified_columns_list.append(modified_column)

    df.columns = modified_columns_list
    return df

# Nan Percentage
def nan_percentage(df):
    nan_percentage = (df.isna().sum()/len(df))*100
    return nan_percentage

# Process Column
def process_column(df, drop_columns, dropna_columns):
    df_unique = df.drop_duplicates()
    duplicate_df = len(df) - len(df_unique)
    print(f"Number of dropped duplicated df: {duplicate_df}")

    df_drop = df_unique.drop(drop_columns, axis=1)
    df_drop_na = df_drop.dropna(subset=dropna_columns)
    return df_drop_na

# Data Imputation
def data_imputation(df, x, method):
    df_imputed = df.copy()
    imputer = SimpleImputer(strategy=method)
    X = df[x].values.reshape(-1, 1)
    imputer.fit(X)
    X_imputed = imputer.transform(X)
    df_imputed[x] = X_imputed

    return df_imputed

# Data Standardization
def standardize(df, column):
    df_copy = df.copy()
    value = df[column].values.reshape(-1, 1)
    scaler = StandardScaler()
    value_scaled = scaler.fit_transform(value)
    df_copy[f'{column}_scaled'] = value_scaled
    return df_copy

# Data Categorization
def categorize_column(df, column, bins, labels, right=False):
    df_copy = df.copy()
    df_copy[f'{column}_category'] = pd.cut(df_copy[column], 
                        bins=bins, 
                        labels=labels, 
                        right=right)
    return df_copy