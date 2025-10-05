from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional, List
from passlib.context import CryptContext


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return password_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


# Users
def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        username=user.username,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Food Logs
def create_user_food_log(db: Session, food_log: schemas.FoodLogCreate, user_id: int) -> models.FoodLog:
    db_log = models.FoodLog(
        owner_id=user_id,
        food_name=food_log.food_name,
        calories=food_log.calories,
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def get_food_logs_by_user(db: Session, user_id: int) -> List[models.FoodLog]:
    return (
        db.query(models.FoodLog)
        .filter(models.FoodLog.owner_id == user_id)
        .order_by(models.FoodLog.timestamp.desc())
        .all()
    )



