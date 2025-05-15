from sqlalchemy import (
    Column, Integer , String, TIMESTAMP, Text , ForeignKey , Boolean , UniqueConstraint, DateTime , DATETIME
)

from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime ,timezone


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True , index = True)
    user_licensenumber = Column(String(14), unique=True, nullable=False)
    user_fname = Column(String(25), nullable=False)
    user_lname = Column(String(25), nullable=False)
    user_phonenumber = Column(String(14), nullable=False)
    user_email = Column(String(30))

    user_password = Column(String(255))

    notifications = relationship("Notification", back_populates="user")
    ownerships = relationship("VehicleOwnership", back_populates="user")



class Vehicle(Base):
    __tablename__ = "vehicle"

    vehicle_id = Column(Integer, primary_key=True, index = True)
    vehicle_type = Column(String(25))
    vehicle_licenceplate_number = Column(String(30))

    ownerships = relationship("VehicleOwnership", back_populates="vehicle")
    violations = relationship("RuleViolation", back_populates="vehicle")


class Traffic(Base):
    __tablename__ = "trafficpersonnel"

    tp_personnelid = Column(Integer, primary_key=True, index = True)
    tp_fname = Column(String(50), nullable=False)
    tp_lname = Column(String(50), nullable=False)
    tp_phonenumber = Column(String(14), nullable=False)

    videos = relationship("Video", back_populates="uploader")


class Video(Base):
    __tablename__ = "video"

    video_id = Column(Integer, primary_key=True,index=True)
    video_path = Column(String(255))
    uploadtime_stamp = Column(TIMESTAMP)
    uploadedbyid = Column(Integer, ForeignKey("trafficpersonnel.tp_personnelid"))

    uploader = relationship("Traffic", back_populates="videos")
    violations = relationship("RuleViolation", back_populates="video")  # ✅ ADD THIS



class VehicleOwnership(Base):
    __tablename__ = "vehicleownership"

    ownership_id = Column(Integer, primary_key=True,index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicle.vehicle_id"))
    user_licensenumber = Column(String(14), ForeignKey("users.user_licensenumber"))

    vehicle = relationship("Vehicle", back_populates="ownerships")
    user = relationship("User", back_populates="ownerships")



class RuleViolation(Base):
    __tablename__ = "ruleviolation"

    violation_id = Column(Integer, primary_key=True,index=True)
    violation_type = Column(String(30))
    violation_timesstamp = Column(TIMESTAMP)
    vehicle_id = Column(Integer, ForeignKey("vehicle.vehicle_id"))
    video_id = Column(Integer, ForeignKey("video.video_id"))

    vehicle = relationship("Vehicle", back_populates="violations")
    video = relationship("Video", back_populates="violations")
    notifications = relationship("Notification", back_populates="violation")

class Notification(Base):
    __tablename__ = "notification"

    notification_id = Column(Integer, primary_key=True, index=True)
    notification_message = Column(Text, nullable=False)
    notification_senttimestamp = Column(TIMESTAMP)
    notification_status = Column(String(20), nullable=False)
    violation_id = Column(Integer, ForeignKey("ruleviolation.violation_id"))
    user_licensenumber = Column(String(14), ForeignKey("users.user_licensenumber"), nullable=False)

    user = relationship("User", back_populates="notifications")
    violation = relationship("RuleViolation", back_populates="notifications")




