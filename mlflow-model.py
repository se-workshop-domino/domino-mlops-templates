from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    data["data"], data["target"], test_size=0.2
)

from domino_data.training_sets import client, model
import pandas as pd

target_column_name = "variety"

training_df = pd.DataFrame(data=X_train, columns=data.feature_names)
training_df[target_column_name] = [data.target_names[y] for y in y_train]

tsv = client.create_training_set_version(
    training_set_name="iris_python_classification",
    df=training_df,
    key_columns=[],
    target_columns=[target_column_name],
    exclude_columns=[],
    meta={"experiment_id": "0.1"},
    monitoring_meta=model.MonitoringMeta(
        **{
            "categorical_columns": [target_column_name],
            "timestamp_columns": [],
            "ordinal_columns": [],
        }
    ),
)

print(f"TrainingSetVersion {tsv.training_set_name}:{tsv.number}")

from xgboost import XGBClassifier
from domino_data_capture.data_capture_client import DataCaptureClient
import uuid
import datetime

xgb_classifier = XGBClassifier(
    n_estimators=10,
    max_depth=3,
    learning_rate=1,
    objective="binary:logistic",
    random_state=123,
)

# train model
xgb_classifier.fit(X_train, y_train)

data_capture_client = DataCaptureClient(data.feature_names, [target_column_name])


class IrisModel(mlflow.pyfunc.PythonModel):
    def __init__(self, model):
        self.model = model

    def predict(self, context, model_input, params=None):
        event_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
        prediction = self.model.predict(model_input)

        for i in range(len(prediction)):
            # Record eventID and current time
            event_id = uuid.uuid4()
            # Convert np types to python builtin type to allow JSON serialization by prediction capture library
            model_input_value = [float(x) for x in model_input[i]]
            prediction_value = [data.target_names[prediction[i]]]

            # Capture this prediction event so Domino can keep track
            data_capture_client.capturePrediction(
                model_input_value,
                prediction_value,
                event_id=event_id,
                timestamp=event_time,
            )
        return prediction


model = IrisModel(xgb_classifier)

with mlflow.start_run() as run:
    model_info = mlflow.pyfunc.log_model(
        registered_model_name="pyfunc-xgboost-model",  # important,
        python_model=model,
        artifact_path="test-model",
    )
print(model_info)
