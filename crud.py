from sqlalchemy.orm import Session

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hash_pass = user.password + "hash"
    db_user = models.User(first_name=user.first_name,
                          username=user.username,
                          address=user.address,
                          gov_id=user.gov_id,
                          email=user.email, 
                          hashed_password=fake_hash_pass,
                          middle_name=user.middle_name,
                          phone_number=user.phone_number)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_vehicles(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Vehicle).offset(skip).limit(limit).all()


def add_vehicle_for_user(db: Session, vehicle: schemas.VehicleCreate, user_id: int):
    db_vehicle = models.Vehicle(**vehicle.model_dump(), driver_id=user_id)
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


def get_appointments(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Appointment).offset(skip).limit(limit).all()


def get_services(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Service).offset(skip).limit(limit).all()


def create_service(db: Session, service: schemas.ServiceCreate):
    db_service = models.Service(name=service.name,
                                description=service.description,
                                price=service.price)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def create_appointment_for_user(db: Session, appointment: schemas.AppointmentCreate, 
                                user_id: int, service: schemas.ServiceCreate):  
    db_service = create_service(db, service)  
    
    db_appointment = models.Appointment(user_id=user_id,
                                        service_id=db_service.id,
                                        appointment_date=appointment.appointment_date,
                                        status=appointment.status)

    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment



def create_roles():
    pass