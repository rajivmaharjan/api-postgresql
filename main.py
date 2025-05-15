from fastapi import FastAPI 
from sqlalchemy.ext.asyncio import async_sessionmaker
from crud import CRUD
from db import engine 
from typing import List
from models import User , Vehicle ,Traffic ,Video , VehicleOwnership , RuleViolation , Notification
from http import HTTPStatus
from fastapi import HTTPException

from fastapi import WebSocket , WebSocketDisconnect , Depends
from typing import Dict



from schemas import UserCreate
from schemas import UserLogin
from schemas import   VehicleCreate ,TrafficRegister ,VideoUpload , OwnershipRegister , RegisterRuleViolation , NotificationSystem


import schemas,models


app = FastAPI(
    #swagger UI
    title = "Noted API",
    description= "This is a simple note taking service",
    docs_url="/"
)

session = async_sessionmaker(
    bind = engine,
    expire_on_commit= False
)

db = CRUD()







@app.post('/register/',status_code=HTTPStatus.CREATED)
async def create_user(user_data: UserCreate):
    new_user = User(
        user_licensenumber=user_data.user_licensenumber,
        user_fname=user_data.user_fname,
        user_lname=user_data.user_lname,
        user_phonenumber=user_data.user_phonenumber,
        user_email=user_data.user_email,
        user_password=user_data.user_password
    )
    user = await db.add_user(session,new_user)

    return user

@app.post("/login",status_code=HTTPStatus.CREATED)
async def login_user(user: UserLogin):
    db_user = await db.authenticate_user(session, user.user_licensenumber, user.user_password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid license number or password")

    return {
        "message": "Login successful",
        "user_fname": db_user.user_fname,
        "user_email": db_user.user_email,
        "user_license": db_user.user_licensenumber
    }



#Create Vehicle
@app.post("/vehicle/",status_code=HTTPStatus.CREATED)
async def create_vehicle(vechile_data: VehicleCreate):
    new_vehicle = Vehicle(
        vehicle_type = vechile_data.vehicle_type,
        vehicle_licenceplate_number = vechile_data.vehicle_licenceplate_number
    )
    vehicle = await db.register_vehicle(session,new_vehicle)

    return vehicle


@app.post("/trafficpersonnel/",status_code=HTTPStatus.CREATED)
async def create_traffic(traffic_data: TrafficRegister):
    new_traffic = Traffic(
        tp_fname =  traffic_data.tp_fname,
        tp_lname = traffic_data.tp_lname,
        tp_phonenumber = traffic_data.tp_phonenumber
    )
    traffic = await db.register_traffic(session,new_traffic)

    return traffic


@app.post("/uploadvideo/",status_code=HTTPStatus.CREATED)
async def upload_video(video_data: VideoUpload):
    naive_upload_time = video_data.uploadtime_stamp.replace(tzinfo=None)

    new_video = Video(
        video_path=video_data.video_path,
        uploadtime_stamp=naive_upload_time,
        uploadedbyid=video_data.uploadedbyID
    )
    video = await db.upload_video(session,new_video)

    return video



@app.post("/registerowner/",status_code=HTTPStatus.CREATED)
async def register_owner(owner_data: OwnershipRegister):


    new_owner = VehicleOwnership(
                vehicle_id = owner_data.vehicle_id,
                user_licensenumber = owner_data.user_licensennumber
    )
    owner = await db.upload_video(session,new_owner)

    return owner



@app.post("/ruleviolation/",status_code=HTTPStatus.CREATED)
async def register_ruleviolation(violation_data: RegisterRuleViolation):

    naive_violation_time = violation_data.violation_timesstamp.replace(tzinfo=None)
    new_violation = RuleViolation(
        violation_type = violation_data.violation_type,
        violation_timesstamp = naive_violation_time,
        vehicle_id = violation_data.vehicle_id,
        video_id = violation_data.video_id

    )
    violation = await db.register_ruleviolation(session,new_violation)

    return violation


@app.post("/notification/",status_code=HTTPStatus.CREATED)
async def log_notification(notification_data: NotificationSystem):

    naive_notification_time = notification_data.notification_senttimestamp.replace(tzinfo=None)
    new_notification = Notification(
        notification_message = notification_data.notification_message,
        notification_senttimestamp = naive_notification_time,
        notification_status = notification_data.notification_status,
        violation_id = notification_data.violation_id,
        user_licensenumber = notification_data.user_licensenumber

    )
    notification = await db.register_ruleviolation(session,new_notification)

    return notification













