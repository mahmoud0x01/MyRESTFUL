from fastapi import FastAPI,Depends, HTTPException
import schemas
import dbpostsmodels as models
from rdb import engine, SessionLocal
from sqlalchemy.orm import Session
import crud
import auth

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


@app.post("/register/", summary="User Signup", status_code= 201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)



@app.post('/login', summary="Create access and refresh tokens for user")
def login(form_data: schemas.login, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db=db,email=form_data.id)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    hashed_pass = user.hashed_password
    if (auth.verify_password(form_data.password, hashed_pass) == False):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": auth.create_access_token(user.email),
        "refresh_token": auth.create_refresh_token(user.email),
    }



@app.post("/posts/create")
def create_post(post: schemas.post,token: str,db: Session = Depends(get_db)):
	user_db = get_current_user(token=token, db=db)
	if(user_db is None):
		raise HTTPException(status_code=403,detail="Not Authorized or not logged in. Please Login at /login")

	db_post = crud.create_user_post(db=db,post=post,user_id=user_db.id)
	return db_post


@app.post("/posts/edit")
def edit_post(postid: str, post: schemas.post,token: str,db: Session = Depends(get_db)):
	user_db = get_current_user(token=token, db=db)
	if(user_db is None):
		raise HTTPException(status_code=403,detail="Not Authorized or not logged in. Please Login at /login")

	ownerid = user_db.id
	owner = crud.get_post_owner(db=db,postid=postid)
	if(owner != ownerid):
		raise HTTPException(status_code=403,detail="Not Authorized or Post Does not exist")
	return crud.edit_user_post(db=db,post=post,postid=postid)


@app.post("/posts/delete")
def delete_post(postid: str,token: str, db: Session = Depends(get_db)):
	user_db = get_current_user(token=token, db=db)
	owner = crud.get_post_owner(db=db,postid=postid)
	if(user_db is None):
		raise HTTPException(status_code=403,detail="Not Authorized or not logged in. Please Login at /login")

	ownerid = user_db.id
	if(owner != ownerid):
		raise HTTPException(status_code=403,detail="Not Authorized or Post Does not exist")
	return crud.delete_user_post(db=db,postid=postid)



@app.put("/posts/dislike")
def put_dislike(dislike: schemas.LikeCreate,token: str ,db: Session =Depends(get_db)):
	user_db = get_current_user(token=token, db=db)
	if(user_db is None):
		raise HTTPException(status_code=403,detail="Not Authorized or not logged in. Please Login at /login")

	if(user_db is not None):
		if(dislike.liker_id != user_db.id):
			raise HTTPException(status_code=403,detail="Not Authorized or not logged in. Please Login at /login")
	post_owner = crud.get_post_owner(db=db,postid=dislike.post_id)
	if(post_owner == None):
		return {'Error': 'Post Does not Exist'}

	if (post_owner==dislike.liker_id):
		return {'Error','Not allowed to like your own post'}
	return crud.create_dislike(db=db,dislikepost=dislike)

@app.put("/posts/like")
def put_like(like: schemas.LikeCreate,token: str, db: Session = Depends(get_db)):
	user_db = get_current_user(token=token, db=db)
	if(user_db is None):
		raise HTTPException(status_code=403,detail="Not Authorized or not logged in. Please Login at /login")
		
	if(user_db is not None):
		if(like.liker_id != user_db.id):
			raise HTTPException(status_code=403,detail="Not Authorized or not logged in. Please Login at /login")
	post_owner = crud.get_post_owner(db=db,postid=like.post_id)
	if(post_owner == None):
		return {'Error': 'Post Does not Exist'}

	if (post_owner==like.liker_id):
		return {'Error','Not allowed to like your own post'}
	return crud.create_like(db=db,likepost=like)





@app.get("/users/")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/user/{id}/posts")
def get_user_details(id: str,db: Session = Depends(get_db)):
	return crud.get_postowner_details(db=db,userid=id)


@app.get("/posts/")
def read_posts(skip: int = 0,limit: int = 100,db: Session = Depends(get_db)):
	posts = crud.get_posts(db, skip=skip, limit=limit)
	return posts

@app.get("/posts/{id}")
def get_post_details(id: str,db: Session = Depends(get_db)):
	return crud.get_all_post_details(db=db,postid=id)


@app.get("/whoami")
def get_current_user(token: str, db: Session = Depends(get_db)):
	username = auth.authorize_current_user(token=token)
	return crud.get_user_by_email(db=db, email= username)

