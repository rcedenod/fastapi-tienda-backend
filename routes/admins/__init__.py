from fastapi import APIRouter, HTTPException, status, Depends, Request, Query
from middlewares import JWTBearer
from utils.logger import logger
from schemas.users import User, BaseUser
from utils.bcrypt import check_password
import routes.admins.models as admins_models

admins_router = APIRouter(prefix='/admins', tags=['admins'], dependencies=[Depends(JWTBearer())])

@admins_router.get('/')
def get_admins(request: Request):
    
    data = request.state._state
    user = data['session']
    
    if user['role'] != 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                            'message': 'Unauthorized, only admins with Role = 1'})
    
    admins = admins_models.get_admins(user)

    if admins is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'Server internal error'})

    for item in admins:
        item['role'] = 'Administrator'

    return admins

@admins_router.get('/search/{id}')
def get_admin_by_id(id: int, request: Request):
    
    data = request.state._state
    user = data['session']
    
    if user['role'] != 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                            'message': 'Unauthorized, only admins with Role = 1'})
    
    admin = admins_models.get_admin_by_id(id)

    if not admin:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'User not found'})
    
    if admin['role'] != 1 :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            'message': 'The user is not an administrator'})
    
    admin['role'] = 'Administrator'

    return admin

@admins_router.post('/create')
def create_admin(admin: User, request: Request):
    
    data = request.state._state
    user = data['session']
    
    if user['role'] != 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                            'message': 'Unauthorized, only admins with Role = 1'})
    
    result = admins_models.create_admin(
        admin.fullname,
        admin.email,
        admin.password,
        admin.role
    )

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            'message': 'Administrator not created'})
    
    if result is None: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'Server internal error'})
    
    return {
            'message': 'Administrator created successfully',
        }

@admins_router.put('/update/{id}')
def update_admin(admin: BaseUser, id: int, request: Request):
    
    data = request.state._state
    user = data['session']
    
    if user['role'] != 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                            'message': 'Unauthorized, only admins with Role = 1'})
    
    exists = admins_models.get_admin_by_id(id)

    if exists is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            'message': 'Administrator not found'})
    
    result = admins_models.update_admin(
        admin.fullname,
        admin.email,
        id
    )

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            'message': 'Administrator not updated'})
    
    if result is None: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'Server internal error'})
    
    return {
            'message': 'Administrator updated successfully',
        }

@admins_router.put('/change-password/{id}')
def change_password(request: Request, id: int, current_password: str, new_password: str = Query(min_length=8)):
    
    data = request.state._state
    user = data['session']
    
    if user['role'] != 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                            'message': 'Unauthorized, only admins with Role = 1'})
    
    exists = admins_models.get_admin_by_id(id)

    if exists is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            'message': 'Administrator not found'})
    
    if check_password(current_password, user['password']):
        
        result = admins_models.change_password(new_password, id)

        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                                'message': 'Administrator password not updated'})
    
        if result is None: 
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                                'message': 'Server internal error'})
    
        return {
                'message': 'Administrator password updated successfully',
            }

    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            'message': 'Incorrect current password'})
    
@admins_router.delete('/delete/{id}')
def delete_admin(request: Request, id: int):

    data = request.state._state
    user = data['session']
    
    if user['role'] != 1:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                            'message': 'Unauthorized, only admins with Role = 1'})

    exists = admins_models.get_admin_by_id(id)

    if exists is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            'message': 'Administrator not found'})
    
    result = admins_models.delete_admin(id)

    if result is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'Server internal error'})

    return {
        'message': 'Administrator deleted successfully',
    }
