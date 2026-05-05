from db import engine
from utils.logger import logger

def get_products(search: str, page: int, per_page: int) :

    try:

        with engine.connect() as connection:
            
            query = '''
                SELECT
                    ProductID AS id,
                    CategoryID AS category_id,
                    Name AS name,
                    Code AS code,
                    Summary as summary,
                    Description as description,
                    Price AS price,
                    IsActived AS is_actived,
                    IsDeleted AS is_deleted,
                    CAST(CreatedAt AS CHAR) AS created_at
                FROM product
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

def get_product_by_id(id: int):
    
    try:

        with engine.connect() as connection:
            
            query = '''
                SELECT
                    ProductID AS id,
                    CategoryID AS category_id,
                    Name AS name,
                    Code AS code,
                    Price AS price,
                    IsActived AS is_active,
                    IsDeleted AS is_deleted,
                    CAST(CreatedAt AS CHAR) AS created_at
                FROM product
                WHERE 
                    ProductID = %s
                    AND IsDeleted = 0
            '''
            values = (id,)
            result = connection.exec_driver_sql(query, values).fetchone()

            return False if result is None else dict(result._mapping)
        
    except Exception as e:

        logger.debug(msg=str(e))
        return None
    
def get_product_by_code(code: str):

    try:

        with engine.connect() as connection:
            
            query = '''
                SELECT
                    ProductID AS id,
                    CategoryID AS category_id,
                    Name AS name,
                    Code AS code,
                    Price AS price,
                    IsActived AS is_active,
                    IsDeleted AS is_deleted,
                    CAST(CreatedAt AS CHAR) AS created_at
                FROM product
                WHERE 
                    Code = %s
                    AND IsDeleted = 0
            '''
            values = (code,)
            result = connection.exec_driver_sql(query, values).fetchone()

            return False if result is None else dict(result._mapping)
        
    except Exception as e:

        logger.debug(msg=str(e))
        return None

def create_product(category_id: int, name: str, code: str, price: float, summary: str, description: str):
    
    try:
        with engine.connect() as connection:

            query = '''
                INSERT INTO product
                (
                CategoryID,
                Name,
                Code,
                Price,
                Summary,
                Description
                )
                values
                (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                )
            '''

            values = (category_id, name.title(), code.upper(), round(price, 2), summary, description)
            
            result = connection.exec_driver_sql(query, values)

            if result.rowcount > 0:
                connection.commit()
                return True
    
    except Exception as e:

        logger.debug(msg=str(e))
        return None
    
def update_product(id: int, category_id: int, name: str, price: float, summary: str, description: str):
    try:
        with engine.connect() as connection:

            query = '''
                UPDATE product SET
                CategoryID = %s,
                Name = %s,
                Price = %s,
                Summary = %s,
                Description = %s
                WHERE
                    ProductID = %s
            '''

            values = (category_id, name.title(), round(price, 2), summary, description, id)
            
            result = connection.exec_driver_sql(query, values)

            if result.rowcount > 0:
                connection.commit()
                return True
    
    except Exception as e:

        logger.debug(msg=str(e))
        return None
    
def delete_product(id: int):

    try:
        with engine.connect() as connection:

            query = '''
                UPDATE product SET
                IsDeleted = 1,
                IsActived = 0
                WHERE
                    ProductID = %s
            '''

            values = (id,)
            
            result = connection.exec_driver_sql(query, values)

            if result.rowcount > 0:
                connection.commit()
                return True

    except Exception as e:

        logger.debug(msg=str(e))
        return None

def get_product_comments(id: int):
    
    try:
        with engine.connect() as connection:

            query = '''
                SELECT
                    c.CommentID as comment_id,
                    c.Comment as comment,
                    u.Fullname as user_fullname,
                    u.Email as user_email
                FROM comment as c
                INNER JOIN user as u
                ON
                    c.UserID = u.UserID
                INNER JOIN product as p
                ON
                    c.ProductID = p.ProductID
                WHERE
                    c.ProductID = %s
            '''

            values = (id,)
            
            result = connection.exec_driver_sql(query, values)
    
            return [dict(item._mapping) for item in result]

    except Exception as e:

        logger.debug(msg=str(e))
        return None