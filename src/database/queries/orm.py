from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy import select
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload

from src.database.database import async_engine
from src.database.database import async_session
from src.database.database import Base
from src.database.models import Resume
from src.database.models import Vacancy
from src.database.models import VacancyReply
from src.database.models import Worker
from src.database.models import WorkType
from src.database.schemas import ResumesRelVacanciesRepliedWithoutVacancyCompensationDTO
from src.database.schemas import VacanciesAddDTO
from src.database.schemas import WorkerRelDTO


class AsyncORM:
    """ALL ORM METHODS."""

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_worker():
        async with async_session() as session:
            worker_1 = Worker(first_name="Sergei", last_name="Isakov", sex="male")
            worker_2 = Worker(first_name="Veniamin", last_name="Alolov", sex="male")
            worker_3 = Worker(first_name="Ivan", last_name="Sulikov", sex="male")
            worker_4 = Worker(first_name="Lera", last_name="Samoylova", sex="female")
            session.add_all([worker_1, worker_2, worker_3, worker_4])
            await session.commit()

    @staticmethod
    async def insert_resumes():
        async with async_session() as session:
            resume_1 = Resume(
                worker_id=1,
                title="DJANGO Python Разработчик",
                salary=80000,
                specialization="Программист, разработчик",
                employment="full_time",
                experience=1,
                work_type="remote",
            )
            resume_2 = Resume(
                worker_id=1,
                title="Отдел по продажам",
                salary=30000,
                specialization="Связист",
                employment="part_time",
                experience=5,
                work_type="remote",
            )
            resume_3 = Resume(
                worker_id=2,
                title="Frontend Разработчик CSS/HTML/JS",
                salary=30000,
                specialization="Программист, разработчик",
                employment="full_time",
                experience=1,
                work_type="combined",
            )
            resume_4 = Resume(
                worker_id=3,
                title="Слесарь",
                salary=30000,
                specialization="Слесарь",
                employment="part_time",
                experience=1,
                work_type="office",
            )
            resume_5 = Resume(
                worker_id=4,
                title="DJANGO + FastAPI Python Разработчик",
                salary=200000,
                specialization="Программист, разработчик",
                employment="full_time",
                experience=8,
                work_type="combined",
            )
            session.add_all([resume_1, resume_2, resume_3, resume_4, resume_5])
            await session.commit()

    @staticmethod
    async def select_worker_resumes():
        async with async_session() as session:
            stmt = select(Worker).options(selectinload(Worker.resume))
            res = await session.execute(stmt)
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
            vacancy_reply_1 = VacancyReply(
                resume_id=1,
                vacancy_id=1,
                cover_letter="Здравствуйте, буду рад присоединиться к вам в команду",
            )
            session.add(vacancy_reply_1)
            await session.commit()

    @staticmethod
    async def select_vacancy_replies():
        async with async_session() as session:
            stmt = select(Resume).join(Resume.vacancy_replied)
            res = await session.execute(stmt)
            result = res.unique().scalars().all()
            print(result[0])

    @staticmethod
    async def convert_workers_to_dto():
        async with async_session() as session:
            stmt = select(Worker).options(selectinload(Worker.resume))
            res = await session.execute(stmt)
            result = res.scalars().all()
            print(f"{result=}")
            result_dto = [
                WorkerRelDTO.model_validate(row, from_attributes=True) for row in result
            ]
            print(f"{result_dto=}")
            return result_dto

    @staticmethod
    async def convert_workers_with_options_to_dto(
        specialization: str, experience, work_type: WorkType
    ):
        async with async_session() as session:
            d = {
                "no experience": [0, 0],
                "from 1 to 3 years": [1, 3],
                "from 3 to 6 years": [3, 6],
                "greater 6 years": [6, 100],
            }
            n1, n2 = 0, 100
            if experience is not None:
                n1, n2 = d.get(experience.value)[0], d.get(experience.value)[1]
            if any([specialization, experience, work_type]):
                if work_type and experience and specialization:
                    stmt = (
                        select(Worker)
                        .join(Worker.resume)
                        .options(contains_eager(Worker.resume))
                        .filter(
                            and_(
                                Resume.experience.between(n1, n2),
                                Resume.work_type == work_type,
                                Resume.specialization == specialization,
                            ),
                        )
                    )
                elif work_type and experience:
                    stmt = (
                        select(Worker)
                        .join(Worker.resume)
                        .options(contains_eager(Worker.resume))
                        .filter(
                            and_(
                                Resume.experience.between(n1, n2),
                                Resume.work_type == work_type,
                            ),
                        )
                    )
                elif work_type and specialization:
                    stmt = (
                        select(Worker)
                        .join(Worker.resume)
                        .options(contains_eager(Worker.resume))
                        .filter(
                            and_(
                                Resume.specialization == specialization,
                                Resume.work_type == work_type,
                            ),
                        )
                    )
                elif specialization and experience:
                    stmt = (
                        select(Worker)
                        .join(Worker.resume)
                        .options(contains_eager(Worker.resume))
                        .filter(
                            and_(
                                Resume.specialization == specialization,
                                Resume.experience.between(n1, n2),
                            ),
                        )
                    )

                elif work_type or experience or specialization:
                    stmt = (
                        select(Worker)
                        .join(Worker.resume)
                        .options(contains_eager(Worker.resume))
                        .filter(
                            or_(
                                Resume.specialization == specialization,
                                Resume.work_type == work_type,
                                Resume.experience.between(n1, n2),
                            ),
                        )
                    )
            else:
                stmt = (
                    select(Worker)
                    .join(Worker.resume)
                    .options(contains_eager(Worker.resume))
                )
            res = await session.execute(stmt)
            result = res.unique().scalars().all()
            print(f"{result=}")
            result_dto = [
                WorkerRelDTO.model_validate(row, from_attributes=True) for row in result
            ]
            print(f"{result_dto=}")
            return result_dto

    @staticmethod
    async def creation_resume_for_worker_post(
        title: str,
        salary: int,
        specialization: str,
        employment: str,
        experience: str,
        work_type: str,
    ):
        async with async_session() as session:
            resume_1 = Resume(
                worker_id=2,
                title=title,
                salary=salary,
                specialization=specialization,
                employment=employment,
                experience=experience,
                work_type=work_type,
            )
            session.add(resume_1)
            await session.commit()

    @staticmethod
    async def add_vacancies_and_replies(title: str, salary: int):
        async with async_session() as session:
            vacancy = Vacancy(title=title, salary=salary)
            get_resume = (
                select(Resume)
                .options(selectinload(Resume.vacancy_replied))
                .filter_by(id=1)
            )
            get_resume2 = (
                select(Resume)
                .options(selectinload(Resume.vacancy_replied))
                .filter_by(id=2)
            )
            resume_1 = (await session.execute(get_resume)).scalar_one()
            resume_2 = (await session.execute(get_resume2)).scalar_one()
            resume_1.vacancy_replied.append(vacancy)
            resume_2.vacancy_replied.append(vacancy)
            await session.commit()

    @staticmethod
    async def select_vacancies():
        async with async_session() as session:
            stmt = select(Vacancy)
            res = await session.execute(stmt)
            result_orm = res.unique().scalars().all()
            print(f"{result_orm=}")
            result_dto = [
                VacanciesAddDTO.model_validate(row, from_attributes=True)
                for row in result_orm
            ]
            return result_dto

    @staticmethod
    async def select_resumes_with_all_relationships():
        async with async_session() as session:
            stmt = (
                select(Resume)
                .options(joinedload(Resume.worker))
                .options(selectinload(Resume.vacancy_replied).load_only(Vacancy.title))
            )

            res = await session.execute(stmt)
            result_orm = res.unique().scalars().all()
            print(f"{result_orm[0]=}")
            result_dto = [
                ResumesRelVacanciesRepliedWithoutVacancyCompensationDTO.model_validate(
                    row, from_attributes=True
                )
                for row in result_orm
            ]
            print(f"{result_dto[0]=}")
            return result_dto

    # @staticmethod
    # async def select_resumes():
    #     async with async_session() as session:
    #         stmt = (
    #             select(Resume)
    #             .options(joinedload(Resume.worker))
    #             .options(selectinload(Resume.vacancy_replied))
    #         )
    #
    #         res = await session.execute(stmt)
    #         result_orm = res.unique().scalars().all()
    #         print(f"{result_orm[0]=}")
    #         result_dto = [
    #             ResumesRelVacanciesRepliedDTO.model_validate(row, from_attributes=True) for
    #             row in result_orm]
    #         print(f"{result_dto[0]=}")
    #         return result_dto
