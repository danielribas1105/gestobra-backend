import uuid
from fastapi import APIRouter, Depends, HTTPException
from app.modules.auth.service import get_current_user
from app.modules.user.model import User
from app.modules.payments.schema import PaymentResponse, PaymentUpdate
from app.modules.payments import service

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.get("/job/{job_id}", response_model=PaymentResponse)
async def get_payment_by_job(job_id: uuid.UUID, user: User = Depends(get_current_user)):
    payment = await service.get_payment_by_job(job_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return payment


@router.patch("/{payment_id}", response_model=PaymentResponse)
async def update_payment(
    payment_id: uuid.UUID,
    data: PaymentUpdate,
    user: User = Depends(get_current_user),
):
    return await service.update_payment(payment_id, data)
