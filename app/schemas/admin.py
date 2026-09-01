from pydantic import BaseModel, ConfigDict, Field
from typing import List
from datetime import datetime
from app.schemas.base import BaseResponse, Meta

from app.enums.admin_enums import BusFilterStatus


class BusCreateSchema(BaseModel):
    name: str|None = Field(None, description="Bus name")
    registration_number: str|None = Field(None, description="Bus registration number")
    capacity: int|None = Field(None, description="Bus capacity")
    route_id: int|None = Field(None, description="Route id")
    is_active: bool|None = Field(None, description="Bus active or not")

class BusFilterSchema(BaseModel):
    status: BusFilterStatus | None = Field(None, description="Bus status")
    route_id: int|None = Field(None, description="Route id")

class CurrentLocationSchema(BaseModel):
    latitude: float = Field(..., description="Current latitude")
    longitude: float = Field(..., description="Current longitude")

class BusDetailsSchema(BaseModel):
    id: int = Field(..., description="Bus id")
    name: str = Field(..., description="Bus name")
    registration_number: str|None = Field(None, description="Bus registration number")
    capacity: int|None = Field(None, description="Bus capacity")
    route_id: int|None = Field(None, description="Route id")
    is_active: bool|None = Field(None, description="Bus active or not")
    is_running: bool|None = Field(None, description="Bus running or not")
    current_location: CurrentLocationSchema|None = Field(None, description="Current location")


# =============================================================================
#                             Stop Management
# =============================================================================
class StopCreateSchema(BaseModel):
    name: str = Field(None, description="Stop name")
    lattitude: float = Field(None, description="Stop lattitude")
    longitude: float = Field(None, description="Stop longitude")
    is_active: bool = Field(None, description="Stop active or not")


class StopListFileterSchema(BaseModel):
    route_id: int | None = Field(None, description="Route id")
    is_active: bool = Field(True, description="Stop active or not")

    sort_by: str = Field(None, description="Sort by")
    sort_order: str = Field(None, description="Sort order")
    page: int = Field(1, description="Page number")
    per_page: int = Field(20, description="Number of items per page")

# =============================================================================
#                             Route Management
# =============================================================================
class RouteStopCreateSchema(BaseModel):
    stop_id: int = Field(None, description="Stop id")
    stop_order: int = Field(None, description="Stop order")

class RouteCreateSchema(BaseModel):
    name: str = Field(None, description="Route name")
    code: str = Field(None, description="Route code")
    description: str = Field(None, description="Route description")
    is_active: bool = Field(True, description="Route active or not")
    stop_ids: list[RouteStopCreateSchema] = Field(None, description="Stop ids with order")

class RouteListFileterSchema(BaseModel):
    name: str|None = Field(None, description="Route name")
    is_active: bool|None = Field(True, description="Route active or not")
    search: str|None = Field(None, description="Search")
    sort_by: str|None = Field(None, description="Sort by")
    sort_order: str|None = Field(None, description="Sort order")
    

# =============================================================================
#                             Driver Management
# =============================================================================
class DriverDetailsSchema(BaseModel):
    id: int = Field(..., description="Driver id")
    username: str|None = Field(None, description="Driver username")
    full_name: str|None = Field(None, description="Driver full name")
    status: str|None = Field(None, description="Driver status")
    address: str|None = Field(None, description="Driver address")
    license_plate: str|None = Field(None, description="Driver license plate")
    license_plate_expiry: datetime|None = Field(None, description="Driver license plate expiry")
    total_triped: int|None = Field(None, description="Driver total triped")
    joining_date: datetime|None = Field(None, description="Driver joining date")
    emergency_contact_name: str|None = Field(None, description="Driver emergency contact name")
    emergency_contact_phone: str|None = Field(None, description="Driver emergency contact phone")
    current_status: str|None = Field(None, description="Driver current status")



# =============================================================================
#                             Trip Management
# =============================================================================
class TripDetailsSchema(BaseModel):
    id: int = Field(..., description="Trip id")
    bus_id: int = Field(..., description="Trip bus id")
    route_id: int = Field(..., description="Trip route id")
    device_id: str = Field(..., description="Trip device id")
    app_version: str = Field(..., description="Trip app version")
    started_at: str = Field(..., description="Trip started at")
    ended_at: str = Field(None, description="Trip ended at")
    status: str = Field(..., description="Trip status")

    current_location: CurrentLocationSchema = Field(None, description="Current location")
    driver: DriverDetailsSchema = Field(None, description="Driver details")