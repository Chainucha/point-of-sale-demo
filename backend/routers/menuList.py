from sqlmodel import SQLModel, Field, select
from fastapi import APIRouter, Depends, HTTPException
from db import SessionDep


# Base model
class MenuListBase(SQLModel):
    menu_name: str = Field(default=None, unique=True, index=True)
    category: str | None = Field(default=None)
    price: float | None = Field(default=None)
    status: bool = Field(default=False)


# Table model
class MenuList(MenuListBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


# Create model
class MenuListCreate(MenuListBase):
    pass


# Public (read/response) model
class MenuListPublic(MenuListBase):
    id: int


# Update model (all fields optional)
class MenuListUpdate(SQLModel):
    menu_name: str | None = None
    category: str | None = None
    price: float | None = None
    status: bool | None = None


router = APIRouter()


@router.get("/menu-list")
def list_menu(session: SessionDep):
    return session.exec(select(MenuList)).all


@router.get("/menu-list/{id}", response_model=MenuListPublic)
def get_menu_by_id(session: SessionDep, id: int):
    statement = session.exec(select(MenuList).where(MenuList.id == id)).first()
    if not statement:
        raise HTTPException(status_code=404, detail="Menu not found")
    else:
        return statement


@router.post("/add-menu/", response_model=MenuListPublic)
def add_menu(new_menu: MenuListCreate, session: SessionDep):
    session.add(new_menu)
    session.commit()
    session.refresh()

    return {"message": "success", "menu": new_menu}

@router.put("/modify-menu/{menu_id}")
def modify_menu(menu_id: int, session: SessionDep)
    statement = session.exec(select(MenuList).where(MenuList.id == menu_id))
    if not statement:
        raise HTTPException(status_code=404, detail= "Menu not found")
    menu_data = statement.model_dump(exclude_unset=True)
    for key, value in menu_data.items():
        setattr(menu_data, key, value)
    
    session.add(menu_data)
    session.commit()
    session.refresh(menu_data)
    
    return menu_data

@router.delete("/delete-menu/{menu_id}")
def delete_menu(menu_id: int, session: SessionDep)
    statement = session.exec(select(MenuList).where(MenuList.id == menu_id))
    if not statement:
        raise HTTPException(status_code=404, detail="Menu not found")
    session.delete(statement)
    session.commit()
    return {"Message" : "Success",
            "deleted_cashier" : statement}