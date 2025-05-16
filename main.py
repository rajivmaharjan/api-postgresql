from fastapi import FastAPI 
from sqlalchemy.ext.asyncio import async_sessionmaker
from crud import CRUD
from db import engine 
from models import User , Vehicle ,Traffic ,Video , VehicleOwnership , RuleViolation , Notification
from http import HTTPStatus
from fastapi import HTTPException # for websockets
from schemas import UserCreate, UserLogin, VehicleCreate ,TrafficRegister ,VideoUpload , OwnershipRegister , RegisterRuleViolation , NotificationSystem

#web sockets
from fastapi import WebSocket,WebSocketDisconnect
from typing import List, Dict

from fastapi.middleware.cors import CORSMiddleware
from ws_manager import endpoints as websocket_routes
from ws_manager.websocket_manager import send_notification_to_user
from fastapi import BackgroundTasks

from ws_manager.websocket_manager import connect_user,disconnect_user





app = FastAPI(
    #swagger UI
    title = "API for Rule Violation",
    description= "This is a simple rule vioaltion APIS ",
    docs_url="/"
)

session = async_sessionmaker(
    bind = engine,
    expire_on_commit= False
)

db = CRUD()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

active_connections: Dict[str,WebSocket] ={}

app.include_router(websocket_routes.router)


@app.websocket("/ws/notifications/{license_number}")
async def websocket_endpoint(websocket: WebSocket, license_number: str):
    await connect_user(license_number,websocket)

    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received from {license_number}: {data}")
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print(f"Client disconnected: {license_number}")
        disconnect_user(license_number)

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
async def log_notification(notification_data: NotificationSystem,background_task:BackgroundTasks):

    naive_notification_time = notification_data.notification_senttimestamp.replace(tzinfo=None)
    new_notification = Notification(
        notification_message = notification_data.notification_message,
        notification_senttimestamp = naive_notification_time,
        notification_status = notification_data.notification_status,
        violation_id = notification_data.violation_id,
        user_licensenumber = notification_data.user_licensenumber

    )
    
    notification = await db.register_ruleviolation(session,new_notification)
    background_task.add_task(send_notification_to_user,notification_data.user_licensenumber,notification_data.notification_message)
    return notification

@app.get("/notification/{licensenumber}")
async def get_notification_by_licencenumber(licensenumber):
    notification = await db.get_notification(session,licensenumber)
    

    return notification














'''@app.websocket("/ws/notifications/{license_number}")
async def websocket_endpoint(websocket: WebSocket, license_number: str):
    await websocket.accept()
    active_connections[license_number] = websocket
    print(f"Client connected: {license_number}")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received from {license_number}: {data}")

            # Optionally echo or broadcast to this specific license
            await websocket.send_text(f"Echo: {data}")

    except WebSocketDisconnect:
        print(f"Client disconnected: {license_number}")
        # Safely remove the disconnected websocket
        active_connections.pop(license_number, None)
'''