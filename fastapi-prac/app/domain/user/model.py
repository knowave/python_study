from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    """
    User 테이블과 매핑되는 Entity 클래스.
    
    Spring JPA와 비교:
    - class User(Base) → @Entity
    - __tablename__    → @Table(name = "users")
    - Mapped[str]      → 타입 힌트 기반 컬럼 정의 (@Column)
    - mapped_column()  → 컬럼 상세 옵션 설정
    
    Mapped[T]를 사용하면 타입 안전성 보장
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"
