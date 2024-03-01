from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import SessionLocal, engine

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/user-company/{user_id}/{company_id}", response_model=schemas.UserCompanyResponse)
async def get_user_company_by_id(user_id: int, company_id: int, db: Session = Depends(get_db)):
    db_user_company = crud.get_user_company_by_id(db, user_id=user_id, company_id=company_id)
    if db_user_company is None:
        raise HTTPException(status_code=404, detail="Details not found")
    return {"status": True, "message": "Success", "data": db_user_company}


@app.get("/user-company/", response_model=schemas.AllUserCompanyResponse)
async def get_user_company(db: Session = Depends(get_db)):
    db_user_company = crud.get_all_user_company(db)
    return {"status": True, "message": "Success", "data": db_user_company}


@app.post("/user-company/", response_model=schemas.UserCompanyResponse)
def create_user_company(user_company: schemas.UserCompanyCreate, db: Session = Depends(get_db)):
    db_user_company = crud.create_user_company_role(db, user_company=user_company)
    return {"status": True, "message": "Created", "data": db_user_company}


@app.patch("/user-company/{user_id}/{company_id}", response_model=schemas.UserCompanyResponse)
def update_user_company(user_id: int, company_id: int, user_company: schemas.UserCompanyUpdate,
                        db: Session = Depends(get_db)):
    db_user_company = crud.update_user_company_role(db, user_id, company_id, user_company)
    return {"status": True, "message": "Updated", "data": db_user_company}


@app.get("/user-film/{user_id}/{film_id}", response_model=schemas.UserFilmResponse)
async def get_user_film_by_id(user_id: int, film_id: int, db: Session = Depends(get_db)):
    db_user_film = crud.get_user_film_by_id(db, user_id=user_id, film_id=film_id)
    if db_user_film is None:
        raise HTTPException(status_code=404, detail="Details not found")
    return {"status": True, "message": "Success", "data": db_user_film}


@app.get("/user-film/", response_model=schemas.AllUserFilmResponse)
async def get_user_film(db: Session = Depends(get_db)):
    db_user_film = crud.get_all_user_film(db)
    return {"status": True, "message": "Success", "data": db_user_film}


@app.post("/user-film/", response_model=schemas.UserFilmResponse)
def create_user_film(user_film: schemas.UserFilmCreate, db: Session = Depends(get_db)):
    db_user_film = crud.create_user_film_role(db, user_film=user_film)
    return {"status": True, "message": "Created", "data": db_user_film}


@app.patch("/user-film/{user_id}/{film_id}", response_model=schemas.UserFilmResponse)
def update_user_film(user_id: int, film_id: int, user_film: schemas.UserFilmUpdate,
                     db: Session = Depends(get_db)):
    db_user_film = crud.update_user_film_role(db, user_id, film_id, user_film)
    return {"status": True, "message": "Updated", "data": db_user_film}
