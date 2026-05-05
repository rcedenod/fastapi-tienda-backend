from sqlalchemy import create_engine, MetaData, Table
from config import config

# URL de base de datos
DATABASE_URI = config['DATABASE_URI']

# Conexion con la base de datos
engine = create_engine(DATABASE_URI)

meta = MetaData()

# Tablas
product_table = Table('product', meta, autoload_with=engine)

# product_table.select().with_only_columns(product_table.c.Name)

# query = product_table.select().where(product_table.c.IsDeleted == 0)
# a = engine.connect()
# a.execute(query)