from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


app = FastAPI()

from routers.field import router as field_router
app.include_router(field_router, prefix="/field")

from routers.sensor_router import router as sensor_router
app.include_router(sensor_router, prefix="/sensor")

from routers.agri_mach import router as agri_mach_router
app.include_router(agri_mach_router, prefix="/agri_mach")

from routers.user_router import router as user_router
app.include_router(user_router, prefix="/user")

from routers.llm_router import router as llm_router
app.include_router(llm_router, prefix="/llm")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


__all__ = [
    "app"
]


if __name__ == "__main__":
    import uvicorn
    from utils import logger
    logger.info("以本地测试模式启动...")
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8080
    )