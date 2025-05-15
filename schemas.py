from pydantic import BaseModel , ConfigDict
from datetime import datetime
from typing  import Optional




class UserCreate(BaseModel):
    user_licensenumber: str
    user_fname: str
    user_lname: str
    user_phonenumber: str
    user_email: Optional[str]
    user_password: Optional[str]


class UserLogin(BaseModel):
    user_licensenumber: str
    user_password: str



class NotificationBase(BaseModel):
    notification_message: str
    notification_senttimestamp: datetime
    notification_status: str
    violation_id: int
    licence_number: str


#class NotificationCreate(NotificationBase):
   # pass



class VehicleCreate(BaseModel):
    vehicle_type: str
    vehicle_licenceplate_number: str



class TrafficRegister(BaseModel):
    tp_fname: str
    tp_lname:str
    tp_phonenumber:str


class VideoUpload(BaseModel):
    video_path:str
    uploadtime_stamp: Optional[datetime]
    uploadedbyID: int

class OwnershipRegister(BaseModel):
    vehicle_id: int
    user_licensennumber: str


class RegisterRuleViolation(BaseModel):
    violation_type: str
    violation_timesstamp: Optional[datetime]
    vehicle_id: int
    video_id: int



class NotificationSystem(BaseModel):
    notification_message: str
    notification_senttimestamp: datetime
    notification_status: str
    violation_id: int
    user_licensenumber : str