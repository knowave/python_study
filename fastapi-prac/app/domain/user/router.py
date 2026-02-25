from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.domain.auth.router import get_current_user
from app.domain.user.model import User
from app.domain.user.schema import UserCreateRequest, UserUpdateRequest, UserResponse
from app.domain.user.service import UserService, get_user_service

router = APIRouter(
    prefix="/users",  # 모든 엔드포인트에 /users 접두사
    tags=["Users"],   # Swagger UI에서 그룹핑
)


def get_service(session: AsyncSession = Depends(get_db_session)) -> UserService:
    """
    FastAPI 의존성 주입 함수.
    
    Depends()는 Spring의 @Autowired와 동일.
    요청이 들어올 때마다 FastAPI가 자동으로 이 함수를 호출해서
    session → repository → service 순으로 객체 생성.
    """
    return get_user_service(session)


@router.get("", response_model=list[UserResponse])
async def get_all_users(
    service: UserService = Depends(get_service),
    _: User = Depends(get_current_user),
):
    """전체 사용자 목록 조회"""
    return await service.get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_service),
    _: User = Depends(get_current_user),
):
    """특정 사용자 조회"""
    try:
        return await service.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: UserCreateRequest,
    service: UserService = Depends(get_service),
):
    """사용자 생성"""
    try:
        return await service.create_user(request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    request: UserUpdateRequest,
    service: UserService = Depends(get_service),
    _: User = Depends(get_current_user),
):
    """사용자 수정"""
    try:
        return await service.update_user(user_id, request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_service),
    _: User = Depends(get_current_user),
):
    """사용자 삭제"""
    try:
        await service.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
