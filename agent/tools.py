# tools.py
from typing import Dict
import joblib
import numpy as np
import pandas as pd

# Load your trained model
MODEL_PATH = "trained_models/xgboost_fuel_model.pkl"
model = joblib.load(MODEL_PATH)

def create_features(speed: float, acceleration: float, engine_rpm: float, 
                   vehicle_weight: float, temp: float) -> np.ndarray:
    """
    Create all 34 features that the model expects.
    This replicates the feature engineering from your notebook.
    """
    # Create a DataFrame with the input
    df = pd.DataFrame({
        'speed': [speed],
        'acceleration': [acceleration],
        'engineRPM': [engine_rpm],
        'MAF': [50.0],  # Default value - you may need to calculate this
        'absoluteLoad': [40.0],  # Default value
        'fuelConsumption': [0.0],  # Placeholder
        'temp': [temp],
        'vehicle_weight': [vehicle_weight]
    })
    
    # === FEATURE ENGINEERING (matching your notebook) ===
    
    # 1. Speed categories
    df['speed_cat_low'] = (df['speed'] < 40).astype(int)
    df['speed_cat_medium'] = ((df['speed'] >= 40) & (df['speed'] < 80)).astype(int)
    df['speed_cat_high'] = (df['speed'] >= 80).astype(int)
    
    # 2. RPM categories
    df['rpm_cat_low'] = (df['engineRPM'] < 1500).astype(int)
    df['rpm_cat_medium'] = ((df['engineRPM'] >= 1500) & (df['engineRPM'] < 3000)).astype(int)
    df['rpm_cat_high'] = (df['engineRPM'] >= 3000).astype(int)
    
    # 3. Interaction features
    df['speed_rpm_ratio'] = df['speed'] / (df['engineRPM'] + 1)
    df['speed_load_interaction'] = df['speed'] * df['absoluteLoad']
    df['rpm_load_interaction'] = df['engineRPM'] * df['absoluteLoad']
    df['acceleration_load'] = df['acceleration'] * df['absoluteLoad']
    
    # 4. Power estimation
    df['power_estimate'] = (df['engineRPM'] * df['absoluteLoad']) / 1000
    
    # 5. Efficiency metrics
    df['efficiency_metric'] = df['speed'] / (df['MAF'] + 1)
    
    # 6. Temperature effects
    df['temp_load_interaction'] = df['temp'] * df['absoluteLoad']
    
    # 7. Boolean flags
    df['is_idling'] = ((df['speed'] < 5) & (df['engineRPM'] < 1000)).astype(int)
    df['is_accelerating'] = (df['acceleration'] > 0.5).astype(int)
    df['is_decelerating'] = (df['acceleration'] < -0.5).astype(int)
    df['is_cruising'] = ((df['acceleration'].abs() < 0.5) & (df['speed'] > 20)).astype(int)
    
    # 8. Weight-based features
    df['weight_speed_ratio'] = df['vehicle_weight'] / (df['speed'] + 1)
    df['weight_acceleration'] = df['vehicle_weight'] * df['acceleration'].abs()
    
    # 9. Rolling statistics (use default values for single prediction)
    # These would normally be calculated from previous readings
    df['speed_rolling_mean_5'] = df['speed']  # Use current value as default
    df['speed_rolling_std_5'] = 0.0  # No variance for single reading
    df['rpm_rolling_mean_5'] = df['engineRPM']
    df['rpm_rolling_std_5'] = 0.0
    df['acceleration_rolling_mean_5'] = df['acceleration']
    df['load_rolling_mean_5'] = df['absoluteLoad']
    
    # 10. Squared features for non-linear relationships
    df['speed_squared'] = df['speed'] ** 2
    df['rpm_squared'] = df['engineRPM'] ** 2
    

    feature_columns = [
        'speed', 'acceleration', 'engineRPM', 'MAF', 'absoluteLoad', 'temp', 'vehicle_weight',
        'speed_cat_low', 'speed_cat_medium', 'speed_cat_high',
        'rpm_cat_low', 'rpm_cat_medium', 'rpm_cat_high',
        'speed_rpm_ratio', 'speed_load_interaction', 'rpm_load_interaction', 'acceleration_load',
        'power_estimate', 'efficiency_metric', 'temp_load_interaction',
        'is_idling', 'is_accelerating', 'is_decelerating', 'is_cruising',
        'weight_speed_ratio', 'weight_acceleration',
        'speed_rolling_mean_5', 'speed_rolling_std_5', 'rpm_rolling_mean_5', 'rpm_rolling_std_5',
        'acceleration_rolling_mean_5', 'load_rolling_mean_5',
        'speed_squared', 'rpm_squared'
    ]
    
    return df[feature_columns].values


def predict_fuel_tool(
    speed: float,
    acceleration: float,
    engine_rpm: float,
    vehicle_weight: float,
    temp: float
) -> Dict:
    """
    Predicts fuel consumption using the ML model.

    Inputs:
        speed (float): km/h
        acceleration (float): m/s²
        engine_rpm (float)
        vehicle_weight (float): kg
        temp (float): °C

    Output:
        {"fuel_consumption": value in L/100km}
    """
    try:
        # Create all 34 features
        X = create_features(speed, acceleration, engine_rpm, vehicle_weight, temp)
        
        # Make prediction
        prediction = float(model.predict(X)[0])
        
        # Apply realistic bounds (based on your notebook analysis)
        prediction = np.clip(prediction, 0.5, 50.0)
        
        return {"fuel_consumption": round(prediction, 2)}
    
    except Exception as e:
        print(f"[ERROR] Prediction failed: {e}")
        return {"fuel_consumption": None, "error": str(e)}
