from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.routers import convert, translate

app = FastAPI(title="文件转换与翻译工具")

app.include_router(convert.router, prefix="/api", tags=["转换"])
app.include_router(translate.router, prefix="/api", tags=["翻译"])

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")
