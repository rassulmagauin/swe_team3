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


# CREATE for users
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# READ for users
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


# READ by ID for users
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# UPDATE for users
@app.put("/users/{user_id}/update", response_model=schemas.User)
def update_user_by_id(user: schemas.UserUpdate, user_id: int, db: Session = Depends(get_db)):
    return crud.update_user(user_id=user_id, user=user, db=db)


# DELETE for users


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


@app.post("/service/", response_model=schemas.Service)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    db_service = crud.create_service(db, service=service)
    return db_service


@app.put("/services/{service_id}/update", response_model=schemas.Service)
def update_service_by_id(service: schemas.ServiceCreate, service_id: int, db: Session = Depends(get_db)):
    return crud.update_service(service_id=service_id, updated_service=service, db=db)


@app.post("/roles/", response_model=schemas.Role)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    db_role = crud.get_role_by_type(db, role_type=role.role_type)
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")
    return crud.create_role(db=db, role=role)


@app.get("/roles/", response_model=list[schemas.Role])
def get_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    roles = crud.get_roles(db, skip=skip, limit=limit)
    return roles


@app.post("/role/{role_type}/user/", response_model=schemas.User)
def add_role_to_user(
    role_type: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.assign_role_to_user(db=db, user=user, role_type=role_type)

