from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field, computed_field


class DataConfig(BaseModel):
    """Centralized paths and tunable data settings."""

    model_config = ConfigDict(frozen=True)

    base_dir: Path = Field(default_factory=Path.cwd)
    stock_api_sleep: float = 1.0
    news_api_sleep: float = 2.0
    cache_expiry_hours: int = 24
    stock_file_ext: str = ".parquet"
    news_file_ext: str = ".json"

    @computed_field(return_type=Path)
    def data_dir(self) -> Path:
        return self.base_dir / "data"

    @computed_field(return_type=Path)
    def stock_data_dir(self) -> Path:
        return self.data_dir / "stocks"

    @computed_field(return_type=Path)
    def news_data_dir(self) -> Path:
        return self.data_dir / "news"

    @computed_field(return_type=Path)
    def logs_dir(self) -> Path:
        return self.base_dir / "logs"

    def setup_directories(self) -> None:
        """Ensure required directories exist before IO starts."""
        for path in (self.data_dir, self.stock_data_dir, self.news_data_dir, self.logs_dir):
            path.mkdir(parents=True, exist_ok=True)


DATA_CONFIG = DataConfig()
DATA_CONFIG.setup_directories()

__all__ = ["DataConfig", "DATA_CONFIG"]