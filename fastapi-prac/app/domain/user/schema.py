from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserCreateRequest(BaseModel):
    """
    사용자 생성 요청 DTO.
    Spring의 CreateUserRequest 같은 역할이에요.

    Pydantic BaseModel을 상속받으면:
    - 자동 유효성 검사 (타입 불일치 시 422 에러 반환)
    - JSON 직렬화/역직렬화 자동 처리
    - API 문서 자동 생성 (Swagger)
    """
    email: str
    name: str
    password: str


class UserUpdateRequest(BaseModel):
    """사용자 수정 요청 DTO. 이름만 수정 가능."""
    name: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """
    사용자 응답 DTO.
    
    model_config = ConfigDict(from_attributes=True) 설정이 중요.
    이게 있어야 SQLAlchemy 모델 객체를 이 Pydantic 모델로 변환 가능.
    Spring의 ModelMapper나 MapStruct와 유사한 역할.
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str
    created_at: datetime
    updated_at: datetime
