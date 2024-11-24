from sqlalchemy.orm import Session
from datetime import date, timedelta
import models
import schemas


def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(
        name=contact.name,
        surname=contact.surname,
        email=contact.email,
        phone=contact.phone,
        birthday=contact.birthday,
        additional_data=contact.additional_data,
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Contact).offset(skip).limit(limit).all()


def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()


def update_contact(db: Session, db_contact: models.Contact, contact: schemas.ContactUpdate):
    for field, value in contact.dict(exclude_unset=True).items():
        setattr(db_contact, field, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, db_contact: models.Contact):
    db.delete(db_contact)
    db.commit()
    return db_contact


def search_contacts(db: Session, query: str):
    return (
        db.query(models.Contact)
        .filter(
            models.Contact.name.ilike(f"%{query}%")
            | models.Contact.surname.ilike(f"%{query}%")
            | models.Contact.email.ilike(f"%{query}%")
        )
        .all()
    )


def birthday_contacts(db: Session):
    today = date.today()
    next_week = today + timedelta(days=7)
    return (
        db.query(models.Contact)
        .filter(models.Contact.birthday.between(today, next_week))
        .all()
    )
