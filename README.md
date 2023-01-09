# A RESTFUL API written in PYTHON using FASTAPI() and SQLalchemy

This is a functional **RESTFUL API** which has the next features :

- Signup
- Login
- Create Posts
- Edit Posts
- Delete Posts
- Like/Dislike Posts
- Some other Authorization check endpoints

I am using **Session Handling** by makine a **JWT implementation**

## INSTALL
1. clonning the repo with **git**
` git clone https://github.com/mahmoud0x01/MyRESTFUL.git `
2. installing requirements of Python libraries
`cd MyRESTFUL && pip3 install -r requirements.txt`

## Usage
1. Setting up some keys or leaving them as default inside file `auth.py`
>JWT_SECRET_KEY, JWT_REFRESH_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, ALGORITHM
2. starting the server using **unicorn**
`uvicorn main:app --reload`


## Docs
all documentaions about each endpoint of the API is available thanks to **FASTAPI Features** at `http://$HOST:$PORT/docs#/` 
you can also test the **POST, PUT** methods without scripting or proxy . the API DOC gives you the ability to do that
