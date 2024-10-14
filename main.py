from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import uvicorn

app = FastAPI()

abs_path = os.path.dirname(os.path.realpath(__file__))

#html 템플릿 폴더를 지정하여 jinja템플릿 객체 생성
templates = Jinja2Templates(directory="templates")
# templates = Jinja2Templates(directory=f"{abs_path}/templates")

#static 폴더(정적파일 폴더)를 app에 연결 - (image,css,js)
app.mount("/static", StaticFiles(directory=f"static"), name="static")
# app.mount("/static", StaticFiles(directory=f"{abs_path}/static"), name='static')

@app.get("/")
async def home(request:Request):
    todos = 100
    todos2 = "fast api 잘하고 싶다"
    return templates.TemplateResponse("index.html",
                                      {"request":request,
                                       "todos":todos,
                                       "todos2":todos2})

if __name__ == "__main__" :
    uvicorn.run("main:app", reload=True)