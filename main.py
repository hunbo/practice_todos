# main.py 는 실제 웹 애플리케이션이 동작하는 파일로, FASTAPI 웹 프레임워크와 함께 라우팅, 비즈니스 로직, DB 세션 관리를 함.


from fastapi import FastAPI, Request, Form, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import uvicorn
from database import engine,Sessionlocal
from sqlalchemy.orm import Session
import models
from fastapi.responses import RedirectResponse

app = FastAPI()

#DB 엔진 연결
# Base.metadata.create_all(bind=engine)
models.Base.metadata.create_all(bind=engine)
# models.py에서 정의된 모델(Todo)을 바탕으로 
# 실제 데이터베이스 테이블을 생성합니다. 
# 여기서 engine은 database.py에서 설정한 데이터베이스 연결 객체입니다.


# 데이터베이스 세션을 생성하고 관리하는 역할.
def get_db():
    db = Sessionlocal()   # 데이터베이스와 연결하는 세션을 생성하는 함수.
    try:
        yield db   # fastapi에서 이 yield 문을 사용해서 데이터베이스 세션을 요청마다 생성하고, 요청이 끝나면 세션을 자동으로 닫도록 관리함.
    except:
        print("db연결 오류")
    finally:
        db.close()

abs_path = os.path.dirname(os.path.realpath(__file__))

#html 템플릿 폴더를 지정하여 jinja템플릿 객체 생성
templates = Jinja2Templates(directory="templates")
# templates = Jinja2Templates(directory=f"{abs_path}/templates")

#static 폴더(정적파일 폴더)를 app에 연결 - (image,css,js)
app.mount("/static", StaticFiles(directory=f"static"), name="static")
# app.mount("/static", StaticFiles(directory=f"{abs_path}/static"), name='static')

@app.get("/")
async def home(request:Request, db_ss : Session = Depends(get_db)): #db:Session은 이 변수가 SQLAlchemy 세션 객체임을 명시.
    # Depends(get_db) : FastAPI는 Depends()를 통해 의존성 주입을 사용하여 get_db() 함수를 호출하고, 이 함수가 변환하는 값을 db_ss 변수에 할당.
    # db객체 생성, 세션 연갈하기 <- 의존성 주입으로 처리
    # 테이블 조회
    todos = db_ss.query(models.Todo) \
    .order_by(models.Todo.id.desc())
    print(type(todos))

    #db 조회한 결과를 출력
    for todo in todos:
        print(todo.id, todo.task, todo.completed)
    return templates.TemplateResponse("index.html",
                                      {"request":request,
                                       "todos":todos
                                       })


# Depends(get_db): FastAPI에서 의존성 주입을 통해 get_db() 함수를 사용하여 데이터베이스 세션을 주입받습니다. 
# 이 세션을 통해 데이터베이스와 상호작용합니다.
@app.post("/add")
async def add(request:Request, task:str=Form(...), db_ss : Session = Depends(get_db) ):
    #여기의 task는 index.html에서 textarea name="task" 의 task임!

    # 클라이언트에서 textarea에서 입력 데이터 넘어오면
    # db 테이블에 저장하고 결과를 html에 랜더링에서 리턴
    print(task)
    # 클라이언트에게서 넘어온 task를 Todo 객체로 생성
    todo = models.Todo(task=task)
    # db 의존성 주입해서 처리함 Depends(get_db) : 엔진객체생성, 세션연결,
    db_ss.add(todo)
    # db에 실제로 저장, commit
    db_ss.commit()

    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
    

@app.get("/edit/{todo_id}")
async def edit(request:Request, todo_id:int, db:Session=Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id==todo_id).first() # query:데이터베이스에서 데이터를 조회
    return templates.TemplateResponse("edit.html", {"request": request, "todo": todo})

@app.post("/edit/{todo_id}")
async def edit(request:Request, todo_id:int, task:str = Form(...), completed:bool = Form(False), db:Session=Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.task = task
    todo.completed = completed
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
    

@app.get("/delete/{todo_id}")  #라우팅, 주로 서버에서 데이터를 조회하거나, 특정 작업을 처리한 후에 리디렉션할 때 GET 요청을 함
async def delete(request:Request, todo_id:int, db:Session=Depends(get_db)):  #todo_id는 경로 매개변수
    todo = db.query(models.Todo).filter(models.Todo.id==todo_id).first() #.first(): 이 쿼리는 조건을 만족하는 항목 중 첫 번째 결과를 반환. 만약 조선을 만족하는 항목이 없으면 None을 반환
    db.delete(todo)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)



if __name__ == "__main__" :
    uvicorn.run("main:app", reload=True)