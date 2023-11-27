from sqlalchemy import delete, insert, select, desc, asc
from sqlalchemy.exc import SQLAlchemyError

from src.database import async_session_maker
from src.logger import logger


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, order_by=None, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            if order_by:
                order_by_conditions = []
                for field in order_by:
                    if field.endswith('-'):
                        order_by_conditions.append(desc(field[:-1]))
                    else:
                        order_by_conditions.append(asc(field))

                query = query.order_by(*order_by_conditions)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        try:
            query = insert(cls.model).values(**data).returning(cls.model.id)
            async with async_session_maker() as session:
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: Cannot insert data into table"
            elif isinstance(e, Exception):
                msg = "Unknown Exc: Cannot insert data into table"

            logger.error(msg, extra={"table": cls.model.__tablename__},
                         exc_info=True)
            return None

    @classmethod
    async def delete(cls, **filter_by):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter_by)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def partial_update(cls, id, **data):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=id).with_for_update()
            result = await session.execute(query)
            obj = result.scalar()
            for key, value in data.items():
                setattr(obj, key, value)

            await session.commit()
