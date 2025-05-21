# agent-api-main/app/models/search.py
from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.icp import ICPData

class SearchRequestDTO(BaseModel):
    icp_data: ICPData = Field(..., description="The Ideal Customer Profile to base the search on.")

class Profile(BaseModel):
    name: str = Field(..., description="Full name of the individual.")
    title: str = Field(..., description="Job title of the individual.")
    company: str = Field(..., description="Company the individual works for.")
    location: str = Field(..., description="Location of the individual or company.")
    industry: Optional[str] = Field(default=None, description="Industry of the company.")
    summary: Optional[str] = Field(default=None, description="A brief summary or bio of the individual/company.")
    # Add other relevant fields as needed, e.g., contact_info, company_url, linkedin_url (if available)

class SearchResponseDTO(BaseModel):
    found_profiles: List[Profile] = Field(default_factory=list, description="List of profiles found matching the ICP.")
    message: Optional[str] = Field(default=None, description="Optional message, e.g., if no profiles were found.")