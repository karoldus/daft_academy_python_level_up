from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import get_db

router = APIRouter()


@router.get("/shippers/{shipper_id}", response_model=schemas.Shipper)
async def get_shipper(shipper_id: PositiveInt, db: Session = Depends(get_db)):
    db_shipper = crud.get_shipper(db, shipper_id)
    if db_shipper is None:
        raise HTTPException(status_code=404, detail="Shipper not found")
    return db_shipper


@router.get("/shippers", response_model=List[schemas.Shipper])
async def get_shippers(db: Session = Depends(get_db)):
    return crud.get_shippers(db)


@router.get('/suppliers', status_code=200)
async def suppliers(db: Session = Depends(get_db)):
    return crud.get_suppliers(db)
    

@router.get('/suppliers/{id}', status_code=200)
async def suppliers_id(id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier

# 5.2

@router.get('/suppliers/{id}/products', status_code=200)
async def suppliers_id_products(id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return crud.get_supplier_products(db, id)


# 5.3
@router.post('/suppliers', status_code=201)
async def suppliers_post(json_data: dict, db: Session = Depends(get_db)):
    return crud.post_supplier(json_data, db, id)

# 5.4
@router.put('/suppliers/{id}', status_code=200)
async def suppliers_id_put(json_data: dict, id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    crud.put_supplier(json_data,db, id)
    return crud.get_supplier(db, id)

# 5.5

@router.delete('/suppliers/{id}', status_code=204)
async def suppliers_delete(id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    crud.delete_supplier(db, id)
    return 0


