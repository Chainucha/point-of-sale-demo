from fastapi import APIRouter,HTTPException
from sqlmodel import Field, Session, SQLModel, select
from db import SessionDep


class CashierBase(SQLModel):
    location_name: str | None = Field(default= None)

class Cashier(CashierBase, table = True):
    id: int = Field(index= True, primary_key= True)

class CashierPublic(CashierBase):
    id: int

class CashierCreate(CashierBase):
    pass

class CashierUpdate(SQLModel):
    location_name: str | None = None
    current_operation_state: bool = Field(default= False)


router = APIRouter()



@router.get("/cashiers-list") # Return all listed cashiers
def list_cashiers(session: SessionDep):
    return session.exec(select(Cashier)).all()

@router.get("/cashiers/{cashier_id}", response_model= CashierPublic)
def cashier_by_id(cashier_id: int, session: SessionDep)
    target_cashier = session.exec(select(Cashier).where(Cashier.id == cashier_id)).first()
    if not target_cashier :
        raise HTTPException(status_code= 404, detail="Cashier not found")
    else:
        return target_cashier

@router.post("/add-cashier") # Insert new cashier to Database
def add_cashier(cashier: CashierCreate,session: SessionDep):
    new_cashier = cashier
    session.add(new_cashier)
    session.commit()
    session.refresh(new_cashier)
    return {"Message" : "Success",
            "cashier" : new_cashier}

@router.put("/modify-cashier/{cashier_id}") # Modify cashier and return new object
def modify_cashier(cashier_id: int,cashier: CashierUpdate, session: SessionDep):
    # Fetch the cashier
    target_cashier = session.exec(select(Cashier).where(Cashier.id == cashier_id)).first()
    
    if not target_cashier:
        raise HTTPException(status_code=404, detail="Cashier not found")
    
    # Update only provided fields
    cashier_data = cashier.model_dump(exclude_unset=True)
    for key, value in cashier_data.items():
        setattr(target_cashier, key, value)
    
    session.add(target_cashier)
    session.commit()
    session.refresh(target_cashier)
    
    return target_cashier

@router.delete("/delete-cashier/{cashier_id}", response_model= CashierPublic)
def delete_cashier(casheir_id: int,session: SessionDep):
    target_cashier = session.exec(select(Cashier).where(Cashier.id == casheir_id)).first()
    if not target_cashier :
        raise HTTPException(status_code= 404, detail = "Cashier not found")
    session.delete(target_cashier)
    session.commit()
    return {"Message" : "Success",
            "deleted_cashier" : target_cashier}