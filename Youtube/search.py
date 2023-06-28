from api import engine

with engine as connection:
    with engine.cursor() as cursor