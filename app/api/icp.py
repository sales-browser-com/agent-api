from fastapi import APIRouter

from app.models.icp import GenerateICPDTO
from app.services.icp import generate_icp_service

router = APIRouter()

@router.post('/generate')
async def generate_icp(icp_data: GenerateICPDTO):
    return await generate_icp_service(icp_data)

