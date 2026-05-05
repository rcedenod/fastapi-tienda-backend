from fastapi import APIRouter, HTTPException, status, Depends, File, UploadFile
import routes.files.models as files_models
from middlewares import JWTBearer
from pathlib import Path
from utils.logger import logger

files_router = APIRouter(prefix='/files', tags=['files'], dependencies=[Depends(JWTBearer())])

@files_router.post('/upload/')
async def upload_file(file: UploadFile = File(...)):

    secure_url = await files_models.upload_file_cloud(file)

    if secure_url is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'File upload to cloud failed'})

    name = file.filename
    suffix = Path(name).suffix
    file_name = name[:-len(suffix)] if suffix else name
    file_type = suffix

    result_db = files_models.upload_file_db(file_name, file_type, secure_url)

    if result_db is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                            'message': 'Server internal error'})

    if result_db is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            'message': 'File not uploaded to database'})
    
    return {
         'message':'File uploaded successfully',
         'url': secure_url
    }
    
@files_router.get('/download/')
def download_file(save_as: str = '', file_url: str = ''):
    
    if not file_url:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
                            'message': 'Empty URL Field'})
    
    result = files_models.download_file(save_as, file_url)
    
    if result is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={
                                'message': 'Server internal error'})
    
    return {
            'message': 'File downloaded successfully'
        }