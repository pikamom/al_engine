import logging

import numpy as np
from sklearn.metrics import r2_score

logger = logging.getLogger("al_engine")


def calculate_performance_metrics(actual, predicted):
    mse = np.mean((actual - predicted) ** 2)
    rmse = np.sqrt(mse)
    absolute_errors = np.abs(actual - predicted)
    mae = np.mean(absolute_errors)
    r2 = r2_score(actual, predicted)

    metrics = {"MSE": mse, "RMSE": rmse, "MAE": mae, "R2": r2}
    logger.info(f"Calcualted Metrics are: [{metrics}]")

    return metrics
