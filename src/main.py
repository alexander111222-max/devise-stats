import logging

import uvicorn
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from src.api.users import router as users_router
from src.api.measurements import router as measurements_router
from src.api.devices import router as devices_router
from src.api.analytics import router as analytics_router
from src.utils.exceptions import StatsException

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


app = FastAPI()


@app.exception_handler(StatsException)
async def app_exception_handler(request: Request, exc: StatsException):
    logging.error(f"Ошибка приложения: {exc.detail} | path={request.url.path}")
    return JSONResponse(status_code=500, content={"detail": exc.detail})


app.include_router(users_router)
app.include_router(measurements_router)
app.include_router(devices_router)
app.include_router(analytics_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
