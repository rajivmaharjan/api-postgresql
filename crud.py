from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from models import User , Vehicle , Traffic ,Video ,VehicleOwnership , RuleViolation , Notification
from sqlalchemy.future import select
from datetime import datetime, timezone





class CRUD:
    
    async def add_user(self, async_session: async_sessionmaker[AsyncSession], user: User):
        async with async_session() as session:
            session.add(user)
            await session.commit()
        return user
    
    async def authenticate_user(self,async_session: async_sessionmaker[AsyncSession], license_number: str, password: str):
        async with async_session() as session:
            result = await session.execute(
                select(User).where(User.user_licensenumber == license_number)
            )
            user = result.scalars().first()

            if not user:
                return None
            if user.user_password != password:
                return None
            return user
        


    async def register_vehicle(self,async_session:async_sessionmaker[AsyncSession],vehicle:Vehicle):
        async with async_session() as session:
            session.add(vehicle)
            await session.commit()

    async def register_traffic(self,async_session:async_sessionmaker[AsyncSession],traffic_personnel:Traffic):
        async with async_session() as session:
            session.add(traffic_personnel)
            await session.commit()

    async def upload_video(self,async_session:async_sessionmaker[AsyncSession],upload_video:Video):
        async with async_session() as session:
            session.add(upload_video)
            await session.commit()

    async def register_owner(self,async_session:async_sessionmaker[AsyncSession],register_owner:VehicleOwnership):
        async with async_session() as session:
            session.add(register_owner)
            await session.commit()

    async def register_ruleviolation(self,async_session:async_sessionmaker[AsyncSession],register_violation:RuleViolation):
        async with async_session() as session:
            session.add(register_violation)
            await session.commit()


    async def notification(self,async_session:async_sessionmaker[AsyncSession],log_notification:Notification):
        async with async_session() as session:
            session.add(log_notification)
            
            await session.commit()

    async def get_notification(self,async_session:async_sessionmaker[AsyncSession],notification_user_licensenumber:str):
        async with async_session() as session:
            statement = select(Notification).filter(Notification.user_licensenumber == notification_user_licensenumber)

            result = await session.execute(statement)

            return result.scalars().one()