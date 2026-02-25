from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    애플리케이션 전역 설정 클래스.
    
    pydantic-settings가 .env 파일을 자동으로 읽어서 각 필드에 매핑. 
    Spring의 @ConfigurationProperties와 동일한 역할.
    
    타입 힌트를 통해 잘못된 타입의 환경변수가 들어오면
    실행 시점에 바로 에러를 발생. (타입 안전성)
    """
    DATABASE_HOST: str
    DATABASE_PORT: int = 3306
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def database_url(self) -> str:
        """동기 드라이버용 URL (Alembic 마이그레이션에 사용)"""
        return (
            f"mysql+pymysql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    @property
    def async_database_url(self) -> str:
        """비동기 드라이버용 URL (실제 애플리케이션에서 사용)"""
        return (
            f"mysql+aiomysql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    model_config = SettingsConfigDict(env_file=".env")


# 애플리케이션 전체에서 공유하는 싱글톤 인스턴스
settings = Settings()
