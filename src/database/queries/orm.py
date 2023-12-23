from src.database.database import session, engine, Base


class AsyncORM:
    @staticmethod
    async def create_tables():
        async with engine.connect() as con:
            await con.run_sync(Base.metadata.drop_all)
            await con.run_sync(Base.metadata.create_all)
