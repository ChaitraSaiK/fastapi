from fastapi import FastAPI
from fastapi import HTTPException, Request, status, Depends, Response
from sqlalchemy.orm import Session
import db,schema
from typing import List

db.Base.metadata.create_all(bind = db.engine)


app = FastAPI()


@app.get("/users",status_code = status.HTTP_200_OK, response_model = List[schema.userOut])
def get_posts(dbd: Session = Depends(db.get_db)):
    posts = dbd.query(db.User).all()
    return posts

@app.get("/users/{uid}",status_code = status.HTTP_200_OK, response_model = schema.userOut)
def get_post(uid :int, dbd: Session = Depends(db.get_db)):
    uid = dbd.query(db.User).filter(db.User.uid == uid).first()

    if not uid:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail = f"user not found"
        )
    return uid

@app.post("/users",status_code = status.HTTP_201_CREATED, response_model = schema.userOut)
def create_post(post: schema.PostCreate, dbd: Session = Depends(db.get_db)):
    new_post = db.User(**post.dict())
    dbd.add(new_post)
    dbd.commit()
    dbd.refresh(new_post)
    return new_post

@app.delete("/users/{uid}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(uid: int,dbd: Session = Depends(db.get_db)):
    post = dbd.query(db.User).filter(db.User.uid == uid)

    if not post.first():
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail = f"user not found"
        )
    post.delete(synchronize_session= False)
    dbd.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/users/{uid}",status_code = status.HTTP_201_CREATED, response_model=schema.userOut)
def update_post(uid: int, updated_post : schema.PostCreate,  dbd: Session = Depends(db.get_db)):
    post_query = dbd.query(db.User).filter(db.User.uid == uid)
    # post = post_query.first()
    if post_query.first() == None:
         raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {uid} does not exists")
    post_query.update(updated_post.dict(), synchronize_session= False)
    dbd.commit()
    return  post_query.first()
  

if __name__ == '__main__':
    app.run()

    