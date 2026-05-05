from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, status
from utils.logger import logger
from utils.jwt import decode_token
    
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):

        payload = await super().__call__(request)

        if payload is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        try:

            request.state._state.update({'session': decode_token(payload.credentials)})

        except Exception as e:
            logger.debug(str(e))
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                                'message': 'Invalid token'})