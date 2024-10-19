from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware

from routes.main import api_router
from settings import config

middlewares = []

app = FastAPI(middleware=middlewares)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=config.ALLOWED_HOSTS)
app.include_router(api_router)
