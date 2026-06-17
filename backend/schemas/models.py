from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# General Response
class HealthResponse(BaseModel):
    status: str
    version: str
    message: str

# District Schemas
class DistrictBase(BaseModel):
    district_name: str = Field(..., alias='District Names')
    state: str = Field(..., alias='State/UT')
    cluster_id: int = Field(..., alias='Cluster')

class DistrictDetail(DistrictBase):
    indicators: Dict[str, float]

class DistrictListResponse(BaseModel):
    total: int
    districts: List[DistrictBase]

# Cluster Schemas
class ClusterBase(BaseModel):
    cluster_id: int
    name: str

class ClusterComparison(BaseModel):
    indicator: str
    cluster_0_mean: float
    cluster_1_mean: float
    cluster_2_mean: float
    cluster_0_zscore: float
    cluster_1_zscore: float
    cluster_2_zscore: float

class ClusterDetail(ClusterBase):
    total_districts: int
    comparison: List[ClusterComparison]

class ClusterListResponse(BaseModel):
    total: int
    clusters: List[ClusterDetail]

# State Schemas
class StateDistribution(BaseModel):
    state_name: str
    total_districts: int
    cluster_0_count: int
    cluster_1_count: int
    cluster_2_count: int
    cluster_0_pct: float
    cluster_1_pct: float
    cluster_2_pct: float

class StateListResponse(BaseModel):
    total: int
    states: List[StateDistribution]
