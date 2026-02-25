from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import engine, Base
from app.domain.auth.router import router as auth_router
from app.domain.user.router import router as user_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    애플리케이션 시작/종료 시 실행되는 이벤트 핸들러.
    Spring의 ApplicationListener나 @PostConstruct/@PreDestroy와 비슷.
    
    yield 이전: 서버 시작 시 실행
    yield 이후: 서버 종료 시 실행
    """
    # 테이블이 없으면 자동 생성 (개발 편의용)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 서버 종료 시 엔진 정리
    await engine.dispose()


app = FastAPI(
    title="FastAPI CRUD",
    description="FastAPI + MySQL CRUD 예제",
    version="1.0.0",
    lifespan=lifespan,
)

# Router 등록 (Spring의 @RequestMapping과 유사)
app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
