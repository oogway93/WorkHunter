from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from src.database.database import Base, async_engine, async_session
from src.database.models import Worker, Resume, Vacancy, VacancyReply


class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_worker():
        async with async_session() as session:
            worker_1 = Worker(first_name="Sergei", last_name="Isakov", sex="male")
            session.add(worker_1)
            await session.commit()

    @staticmethod
    async def insert_resumes():
        async with async_session() as session:
            resume_1 = Resume(worker_id=1, title="Python Разработчик",
                              salary=80000, specialization="Программист, разработчик",
                              employment="full_time", experience="1 год",
                              schedule="remote")
            resume_2 = Resume(worker_id=1, title="Отдел по продажам",
                              salary=30000, specialization="Связист",
                              employment="part_time", experience="5 лет",
                              schedule="remote")
            session.add_all([resume_1, resume_2])
            await session.commit()

    @staticmethod
    async def select_worker_resumes():
        async with async_session() as session:
            query = (
                select(Worker)
                .options(selectinload(Worker.resume))
            )
            res = await session.execute(query)
            result = res.unique().scalars().all()
            print(result[0].resume)

    @staticmethod
    async def insert_vacancies():
        async with async_session() as session:
            vacancy_1 = Vacancy(title="Junior Python Разработчик", salary=50000)
            vacancy_2 = Vacancy(title="Слесарь", salary=30000)
            session.add_all([vacancy_1, vacancy_2])
            await session.commit()

    @staticmethod
    async def insert_vacancy_replies():
        async with async_session() as session:
            vacancy_reply_1 = VacancyReply(resume_id=1, vacancy_id=1,
                                           cover_letter="Здравствуйте, буду рад присоединиться к вам в команду")
            session.add(vacancy_reply_1)
            await session.commit()

    @staticmethod
    async def select_vacancy_replies():
        async with async_session() as session:
            query = (
                select(Resume)
                .join(Resume.vacancy_replied)
            )
            res = await session.execute(query)
            result = res.unique().scalars().all()
            print(result[0])