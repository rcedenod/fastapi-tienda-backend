from db import engine
from utils.logger import logger
from pydantic import EmailStr
from utils.bcrypt import hash_password

def get_profile(admin: dict):
    
    try:
        with engine.connect() as connection:
            query = '''
                SELECT
                    UserID as id,
                    Fullname as fullname,
                    Email as email,
                    Role as role
                FROM user
                WHERE
                    UserID = %s
            '''

            values = (admin['id'],)
            result = connection.exec_driver_sql(query, values).fetchone()

            return False if result is None else dict(result._mapping)

    except Exception as e:

        logger.debug(msg=str(e))
        return None
    
def update_profile(fullname: str, email: EmailStr, id: int):

    try:

        with engine.connect() as connection:
            
            query = '''
                UPDATE user
                SET
                    Fullname = %s,
                    Email = %s
                WHERE
                    UserID = %s
            '''
            values = (fullname, email, id)

            result = connection.exec_driver_sql(query, values)

            if result.rowcount > 0:
                connection.commit()
                return True
            
            return False

    except Exception as e:

        logger.debug(msg=str(e))
        return None
    
def change_password(new_password: str, id: int):
    
    try:

        with engine.connect() as connection:
            
            query = '''
                UPDATE user
                SET
                    Password = %s
                WHERE
                    UserID = %s
            '''
            values = (hash_password(new_password), id)

            result = connection.exec_driver_sql(query, values)

            if result.rowcount > 0:
                connection.commit()
                return True
            
            return False
        
    except Exception as e:

        logger.debug(msg=str(e))
        return None