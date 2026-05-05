from db import engine
from utils.logger import logger
from utils.bcrypt import hash_password
from pydantic import EmailStr

def get_configs():
    
    try:
        with engine.connect() as connection:
            query = '''
                SELECT
                    EmailConfigID as id,
                    HostAddress as host_address,
                    HostPort as host_port,
                    EmailAddress as email_address,
                    EmailUsername as email_username,
                    CAST(CreatedAt AS CHAR) AS created_at
                FROM email_config
            '''

            result = connection.exec_driver_sql(query).fetchall()

            return [dict(item._mapping) for item in result]

    except Exception as e:

        logger.debug(msg=str(e))
        return None
    
def get_config_by_id(id: int):

    try:

        with engine.connect() as connection:
            
            query = '''
                SELECT
                    EmailConfigID as id,
                    HostAddress as host_address,
                    HostPort as host_port,
                    EmailAddress as email_address,
                    EmailUsername as email_username,
                    CAST(CreatedAt AS CHAR) AS created_at
                FROM email_config
                WHERE 
                    EmailConfigID = %s
            '''

            values = (id, )

            result = connection.exec_driver_sql(query, values).fetchone()

            return False if result is None else dict(result._mapping)

    except Exception as e:

        logger.debug(msg=str(e))
        return None
    
def update_config(
        host_address: EmailStr, 
        host_port: int, 
        email_address: EmailStr, 
        email_username: EmailStr, 
        email_password: str, 
        id: int
        ):

    try:

        with engine.connect() as connection:
            
            query = '''
                UPDATE email_config
                SET
                    HostAddress = %s,
                    HostPort = %s,
                    EmailAddress = %s,
                    EmailUsername = %s,
                    EmailPassword = %s
                WHERE
                    EmailConfigID = %s
            '''
            values = (
                host_address,
                host_port,
                email_address,
                email_username,
                hash_password(email_password),
                id
            )

            result = connection.exec_driver_sql(query, values)

            if result.rowcount > 0:
                connection.commit()
                return True
            
            return False

    except Exception as e:

        logger.debug(msg=str(e))
        return None