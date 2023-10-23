from pydantic import BaseModel


class VehicleBase(BaseModel):
    make: str
    model: str
    year: int
    type: str
    VIN: str
    color: str
    current_mileage: int | None = None



class VehicleCreate(VehicleBase):
    license_plate: str


class Vehicle(VehicleBase):
    id: int
    driver_id: int
    type: str
    

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    username: str
    address: str
    gov_id: str


class UserCreate(UserBase):
    first_name: str
    middle_name: str
    last_name: str
    phone_number: str
    password: str


class User(UserBase):
    id: int
    is_active: bool
    driving_license_code: str | None = None
    vehicles: list[Vehicle] = []

    class Config:
        orm_mode = True



class RoleBase(BaseModel):
    pass


class RoleCreate(RoleBase):
    role_type: str
    can_access_car_info: bool
    can_view_own_profile: bool
    can_view_driving_history: bool
    can_manage_users: bool
    can_view_fueling_info: bool
    can_update_maintenance_details: bool
    can_search_by_license_plate: bool
    can_create_auction_vehicles: bool
    can_view_auction_page: bool
    can_edit_route_details: bool
    can_assign_vehicle_to_driver: bool
    can_assign_task_to_driver: bool
    can_generate_reports: bool


class Role(RoleCreate):
    id: int

    users: list[User] = []

    class Config:
        orm_mode = True
    

class AppointmentBase(BaseModel):
    status: str


class AppointmentCreate(AppointmentBase):
    appointment_date: str


class Appointment(AppointmentBase):
    id: int
    user_id: int
    service_id: int

    class Config:
        orm_mode = True


class ServiceBase(BaseModel):
    name: str
    description: str
    price: int


class ServiceCreate(ServiceBase):
    pass


class Service(ServiceBase):
    id: int
    appointments: list[Appointment] = []

    class Config:
        orm_mode = True
