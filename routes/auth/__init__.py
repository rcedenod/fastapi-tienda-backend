from fastapi import APIRouter, HTTPException, status
from schemas.auth import Login, PasswordRecovery
import routes.auth.models as auth_models
from utils.bcrypt import check_password, hash_password
from utils.jwt import encode_token
from routes.auth.services import send_email_pw_recovery
from utils.new_password import generate_password

auth_router = APIRouter(prefix='/auth', tags=['auth'])

@auth_router.post('/login')
def login(user: Login):

    result = auth_models.get_user_by_email(user.email)

    if result is None:

        raise HTTPException(status_code=500)

    elif result is False:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    elif check_password(user.password, result['password']) is False:

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            'message': 'Incorrect password'})
    
    # del result['password']

    token: str = encode_token(result)

    return token
    # return check_password(user.password, result['password'])

@auth_router.post('/password-recovery')
def password_recovery(user: PasswordRecovery):

    user_exists = auth_models.get_user_by_email(user.email)

    if user_exists is None:

        raise HTTPException(status_code=500)

    elif user_exists is False:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    company_config = auth_models.get_company_config()

    if company_config is None:

        raise HTTPException(status_code=500)

    elif company_config is False:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    new_password = generate_password()

    hashed_password = hash_password(new_password)

    result = auth_models.update_password(hashed_password, user_exists['id'])

    if not result:

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    response = send_email_pw_recovery(
        company_config['host_address'],
        company_config['host_port'],
        company_config['email_address'],
        company_config['email_username'],
        company_config['email_password'],
        user_exists['email'],
        new_password
    )

    return response
