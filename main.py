import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from loggers.logger import get_custom_logger, get_rotating_file_handler, init_logging
from loggers.middleware import LoggerMiddleware
from routers import router
from settings import settings

url_logger = get_custom_logger(
    logger_name=__name__,
    handlers=[get_rotating_file_handler(settings.PATH_LOG_DIR, "urls.log")],
)

tags_metadata = [
    {
        "name": "API ASUTP Controller",
        "description": "API взаимодействия с данными контроллера АСУТП водоподготовки.",
    }
]

app = FastAPI(
    openapi_tags=tags_metadata,
    title="API ASUTP Controller",
    version="0.0.1",
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
app.add_middleware(LoggerMiddleware, logger=url_logger)


@app.on_event("startup")
async def startup_event():
    init_logging(settings.PATH_LOG_DIR, level_console="DEBUG")


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=settings.SERVER_HOST, port=settings.SERVER_PORT, reload=True
    )


@app.get("/", include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
