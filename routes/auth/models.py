from db import engine
from utils.logger import logger
from utils.bcrypt import hash_password, gensalt

def get_user_by_email(email: str):
    try:
        with engine.connect() as connection:
            query = '''
                SELECT
                    UserID as id,
                    Fullname as fullname,
                    Email as email,
                    Password as password,
                    Role as role
                FROM user
                WHERE 
                    Email = %s          
            '''

            values = (email,)

            result = connection.exec_driver_sql(query, values).fetchone()

            return False if result is None else dict(result._mapping)

    except Exception as e:

        logger.debug(msg=str(e))
        return None

def get_company_config():
    try:
        with engine.connect() as connection:
            query = '''
                SELECT
                    EmailConfigID as email_config_id,
                    HostAddress as host_address,
                    HostPort as host_port,
                    EmailAddress as email_address,
                    EmailUsername as email_username,
                    EmailPassword as email_password
                FROM email_config
                WHERE 
                    EmailConfigID = 1     
            '''
            result = connection.exec_driver_sql(query).fetchone()

            return False if result is None else dict(result._mapping)
    
    except Exception as e:

        logger.debug(msg=str(e))
        return None

def update_password(new_password: str, user_id: int):
    
    try:

        with engine.connect() as connection:

            query = '''
                UPDATE user set Password = %s where UserID = %s    
            '''
            values = (new_password, user_id)
            result = connection.exec_driver_sql(query, values)

            if result.rowcount > 0:
                connection.commit()
                return True

            return False
    
    except Exception as e:

        logger.debug(msg=str(e))
        return None
