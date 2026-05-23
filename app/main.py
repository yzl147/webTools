from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.routers import convert

app = FastAPI(title="文件转换工具")

app.include_router(convert.router, prefix="/api", tags=["转换"])

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")
