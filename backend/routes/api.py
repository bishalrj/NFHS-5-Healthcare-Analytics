from fastapi import APIRouter
from backend.schemas.models import (
    HealthResponse,
    DistrictListResponse,
    DistrictDetail,
    StateListResponse,
    StateDistribution,
    ClusterListResponse,
    ClusterDetail
)
from backend.services.data_service import data_service

router = APIRouter()

@router.get("/", response_model=HealthResponse, tags=["System"])
def root():
    return {
        "status": "online",
        "version": "1.0",
        "message": "NFHS-5 Healthcare Analytics API"
    }

@router.get("/districts", response_model=DistrictListResponse, tags=["Districts"])
def get_districts():
    records = data_service.get_all_districts()
    return {"total": len(records), "districts": records}

@router.get("/district/{district_name}", response_model=DistrictDetail, tags=["Districts"])
def get_district(district_name: str):
    record = data_service.get_district_by_name(district_name)
    return record

@router.get("/states", response_model=StateListResponse, tags=["States"])
def get_states():
    records = data_service.get_all_states()
    return {"total": len(records), "states": records}

@router.get("/state/{state_name}", response_model=StateDistribution, tags=["States"])
def get_state(state_name: str):
    record = data_service.get_state_by_name(state_name)
    return record

@router.get("/clusters", response_model=ClusterListResponse, tags=["Clusters"])
def get_clusters():
    records = data_service.get_all_clusters()
    return {"total": len(records), "clusters": records}

@router.get("/cluster/{cluster_id}", response_model=ClusterDetail, tags=["Clusters"])
def get_cluster(cluster_id: int):
    record = data_service.get_cluster_by_id(cluster_id)
    return record
