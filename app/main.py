from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import Base, engine
from routes.auth_routes import router as auth_router
from routes.predict_routes import router as predict_router
from routes.trip_routes import router as trip_router
from routes.car_routes import router as car_router
from routes.user_routes import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(car_router, prefix="/cars", tags=["Cars"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(predict_router, prefix="/predict", tags=["Prediction"])
app.include_router(trip_router, prefix="/trips", tags=["Trips"])
