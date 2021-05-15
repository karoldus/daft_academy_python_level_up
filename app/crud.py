from sqlalchemy.orm import Session

from . import models


def get_shippers(db: Session):
    return db.query(models.Shipper).all()


def get_shipper(db: Session, shipper_id: int):
    return (
        db.query(models.Shipper).filter(models.Shipper.ShipperID == shipper_id).first()
    )

# 5.1
def get_suppliers(db: Session):
    return db.query(models.Supplier.SupplierID, models.Supplier.CompanyName).order_by(models.Supplier.SupplierID).all()


def get_supplier(db: Session, s_id: int):
    return (
        db.query(models.Supplier).filter(models.Supplier.SupplierID == s_id).first()
    )

def get_supplier_products(db: Session, s_id: int):
    return (
        db.query(models.Product).join(models.Supplier, models.Supplier.SupplierID==models.Product.SupplierID).filter(models.Supplier.SupplierID == s_id).order_by(models.Product.ProductID.desc()).all()
    )
