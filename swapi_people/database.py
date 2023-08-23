from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.ext.declarative import declarative_base

from common import PG_DSN

engine = create_async_engine(PG_DSN, echo=True)
Base = declarative_base()
Session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
