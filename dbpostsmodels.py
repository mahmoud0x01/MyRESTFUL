from sqlalchemy import Column, Integer, String, ForeignKey
from rdb import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "User"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    postsown = relationship("Posts", backref="author")



class Posts(Base):
    __tablename__ = "Posts"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("User.id"))
    #owner_name = Column(String,owner_id.name)
    #user = relationship("User", back_populates="postsown")
    likes = Column(Integer,nullable=False, default=0)
    dislikes = Column(Integer,nullable=False, default=0)

