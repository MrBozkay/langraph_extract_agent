"""
Pydantic models for structured data extraction.
"""
from pydantic import BaseModel, Field
from typing import Optional


class CompanyInfoLite(BaseModel):
    """
    German business information schema for Impressum/About extraction.
    
    Designed to extract key business details from German websites,
    particularly from Impressum (legal notice) and About Us pages.
    """
    owner_name: str = Field(
        default="",
        description="Name of the business owner or primary contact person"
    )
    position: str = Field(
        default="",
        description="Position/title (e.g., Geschäftsführer, Inhaber, Zahnärztin)"
    )
    company_name: str = Field(
        default="",
        description="Official company name (e.g., Mustermann GmbH)"
    )
    email: str = Field(
        default="",
        description="Primary contact email (prioritize personal over generic)"
    )
    phone: str = Field(
        default="",
        description="Primary phone number"
    )
    fax: str = Field(
        default="",
        description="Fax number if available"
    )
    website: str = Field(
        default="",
        description="Company website URL"
    )
    profession: str = Field(
        default="",
        description="Professional qualification (e.g., Dr. med. dent., Rechtsanwalt)"
    )
    sector: str = Field(
        default="",
        description="Business sector (e.g., Dentistry, Legal, Consulting)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "owner_name": "Hans Müller",
                "position": "Geschäftsführer",
                "company_name": "Mustermann GmbH",
                "email": "h.mueller@mustermann.de",
                "phone": "+49 123 456789",
                "fax": "+49 123 456788",
                "website": "www.mustermann.de",
                "profession": "",
                "sector": "Consulting"
            }
        }
