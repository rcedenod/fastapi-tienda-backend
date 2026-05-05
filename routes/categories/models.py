from db import engine
from utils.logger import logger

def get_categories(search: str, page: int, per_page:int):

    try:

        with engine.connect() as connection:
            
            query = '''
                SELECT
                    CategoryID AS id,
                    Name AS name,
                    Code AS code,
                    Summary AS summary,
                    IsActived AS is_actived,
                    CAST(CreatedAt AS CHAR) AS created_at
                FROM category
                WHERE 
                    Name LIKE %s 
                    AND IsActived = 1
                LIMIT %s OFFSET %s
            '''

            values = (f'{search}%', per_page, (page * per_page) -  per_page)

            result = connection.exec_driver_sql(query, values).fetchall()

            return [dict(item._mapping) for item in result]

    except Exception as e:

        logger.debug(msg=str(e))
        return None
    
def get_category_by_id(id: int):

    try:

        with engine.connect() as connection:
            
            query = '''
                SELECT
                    CategoryID AS id,
                    Name AS name,
                    Code AS code,
                    Summary AS summary,
                    IsActived AS is_actived,
                    CAST(CreatedAt AS CHAR) AS created_at
                FROM category
                WHERE 
                    CategoryID = %s
            '''

            values = (id,)

            result = connection.exec_driver_sql(query, values).fetchone()

            return False if result is None else dict(result._mapping)

    except Exception as e:

        logger.debug(msg=str(e))
        return None
    
def get_products_by_category(id: int):
    
    try:

        with engine.connect() as connection:
            
            query = '''
                SELECT
                    ProductID AS id,
                    CategoryID AS category_id,
                    Name AS name,
                    Code AS code,
                    Summary AS summary,
                    Description AS description,
                    Price AS price,
                    IsActived AS is_actived,
                    IsDeleted as is_deleted,
                    CAST(CreatedAt AS CHAR) AS created_at
                FROM product
                WHERE 
                    CategoryID = %s
                ORDER BY
                    ProductID
            '''

            values = (id,)

            result = connection.exec_driver_sql(query, values).fetchall()

            return [dict(item._mapping) for item in result]

    except Exception as e:

        logger.debug(msg=str(e))
        return None

def get_category_by_code(code: str):
    
    try:

        with engine.connect() as connection:
            
            query = '''
                SELECT
                    CategoryID AS id,
                    Name AS name,
                    Code AS code,
                    Summary AS summary,
                    IsActived AS is_actived,
                    CAST(CreatedAt AS CHAR) AS created_at
                FROM category
                WHERE 
                    Code = %s
            '''

            values = (code,)

            result = connection.exec_driver_sql(query, values).fetchone()

            return False if result is None else dict(result._mapping)

    except Exception as e:

        logger.debug(msg=str(e))
        return None

def create_category(name: str, code: str, summary: str):
    
    try:
        
        with engine.connect() as connection:

            query = '''
                    INSERT INTO category
                    (
                        Name,
                        Code,
                        Summary
                    )
                    values
                    (
                        %s,
                        %s,
                        %s
                    )
                '''

            values = (name, code, summary)

            result = connection.exec_driver_sql(query, values)

            if result.rowcount > 0:
                connection.commit()
                return True
            
    except Exception as e:

        logger.debug(msg=str(e))
        return None
    
def update_category(name: str, summary: str, id: int):
    
    try:
        
        with engine.connect() as connection:

            query = '''
                    UPDATE category
                    SET
                        Name = %s,
                        Summary = %s
                    WHERE
                        CategoryID = %s
                '''

            values = (name, summary, id)

            result = connection.exec_driver_sql(query, values)

            if result.rowcount > 0:
                connection.commit()
                return True
            
    except Exception as e:

        logger.debug(msg=str(e))
        return None

def delete_category(id: int):
    
    try:
        
        with engine.connect() as connection:

            query = '''
                    DELETE FROM category
                    WHERE
                        CategoryID = %s
                '''

            values = (id,)

            result = connection.exec_driver_sql(query, values)

            if result.rowcount > 0:
                connection.commit()
                return True
            
    except Exception as e:

        logger.debug(msg=str(e))
        return None