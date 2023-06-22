import pandas as pd
# from sklearn.impute import SimpleImputer
# from sklearn.preprocessing import StandardScaler

# Function
## Histogram and Boxplot with Stats
class F:
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