# agent-api-main/app/api/search.py
from fastapi import APIRouter, HTTPException
from app.models.search import SearchRequestDTO, SearchResponseDTO
from app.services.search import find_profiles_service

router = APIRouter()

@router.post('/find-profiles', response_model=SearchResponseDTO)
async def find_profiles_endpoint(request_dto: SearchRequestDTO):
    """
    Finds profiles based on the provided Ideal Customer Profile (ICP).
    """
    try:
        response = await find_profiles_service(request_dto)
        return response
    except Exception as e:
        # Log the exception e
        print(f"Error in find_profiles_endpoint: {e}") # Basic logging
        raise HTTPException(status_code=500, detail=f"An error occurred while searching for profiles: {str(e)}")