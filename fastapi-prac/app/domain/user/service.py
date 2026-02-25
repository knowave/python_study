from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.domain.user.model import User
from app.domain.user.repository import UserRepository, UserRepositoryInterface
from app.domain.user.schema import UserCreateRequest, UserUpdateRequest


class UserService:
    """
    User 도메인 비즈니스 로직 담당 클래스.
    
    단일 책임 원칙(SRP): 비즈니스 로직만 담당.
    DB 접근은 Repository에, HTTP 처리는 Router에 위임.
    
    의존성 역전 원칙(DIP): 구현체(UserRepository)가 아닌
    인터페이스(UserRepositoryInterface)에 의존.
    테스트 시 Mock Repository로 쉽게 교체 가능.
    """

    def __init__(self, repository: UserRepositoryInterface) -> None:
        self._repository = repository

    async def get_user(self, user_id: int) -> User:
        user = await self._repository.find_by_id(user_id)
        if user is None:
            raise ValueError(f"사용자를 찾을 수 없습니다. id={user_id}")
        return user

    async def get_all_users(self) -> list[User]:
        return await self._repository.find_all()

    async def create_user(self, request: UserCreateRequest) -> User:
        # 이메일 중복 검사
        existing = await self._repository.find_by_email(request.email)
        if existing is not None:
            raise ValueError(f"이미 사용 중인 이메일입니다. email={request.email}")

        new_user = User(
            email=request.email,
            name=request.name,
            hashed_password=hash_password(request.password),
        )
        return await self._repository.save(new_user)

    async def update_user(self, user_id: int, request: UserUpdateRequest) -> User:
        user = await self.get_user(user_id)
        user.name = request.name
        return await self._repository.save(user)

    async def delete_user(self, user_id: int) -> None:
        user = await self.get_user(user_id)
        await self._repository.delete(user)


def get_user_service(session: AsyncSession) -> UserService:
    """
    UserService 인스턴스를 생성해주는 팩토리 함수.
    
    FastAPI의 Depends()와 함께 사용되어 의존성 주입을 담당.
    Spring의 @Bean 메서드와 유사한 역할.
    """
    repository = UserRepository(session)
    return UserService(repository)
