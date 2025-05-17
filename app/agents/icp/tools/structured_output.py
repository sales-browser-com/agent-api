from pydantic import BaseModel, Field, constr
from typing import List


class ICPData(BaseModel):
    industries: List[str] = Field(default_factory=list, description="Target industries the agent should focus on when searching for potential customers. Leave empty for a broad search.")
    locations: List[str] = Field(default_factory=list, description="Geographic regions where potential customers should be located. Helps tailor communication based on cultural or timezone relevance.")
    technologiesUsed: List[str] = Field(default_factory=list, description="Specific technologies or tools commonly used by the ideal customers. Helps in identifying companies aligned with your product's ecosystem.")
    businessModels: List[str] = Field(default_factory=list, description="Target company business models (e.g., B2B, SaaS, DTC). Used to ensure the message resonates with how they operate.")
    companyKeywords: List[str] = Field(default_factory=list, description="Words or phrases associated with target companies (e.g., 'bootstrapped', 'growth-stage'). Helps surface niche or ideal organizations.")
    jobTitles: List[str] = Field(default_factory=list, description="Relevant job titles of individuals who should be contacted (e.g., 'Head of Marketing', 'Founder').")
    seniorityLevels: List[str] = Field(default_factory=list, description="Seniority of the target individuals (e.g., 'executive', 'manager'). Used to tailor tone and content of outreach.")
    departments: List[str] = Field(default_factory=list, description="Departments where potential buyers are likely to work (e.g., 'Marketing', 'Product', 'Operations').")
    skillsKeywords: List[str] = Field(default_factory=list, description="Skills found on target individual profiles (e.g., 'cold outreach', 'CRM'). Useful for identifying doers over talkers.")
    responsibilitiesKeywords: List[str] = Field(default_factory=list, description="Day-to-day responsibilities or functions that indicate relevance (e.g., 'lead generation', 'growth strategy').")
    actionTakerSignals: List[str] = Field(default_factory=list, description="Signals that suggest someone takes action rather than just posting (e.g., 'project launched', 'bootstrapped company', 'hiring for X'). Critical for identifying builders.")
    painPointsKeywords: List[str] = Field(default_factory=list, description="Common pain points your product solves (e.g., 'lead quality', 'manual outreach'). Helps personalize the warm-up message.")
    excludedIndustries: List[str] = Field(default_factory=list, description="Industries to avoid in outreach. Helps refine and reduce irrelevant targeting.")
    excludedJobTitles: List[str] = Field(default_factory=list, description="Job titles to exclude from targeting, such as roles not involved in decision-making or irrelevant departments.")
    excludedCompanyKeywords: List[str] = Field(default_factory=list, description="Keywords that, if present in a company's description, should disqualify them from targeting (e.g., 'agency', 'influencer network').")
    excludedIndividualKeywords: List[str] = Field(default_factory=list, description="Disqualifying words found in individual bios or posts (e.g., 'coach', 'guru', 'solopreneur') that signal poor fit.")
