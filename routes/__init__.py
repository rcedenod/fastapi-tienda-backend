from fastapi import APIRouter
from routes.auth import auth_router
from routes.products import products_router
from routes.categories import categories_router
from routes.admins import admins_router
from routes.profile import profile_router
from routes.configs import configs_router
from routes.files import files_router

app_router = APIRouter(prefix='/api')

app_router.include_router(auth_router)
app_router.include_router(products_router)
app_router.include_router(categories_router)
app_router.include_router(admins_router)
app_router.include_router(profile_router)
app_router.include_router(configs_router)
app_router.include_router(files_router)