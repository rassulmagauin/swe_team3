from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Title", description="descr", docs_url="/")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/vehicles/", response_model=schemas.Vehicle)
def add_vehicles_for_user(
    user_id: int, vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    return crud.add_vehicle_for_user(db=db, vehicle=vehicle, user_id=user_id)


@app.get("/vehicles/", response_model=list[schemas.Vehicle])
def get_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vehicles = crud.get_vehicles(db, skip=skip, limit=limit)
    return vehicles


@app.post("/users/{user_id}/appointment/", response_model=schemas.Appointment)
def create_appointment_for_user(
    user_id: int, appointment: schemas.AppointmentCreate,
    service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    return crud.create_appointment_for_user(db=db, appointment=appointment, user_id=user_id, service=service)


@app.get("/appointments/", response_model=list[schemas.Appointment])
def get_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    appointments = crud.get_appointments(db, skip=skip, limit=limit)
    return appointments


@app.get("/services/", response_model=list[schemas.Service])
def get_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    services = crud.get_services(db, skip=skip, limit=limit)
    return services