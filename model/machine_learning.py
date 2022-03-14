import xgboost as xgb
import pathlib

filename = "model/model.json" # pathlib.Path(__file__).resolve().parent.joinpath("model.json").resolve()

def load_model():
    model = xgb.XGBRegressor()
    model.load_model(filename)

    return model

def handle_unique(df, target="Z-AxisAgle(Azimuth)", categorical=["timestamp"]):
    yval = df[target]
    df2 = df.drop([target]+categorical, axis=1)
    
    return df2, yval


def predict(model, df):
    """Predict using the machine learning model
    Args:
        - model (xgb boost model)
        - df (dataframe with features)
    """

    xtest, yval = handle_unique(df)
    ypred = model.predict(xtest)

    return yval, ypred
