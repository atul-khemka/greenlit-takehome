from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from database import Base
import enum


class UserFilmRole(enum.Enum):
    writer = 'writer'
    producer = 'producer'
    director = 'director'


class UserCompanyRole(enum.Enum):
    owner = 'owner'
    member = 'member'


class UserFilm(Base):
    __tablename__ = 'user_films'

    user_id = Column(ForeignKey('users.id'), primary_key=True)
    film_id = Column(ForeignKey('films.id'), primary_key=True)
    role = Column(Enum(UserFilmRole), nullable=False)

    user = relationship('User', back_populates='film_associations')
    film = relationship('Film', back_populates='maker_associations')


class UserCompany(Base):
    __tablename__ = 'user_companies'

    user_id = Column(ForeignKey('users.id'), primary_key=True)
    company_id = Column(ForeignKey('companies.id'), primary_key=True)
    role = Column(Enum(UserCompanyRole), nullable=False)

    user = relationship('User', back_populates='company_associations')
    company = relationship('Company', back_populates='member_associations')


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    minimum_fee = Column(Integer)

    films = relationship("Film", secondary="user_films", back_populates='makers', viewonly=True)
    film_associations = relationship("UserFilm", back_populates='user')

    companies = relationship("Company", secondary="user_companies", back_populates='members', viewonly=True)
    company_associations = relationship("UserCompany", back_populates='user')


class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    budget = Column(Integer)
    release_year = Column(Integer, nullable=False)
    genres = Column(ARRAY(String))
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("Company", back_populates="films")

    makers = relationship("User", secondary="user_films", back_populates="films", viewonly=True)
    maker_associations = relationship("UserFilm", back_populates='film')


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_email_address = Column(String)
    phone_number = Column(String)

    films = relationship("Film", back_populates="company")

    members = relationship("User", secondary="user_companies", back_populates="companies", viewonly=True)
    member_associations = relationship("UserCompany", back_populates='company')
