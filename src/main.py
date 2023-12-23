import asyncio

from src.database.queries.orm import AsyncORM


async def main():
    await AsyncORM.create_tables()


if __name__ == '__main__':
    asyncio.run(main())
