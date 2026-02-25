from datetime import datetime
from typing import AsyncGenerator

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.config import settings


# 비동기 엔진 생성
# echo=True는 실행되는 SQL을 콘솔에 출력 (개발 시 편리, 운영에선 False)
engine = create_async_engine(
    settings.async_database_url,
    echo=True,
)

# 세션 팩토리 생성
# Spring의 EntityManagerFactory와 동일한 역할
async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # commit 후에도 객체 속성 접근 가능하게 설정
)


class Base(DeclarativeBase):
    """
    모든 Entity 클래스가 상속받을 베이스 클래스.
    Spring의 @Entity + JPA 매핑 설정을 담당하는 역할.
    이 클래스를 상속받아야 SQLAlchemy가 해당 클래스를 테이블로 인식.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    DB 세션을 제공하는 의존성 함수 (Dependency).

    FastAPI의 의존성 주입 시 사용.
    Spring의 @Transactional + EntityManager 주입과 유사한 개념.

    yield 키워드를 사용하면:
    - yield 이전: 세션 생성 (요청 시작)
    - yield: 세션을 Router/Service에 제공
    - yield 이후: 세션 자동 종료 (요청 완료 후)
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
