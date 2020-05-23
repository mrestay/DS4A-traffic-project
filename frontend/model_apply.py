import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, cohen_kappa_score, classification_report , roc_curve, roc_auc_score, average_precision_score
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
import xgboost
from sklearn.compose import ColumnTransformer

location_frontend = ['x', 'y']
datetime_frontend = ['time']
cols_to_keep_weather = [
       'precipIntensity', 'precipProbability', 'temperature',
       'dewPoint', 'humidity', 'windSpeed',
       'cloudCover', 'uvIndex', 'visibility']
cols_to_keep = location_frontend + datetime_frontend + cols_to_keep_weather
numerical_cols_weather = ['temperature',
       'dewPoint', 'humidity', 'windSpeed',
       'cloudCover', 'uvIndex', 'visibility']
numerical_cols = location_frontend + numerical_cols_weather

#Custom Transformer that extracts columns passed as argument to its constructor
class FeatureSelector( BaseEstimator, TransformerMixin ):
    #Class Constructor
    def __init__( self, feature_names ):
        self._feature_names = feature_names

    #Return self nothing else to do here
    def fit( self, X, y = None ):
        return self

    #Method that describes what we need this transformer to do
    def transform( self, X, y = None ):
        return X.loc[:,self._feature_names ]

#Custom Transformer that extracts columns passed as argument to its constructor
class IntensityProba( BaseEstimator, TransformerMixin ):
    #Class Constructor
    def __init__( self, column_intensity, column_probability ):
        self.column_intensity = column_intensity
        self.column_probability = column_probability

    #Return self nothing else to do here
    def fit( self, X, y = None ):

        return self

    #Method that describes what we need this transformer to do
    def transform( self, X, y = None ):
        X.loc[:,'precip_intensity_probability'] = X[self.column_intensity] * X[self.column_probability]
        return X.drop([self.column_intensity, self.column_probability], axis=1)

#Custom Transformer that extracts columns passed as argument to its constructor
class CyclicalGenerator( BaseEstimator, TransformerMixin ):
    #Class Constructor
    def __init__( self, column, period ):
        self.column = column
        self.period = period

    #Return self nothing else to do here
    def fit( self, X, y = None ):

        return self

    #Method that describes what we need this transformer to do
    def transform( self, X, y = None ):
        if X[self.column].min() != 0:
            X.loc[:,f'{self.column}_sin'] = np.sin((X[self.column] - 1)*(2.*np.pi/self.period))
            X.loc[:,f'{self.column}_cos'] = np.cos((X[self.column] - 1)*(2.*np.pi/self.period))
        else:
            X.loc[:,f'{self.column}_sin'] = np.sin((X[self.column])*(2.*np.pi/self.period))
            X.loc[:,f'{self.column}_cos'] = np.cos((X[self.column])*(2.*np.pi/self.period))

        return X.drop(self.column, axis=1)

class ExtractDateParts( BaseEstimator, TransformerMixin ):
    #Class Constructor
    def __init__( self, datime_column):
        self.datime_column = datime_column

    #Return self nothing else to do here
    def fit( self, X, y = None ):

        return self

    #Method that describes what we need this transformer to do
    def transform( self, X, y = None ):
        X.loc[:,'day_of_year'] = pd.to_datetime(X[self.datime_column]).dt.dayofyear
        X.loc[:,'day_of_week'] = pd.to_datetime(X[self.datime_column]).dt.dayofweek
        X.loc[:,'month'] = pd.to_datetime(X[self.datime_column]).dt.month
        X.loc[:,'hour'] = pd.to_datetime(X[self.datime_column]).dt.hour

        return   X.drop(self.datime_column, axis=1)

minmax_transformer = Pipeline(steps=[
        ('minmax', MinMaxScaler())])

preprocessor = ColumnTransformer(
        remainder='passthrough', #passthough features not listed
        transformers=[
            ('scaler', minmax_transformer , numerical_cols),
        ])

full_pipeline = Pipeline([
    ('preprocess', pipeline_preprocess),
    ('scaler', preprocessor),
])

    pipeline_preprocess = Pipeline([
    ('select_cols', FeatureSelector(cols_to_keep)),
    ('date_parts', ExtractDateParts('timestamp')),
    ('cyclical_hour', CyclicalGenerator('hour', 24)),
    ('cyclical_dow', CyclicalGenerator('day_of_week', 7)),
    ('cyclical_month', CyclicalGenerator('month', 12)),
    ('cyclical_doy', CyclicalGenerator('day_of_year', 365) ),
    ('intesity_proba', IntensityProba('precipIntensity', 'precipProbability')),
    ])




def model_apply(data, filename):

    data_prepared = full_pipeline.fit_transform(data)

    model = joblib.load(filename)

    return model.predict_proba(data_prepared)[:,1]
