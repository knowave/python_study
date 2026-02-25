from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.user.model import User


class UserRepositoryInterface(ABC):
    """
    Repository 인터페이스.
    
    의존성 역전 원칙(DIP) 적용.
    Service가 구체적인 구현체가 아닌 이 인터페이스에만 의존.
    
    Spring의 JpaRepository 인터페이스와 동일한 개념.
    """

    @abstractmethod
    async def find_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def find_all(self) -> list[User]:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete(self, user: User) -> None:
        pass


class UserRepository(UserRepositoryInterface):
    """
    UserRepository 구현체.
    
    단일 책임 원칙(SRP): 오직 DB 접근 담당.
    
    AsyncSession 생성자 주입.
    Spring의 @Autowired EntityManager와 동일한 패턴.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_id(self, user_id: int) -> Optional[User]:
        result = await self._session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def find_all(self) -> list[User]:
        result = await self._session.execute(select(User))
        return list(result.scalars().all())

    async def find_by_email(self, email: str) -> Optional[User]:
        result = await self._session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def save(self, user: User) -> User:
        self._session.add(user)
        await self._session.flush()  # DB에 반영하되 commit은 하지 않음
        await self._session.refresh(user)  # DB에서 최신 상태로 갱신 (auto increment id 등)
        return user

    async def delete(self, user: User) -> None:
        await self._session.delete(user)
        await self._session.flush()
