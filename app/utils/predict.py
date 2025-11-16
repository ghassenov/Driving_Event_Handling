import numpy as np
import joblib

model = joblib.load("trained_models/harsh_driving_rf_model.pkl")

def predict_trip(trip):
    rows = []
    for s in trip.sensors:
        acc_mag = np.sqrt(s.acc_x**2 + s.acc_y**2 + s.acc_z**2)
        gyro_mag = np.sqrt(s.gyro_x**2 + s.gyro_y**2 + s.gyro_z**2)
        mag_mag = np.sqrt(s.mag_x**2 + s.mag_y**2 + s.mag_z**2)

        rows.append([
            s.acc_x, s.acc_y, s.acc_z,
            s.gyro_x, s.gyro_y, s.gyro_z,
            s.mag_x, s.mag_y, s.mag_z,
            acc_mag, gyro_mag, mag_mag
        ])

    X = np.array(rows)
    events = model.predict(X).tolist()
    harsh_events = sum(events)
    score = max(0, 100 - harsh_events * 10)

    return score, events
