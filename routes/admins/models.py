from db import engine
from utils.logger import logger
from pydantic import EmailStr
from utils.bcrypt import hash_password

def get_admins(admin: dict):
    
    try:
        with engine.connect() as connection:
            query = '''
                SELECT
                    UserID as id,
                    Fullname as fullname,
                    Email as email,
                    Role as role,
                    CAST(CreatedAt AS CHAR) AS created_at
                FROM user
                WHERE
                    UserID != %s
                    AND Role = 1
                ORDER BY UserID
            '''

            values = (admin['id'],)
            result = connection.exec_driver_sql(query, values).fetchall()

            return [dict(item._mapping) for item in result]

    except Exception as e:

        logger.debug(msg=str(e))
        return None
      
def get_admin_by_id(id: int):

    try:

        with engine.connect() as connection:
            
            query = '''
                SELECT
                    UserID AS id,
                    Fullname AS fullname,
                    Role AS role,
                    CAST(CreatedAt AS CHAR) AS created_at
                FROM user
                WHERE 
                    UserID = %s
            '''

            values = (id, )

            result = connection.exec_driver_sql(query, values).fetchone()

            return False if result is None else dict(result._mapping)

    except Exception as e:

        logger.debug(msg=str(e))
        return None
    
def create_admin(fullname: str, email: EmailStr, password: str, role: int):
    
    try:

        with engine.connect() as connection:
            
            query = '''
                INSERT INTO user
                (
                Fullname,
                Email,
                Password,
                Role
                )
                values
                (
                %s,
                %s,
                %s,
                %s
                )
            '''
            values = (fullname, email, hash_password(password), role)

            result = connection.exec_driver_sql(query, values)

            if result.rowcount > 0:
                connection.commit()
                return True
            
            return False

    except Exception as e:

        logger.debug(msg=str(e))
        return None
    
def update_admin(fullname: str, email: EmailStr, id: int):

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
    
def delete_admin(id: int):

    try:

        with engine.connect() as connection:
            
            query = '''
                UPDATE user
                SET
                    IsActived = 0,
                    IsDeleted = 1
                WHERE
                    UserID = %s
            '''
            values = (id,)

            result = connection.exec_driver_sql(query, values)

            if result.rowcount > 0:
                connection.commit()
                return True
            
            return False

    except Exception as e:

        logger.debug(msg=str(e))
        return None