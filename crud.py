from sqlalchemy.orm import Session

import dbpostsmodels as models
import schemas
import auth
from uuid import uuid4

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_postowner_details(db: Session,userid: str):
    user = db.query(models.User).filter(models.User.id == userid).first()
    return {'id':user.id, 'name': user.name, 'email': user.email, 'number of posts': len(user.postsown), 'Other_Posts': dict(user.postsown)}

def get_all_post_details(db: Session,postid: str):

     db_post = db.query(models.Posts).filter_by(id=postid).first()
     #db_user = db.query(models.User).filter_by(id=db_post.author.id).first()
     return db_post , {'Author ': db_post.author.name}


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(*[c for c in models.User.__table__.c if c.name != 'hashed_password']).offset(skip).limit(limit).all()



def get_posts(db: Session, skip: int = 0 , limit: int=100):
    return db.query(models.Posts).offset(skip).limit(limit).all()


def get_post_owner(db: Session, postid: str):
    db_post = db.query(models.Posts).filter_by(id=postid).first()
    if(bool(db_post) == False):
        return None
    return db_post.owner_id



def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_hashed_password(user.password)
    id = str(uuid4())
    db_user = models.User(id = id,email=user.email, hashed_password=hashed_password, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # to refresh the row added in the db so that db_user have actual values from current db
    return{'id': db_user.id,'email': db_user.email,'name':db_user.name}



def create_user_post(db: Session, post: schemas.post, user_id: str):
    db_user = db.query(models.User).filter_by(id=user_id).first()
    id = str(uuid4())
    db_post = models.Posts(id = id,title=post.title,description=post.description, author=db_user)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def edit_user_post(db: Session, post: schemas.post,postid: str):
    db_post = db.query(models.Posts).filter_by(id=postid).first()
    db_post.description = post.description
    db_post.title = post.title
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_user_post(db: Session,postid: str):
    db_post = db.query(models.Posts).filter_by(id=postid)
    db_post.delete()
    db.commit()
    return "Done."

def create_like(db: Session, likepost: schemas.LikeCreate):
    db_post = db.query(models.Posts).filter_by(id=likepost.post_id).first()
    db_post.likes = (db.query(models.Posts).filter_by(id=likepost.post_id).first()).likes + 1
    db.commit()
    db.refresh(db_post)
    return db_post



def create_dislike(db: Session, dislikepost: schemas.LikeCreate):
    db_post = db.query(models.Posts).filter_by(id=dislikepost.post_id).first()
    db_post.dislikes = (db.query(models.Posts).filter_by(id=dislikepost.post_id).first()).dislikes + 1
    db.commit()
    db.refresh(db_post)
    return db_post
