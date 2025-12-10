from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime
from typing import Optional
from dateutil import parser as date_parser

"""
NEWS MODELS
-----------
Standardized data structures for the news pipeline.
"""

class NewsArticle(BaseModel):
    title: str
    link: str
    source: str
    published_raw: str = Field(alias="published")
    published_dt: Optional[datetime] = None

    @model_validator(mode="after")
    def parse_date(self):
        # Already parsed?
        if isinstance(self.published_dt, datetime):
            return self

        raw = self.published_raw
        if raw:
            try:
                self.published_dt = date_parser.parse(raw).replace(tzinfo=None)
            except Exception:
                self.published_dt = datetime.now()
        else:
            self.published_dt = datetime.now()

        return self

    class Config:
        populate_by_name = True
