from fastapi import FastAPI
from fastapi import HTTPException, Request, status, Depends
from sqlalchemy.orm import Session
import db,schema

db.Base.metadata.create_all(bind = db.engine)


app = FastAPI()


@app.post("/users/create",status_code = status.HTTP_201_CREATED, response_model = schema.userInput)
def create(user: schema.userInput, dbd: Session = Depends(db.get_db)):
    user_email = dbd.query(db.User).filter(db.User.email == user.email).first()

    if not user_email:
        user_dict = user.dict()
        new_user = db.User(**user_dict)
        dbd.add(new_user)
        
        dbd.commit()
        dbd.refresh(new_user)

    else:
        raise HTTPException(
            status_code= status.HTTP_403_FORBIDDEN, detail = f"Email id already exists"
        )
    return new_user

if __name__ == '__main__':
    app.run()

    