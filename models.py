from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    gov_id = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    phone_number = Column(String, unique=True, nullable=False)
    driving_license_code = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)

    # registration_date, last_login, created_at, updated_at
  #  role_type = Column(String, ForeignKey("roles.role_type"))  # TODO

    appointments = relationship("Appointment", back_populates="user")
  #  role = relationship("Role", back_populates="users")
    vehicles = relationship("Vehicle", back_populates="driver") 



class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer)
    license_plate = Column(String, unique=True, index=True, nullable=False)
    sitting_capacity = Column(Integer, default=5)
    type = Column(String)
    color = Column(String)
    VIN = Column(String, unique=True, nullable=False, index=True)
    current_mileage = Column(Integer)
    # last_maintenance_date = Column(String), registration date
    next_scheduled_maintenance_mileage = Column(Integer)
    status = Column(String)
    note = Column(String)

    driver_id = Column(Integer, ForeignKey("users.id"))

    driver = relationship("User", back_populates="vehicles")


# class Role(Base): # no primary key?
#     __tablename__ = "roles"
    
#     id = Column(Integer, primary_key=True, unique=True)
#     role_type = Column(String, index=True)
#     can_access_car_info = Column(Boolean)
#     can_view_own_profile = Column(Boolean)
#     can_view_driving_history = Column(Boolean)
#     can_manage_users = Column(Boolean)
#     can_view_fueling_info = Column(Boolean)
#     can_update_maintenance_details = Column(Boolean)
#     can_search_by_license_plate = Column(Boolean)
#     can_create_auction_vehicles = Column(Boolean)
#     can_view_auction_page = Column(Boolean)
#     can_edit_route_details = Column(Boolean)
#     can_assign_vehicle_to_driver = Column(Boolean)
#     can_assign_task_to_driver = Column(Boolean)
#     can_generate_reports = Column(Boolean)

#     users = relationship("User", back_populates="role")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, unique=True, index=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    appointment_date = Column(String)
    status = Column(String)

    user = relationship("User", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, unique=True, index=True, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer)

    appointments = relationship("Appointment", back_populates="service")

