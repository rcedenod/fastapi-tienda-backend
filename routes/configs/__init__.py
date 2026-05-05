from fastapi import APIRouter, HTTPException, status, Depends
from middlewares import JWTBearer
from utils.logger import logger
from schemas.configs import Config
import routes.configs.models as configs_models

configs_router = APIRouter(prefix='/configs', tags=['configs'], dependencies=[Depends(JWTBearer())])

@configs_router.get('/')
def get_configs():

    configs = configs_models.get_configs()

    if configs is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'Server internal error'})

    return configs

@configs_router.get('/search/{id}')
def get_config_by_id(id: int):
    
    config = configs_models.get_config_by_id(id)

    if not config:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'Email configuration not found'})
    
    if config is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'Server internal error'})
    
    return config

@configs_router.put('/update/{id}')
def update_config(config: Config, id: int):
     
    exists = configs_models.get_config_by_id(id)

    if exists is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            'message': 'Email configuration not found'})
    
    result = configs_models.update_config(
        config.host_address,
        config.host_port,
        config.email_address,
        config.email_username,
        config.email_password,
        id
    )

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            'message': 'Email configuration not updated'})
    
    if result is None: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'Server internal error'})
    
    return {
            'message': 'Email configuration updated successfully',
        }