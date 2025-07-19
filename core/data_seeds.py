from core.security import get_password_hash
from models.role import Role
from models.type_info import Type
from fastapi import Depends
from core.db import SessionLocal
from sqlalchemy.orm import Session
from models.token import Token
from models.user import User


def seed_types(db: Session):
    if db.query(Type).first():
        print("Ya existen los tipos de información. Seed omitido.")
        return
    info = [
        Type(name='Herramientas observabilidad'),
        Type(name='Información relevante'),
        Type(name='Tarjeta con imagen'),
        Type(name='Información herramientas observabilidad'),
        Type(name='Videos'),
    ]
    db.add_all(info)
    print("Tipos de información añadidos.")

def seed_roles(db: Session):
    if db.query(Role).first():
        print("Ya existen los roles. Seed omitido.")
        return
    roles = [
        Role(id='864c38b2-4a35-40a1-84d4-39af5a18b3bc',name='Administrador'),
        Role(id='b64bcee3-1bee-468e-9825-39a7a77112bc',name='Usuario'),
    ]
    db.add_all(roles)
    print("Roles añadidos.")

def seed_token(db: Session):
    if db.query(Token).first():
        print("Ya existen los roles. Seed omitido.")
        return
    roles = [
        Token(id='60e4daec-19f7-4cc7-a5fa-74c23cad2bf7',title='Dynatrace', user_id='340e887e-67f2-4a89-b9b0-aed8b28c6c10', token=''),
        Token(id='23fc730f-7acd-4727-b157-43152cfa02de',title='New Relic', user_id='340e887e-67f2-4a89-b9b0-aed8b28c6c10', token=''),
        Token(id='c052574a-9e1f-46cf-9d6e-6f87d2138c23',title='Client Secret', user_id='340e887e-67f2-4a89-b9b0-aed8b28c6c10', token=''),
        Token(id='6d61cbd3-c8c4-4861-b75c-373b0a554cb1',title='Complemento dynatrace', user_id='340e887e-67f2-4a89-b9b0-aed8b28c6c10', token=''),
    ]
    db.add_all(roles)
    print("Tokens añadidos.")
    
def seed_admin(db: Session):
    if db.query(Token).first():
        print("Ya existen los roles. Seed omitido.")
        return
    roles = [
        User(id='340e887e-67f2-4a89-b9b0-aed8b28c6c10', name='Admin', email='admin@admin.com',role_id='864c38b2-4a35-40a1-84d4-39af5a18b3bc',password=get_password_hash('admin123')),
    ]
    db.add_all(roles)
    print("Usuario añadido.")

def run_seeds():
    db: Session = SessionLocal()
    seed_types(db)
    seed_roles(db)
    seed_admin(db)
    seed_token(db)
    db.commit()
    db.close()

