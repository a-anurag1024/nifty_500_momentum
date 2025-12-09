from pydantic import BaseModel, Field, field_validator
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
    published_raw: str = Field(alias="published") # The raw string from RSS
    published_dt: Optional[datetime] = None       # The parsed datetime object

    @field_validator('published_dt', mode='before')
    @classmethod
    def parse_date(cls, v, values):
        """
        Auto-parses the raw date string into a Python datetime object
        upon initialization.
        """
        # If already a datetime, return it
        if isinstance(v, datetime):
            return v
            
        # If 'published_raw' is available in the input data
        raw_date = values.data.get('published') or values.data.get('published_raw')
        
        if raw_date:
            try:
                # dateutil handles "Mon, 07 Dec 2025..." automatically
                return date_parser.parse(raw_date).replace(tzinfo=None) # naive for simple math
            except Exception:
                return datetime.now() # Fallback
        return datetime.now()

    class Config:
        populate_by_name = True