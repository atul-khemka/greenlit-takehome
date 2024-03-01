from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
import schemas


def create_user_film_role(db: Session, user_film: schemas.UserFilmCreate):
    film = user_film.film
    old_db_film = db.query(models.Film).filter(models.Film.title == film.title,
                                               models.Film.release_year == film.release_year).one_or_none()
    if old_db_film:
        db_film = old_db_film
    else:
        old_db_company = db.query(models.Company).filter(models.Company.id == film.company_id).one_or_none()
        if not old_db_company:
            raise HTTPException(status_code=404, detail="Company not found")

        db_film = models.Film(**film.model_dump(exclude_unset=True))
        db.add(db_film)
        db.commit()
        db.refresh(db_film)

    user = user_film.user
    old_db_user = db.query(models.User).filter(models.User.email == user.email).one_or_none()
    if old_db_user:
        db_user = old_db_user
    else:
        db_user = models.User(**user.model_dump(exclude_unset=True))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    query = db.query(models.UserFilm).filter(models.UserFilm.user_id == db_user.id,
                                             models.UserFilm.film_id == db_film.id).first()
    if query:
        return query

    db_user_film = models.UserFilm(film=db_film, role=user_film.role)
    db_user.film_associations.append(db_user_film)
    db.add(db_user_film)
    db.commit()
    db.refresh(db_user_film)
    return db_user_film


def get_user_film_by_id(db: Session, user_id: int, film_id: int):
    return db.query(models.UserFilm).filter(models.UserFilm.user_id == user_id,
                                            models.UserFilm.film_id == film_id).first()


def get_all_user_film(db: Session):
    return db.query(models.UserFilm).all()


def update_user_film_role(db: Session, user_id: int, film_id: int, user_film: schemas.UserFilmUpdate):
    db_user_film = db.query(models.UserFilm).filter(models.UserFilm.user_id == user_id,
                                                    models.UserFilm.film_id == film_id).first()
    if not db_user_film:
        raise HTTPException(status_code=404, detail="User Film not found")

    role = user_film.role
    user = user_film.user
    film = user_film.film

    if role:
        db_user_film.role = role

    if film:
        for key, value in film.model_dump(exclude_unset=True).items():
            if key == "company_id" and value:
                db_company = db.query(models.Company).filter(models.Company.id == value).one_or_none()
                if not db_company:
                    raise HTTPException(status_code=404, detail="Company not found")
            setattr(db_user_film.film, key, value) if value else None

    if user:
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user_film.user, key, value) if value else None

    db.commit()
    db.refresh(db_user_film)
    return db_user_film


def create_user_company_role(db: Session, user_company: schemas.UserCompanyCreate):

    user = user_company.user
    old_db_user = db.query(models.User).filter(models.User.email == user.email).one_or_none()
    if old_db_user:
        db_user = old_db_user
    else:
        db_user = models.User(**user.model_dump(exclude_unset=True))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    company = user_company.company
    old_db_company = db.query(models.Company).filter(models.Company.name == company.name).one_or_none()
    if old_db_company:
        db_company = old_db_company
    else:
        db_company = models.Company(**company.model_dump(exclude_unset=True))
        db.add(db_company)
        db.commit()
        db.refresh(db_company)

    query = db.query(models.UserCompany).filter(models.UserCompany.user_id == db_user.id,
                                               models.UserCompany.company_id == db_company.id).first()
    if query:
        return query

    db_user_company = models.UserCompany(company=db_company, role=user_company.role)
    db_user.company_associations.append(db_user_company)
    db.add(db_user_company)
    db.commit()
    db.refresh(db_user_company)
    return db_user_company


def get_user_company_by_id(db: Session, user_id: int, company_id: int):
    return db.query(models.UserCompany).filter(models.UserCompany.user_id == user_id,
                                               models.UserCompany.company_id == company_id).first()


def get_all_user_company(db: Session):
    return db.query(models.UserCompany).all()


def update_user_company_role(db: Session, user_id: int, company_id: int, user_company: schemas.UserCompanyUpdate):
    db_user_company = db.query(models.UserCompany).filter(models.UserCompany.user_id == user_id,
                                                          models.UserCompany.company_id == company_id).first()
    if not db_user_company:
        raise HTTPException(status_code=404, detail="User company not found")

    role = user_company.role
    user = user_company.user
    company = user_company.company

    if role:
        db_user_company.role = role

    if user:
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(db_user_company.user, key, value) if value else None

    if company:
        for key, value in company.model_dump(exclude_unset=True).items():
            setattr(db_user_company.company, key, value) if value else None

    db.commit()
    db.refresh(db_user_company)
    return db_user_company
