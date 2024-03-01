from typing import Optional
from pydantic import BaseModel
from models import UserCompanyRole, UserFilmRole


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    minimum_fee: Optional[int] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    minimum_fee: Optional[int] = None


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class FilmBase(BaseModel):
    title: str
    description: Optional[str] = None
    budget: Optional[int] = None
    release_year: int
    genres: list[str]
    company_id: int


class FilmCreate(FilmBase):
    pass


class FilmUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    budget: Optional[int] = None
    release_year: Optional[int] = None
    genres: Optional[list[str]] = None
    company_id: Optional[int] = None


class Film(FilmBase):
    id: int

    class Config:
        orm_mode = True


class CompanyBase(BaseModel):
    name: str
    contact_email_address: Optional[str]
    phone_number: Optional[str] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    contact_email_address: Optional[str] = None
    phone_number: Optional[str] = None


class Company(CompanyBase):
    id: int

    class Config:
        orm_mode = True


class UserCompanyCreate(BaseModel):
    role: UserCompanyRole
    user: UserCreate
    company: CompanyCreate


class UserCompanyUpdate(BaseModel):
    role: Optional[UserCompanyRole] = None
    user: Optional[UserUpdate] = None
    company: Optional[CompanyUpdate] = None


class UserCompany(BaseModel):
    role: UserCompanyRole
    user: User
    company: Company

    class Config:
        orm_mode = True


class UserFilmCreate(BaseModel):
    role: UserFilmRole
    user: UserCreate
    company: FilmCreate


class UserFilmUpdate(BaseModel):
    role: Optional[UserFilmRole] = None
    user: Optional[UserUpdate] = None
    company: Optional[FilmUpdate] = None


class UserFilm(BaseModel):
    role: UserFilmRole
    user: User
    film: Film

    class Config:
        orm_mode = True


class GenericResponse(BaseModel):
    status: bool
    message: str


class UserCompanyResponse(GenericResponse):
    data: UserCompany


class AllUserCompanyResponse(GenericResponse):
    data: list[UserCompany]


class UserFilmResponse(GenericResponse):
    data: UserFilm


class AllUserFilmResponse(GenericResponse):
    data: list[UserFilm]
