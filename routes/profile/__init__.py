from fastapi import APIRouter, HTTPException, status, Depends, Request, Query
from middlewares import JWTBearer
from utils.logger import logger
from schemas.users import User, BaseUser
from utils.bcrypt import check_password
import routes.profile.models as profile_models

profile_router = APIRouter(prefix='/profile', tags=['profile'], dependencies=[Depends(JWTBearer())])

@profile_router.get('/')
def get_profile(request: Request):
    
    data = request.state._state
    user = data['session']

    admin = profile_models.get_profile(user)

    if admin is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'Server internal error'})
    
    admin['role'] = 'Administrator'

    return admin

@profile_router.put('/update')
def update_profile(profile: BaseUser, request: Request):
    
    data = request.state._state
    user = data['session']
    
    result = profile_models.update_profile(
        profile.fullname,
        profile.email,
        user['id']
    )

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            'message': 'Profile not updated'})
    
    if result is None: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'Server internal error'})
    
    return {
            'message': 'Profile updated successfully',
    }

@profile_router.put('/change-password')
def change_password(request: Request, current_password: str, new_password: str = Query(min_length=8)):
    
    data = request.state._state
    user = data['session']
        
    if check_password(current_password, user['password']):
        
        result = profile_models.change_password(new_password, user['id'])

        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                                'message': 'Password not updated'})
    
        if result is None: 
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                                'message': 'Server internal error'})
    
        return {
                'message': 'Password updated successfully',
            }

    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            'message': 'Incorrect current password'})