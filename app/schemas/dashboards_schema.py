from pydantic import BaseModel
from typing import List, Optional

class DataPoint(BaseModel):
    dimensions: List[str]
    dimensionMap: dict
    timestamps: List[int]
    values: List[float]

class ResultItem(BaseModel):
    metricId: str
    dataPointCountRatio: float
    dimensionCountRatio: float
    data: List[DataPoint]

class DynatraceResponse(BaseModel):
    totalCount: int
    nextPageKey: Optional[str]
    resolution: str
    warnings: Optional[List[str]]
    result: List[ResultItem]
