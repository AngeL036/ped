from pydantic_settings import BaseSettings
from pydantic import Field



class Setting(BaseSettings):
    db_user: str = Field(...,env="DB_USER")
    db_password: str = Field(...,env="DB_PASSWORD")
    db_host: str = Field(...,env="DB_HOST")
    db_port: int = Field(...,env="DB_PORT")
    db_name: str = Field(...,env="DB_NAME")

    #JWT
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    jwt_expire_minutes: int = Field(60, env="JWT_EXPIRE_MINUTES")

    @property
    def database_url(self) -> str:
        return(
            f"mysql+pymysql://{self.db_user}:"
            f"{self.db_password}@"
            f"{self.db_host}:"
            f"{self.db_port}/"
            f"{self.db_name}"
        )
    class Config:
        env_file = ".env"
        
settings = Setting()