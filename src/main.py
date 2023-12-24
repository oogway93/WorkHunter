import asyncio
import os
import sys

from src.database.queries.orm import AsyncORM

sys.path.insert(1, os.path.join(sys.path[0], '..'))


async def main():
    await AsyncORM.create_tables()
    await AsyncORM.insert_worker()
    await AsyncORM.insert_resumes()
    await AsyncORM.select_worker_resumes()


if __name__ == '__main__':
    asyncio.run(main())
