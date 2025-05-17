from fastapi import APIRouter

from app.models.icp import GenerateICPDTO
from app.services.icp import generate_icp_service

router = APIRouter()

@router.post('/generate')
async def generate_icp(generate_icp_dto: GenerateICPDTO):
    return await generate_icp_service(generate_icp_dto.messages, generate_icp_dto.icp_data)

