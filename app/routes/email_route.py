# app/routes/email_route.py
from typing import List, Optional, Union
from fastapi import APIRouter, HTTPException, Depends, Header, Body
from pydantic import BaseModel, EmailStr, constr
from app.config import settings
from app.email.sender import SMTPSender

router = APIRouter()

class EmailPayload(BaseModel):
    name: constr(min_length=1, max_length=50)
    email: EmailStr
    message: constr(min_length=1, max_length=5000)
    mobile: constr(min_length=10, max_length=15)
    brand: constr(min_length=1)  # e.g., "legalvala" or "brchub"
    services: Optional[Union[List[constr(min_length=1, max_length=100)], constr(min_length=1, max_length=500)]] = None

    def services_text(self) -> Optional[str]:
        if self.services is None:
            return None
        if isinstance(self.services, list):
            return ", ".join(service.strip() for service in self.services if service.strip()) or None
        value = self.services.strip()
        return value or None

def get_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=403, detail="Could not validate API key")
    return x_api_key

@router.post("/send-email/{smtp_provider}")
async def send_email(
    smtp_provider: str,
    payload: EmailPayload = Body(...),
    api_key: str = Depends(get_api_key)
):
    provider_configs = settings.smtp_servers.get(smtp_provider)
    if not provider_configs:
        raise HTTPException(
            status_code=400,
            detail=f"SMTP configuration for provider '{smtp_provider}' not found."
        )
    smtp_config = provider_configs.get(payload.brand.lower())
    if not smtp_config:
        smtp_config = provider_configs.get("default")
        if not smtp_config:
            raise HTTPException(
                status_code=400,
                detail=f"No SMTP configuration found for brand '{payload.brand}' under provider '{smtp_provider}'."
            )

    sender = SMTPSender(smtp_config)
    context = {
        "name": payload.name,
        "message": payload.message,
        "mobile": payload.mobile,
        "email": payload.email,
        "services": payload.services_text()
    }
    subject = "Thank you for contacting our business"
    result = sender.send_email(recipient=payload.email, subject=subject, context=context)
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("message"))
    return result
