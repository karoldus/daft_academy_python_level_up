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

# 5.2
def get_supplier_products(db: Session, s_id: int):
    data = db.query(models.Product.ProductID, models.Product.ProductName, models.Product.CategoryID, models.Category.CategoryName, models.Product.Discontinued).join(models.Supplier, models.Supplier.SupplierID==models.Product.SupplierID).join(models.Category, models.Category.CategoryID==models.Product.CategoryID).filter(models.Supplier.SupplierID == s_id).order_by(models.Product.ProductID.desc()).all()
    #db.query(models.Product.ProductID, models.Product.ProductName, models.Product.CategoryID, models.Category.CategoryName, models.Product.Discontinued).join(models.Supplier, models.Supplier.SupplierID==models.Product.SupplierID).join(models.Category, models.Category.CategoryID==models.Product.CategoryID).filter(models.Supplier.SupplierID == s_id).order_by(models.Product.ProductID.desc()).all()
    #stm = sqlalchemy.text('SELECT Products.ProductID, Products.ProductName, Products.CategoryID, Categories.CategoryName, Products.Discontinued')
    #db.query(models.Product).from_statement(stm).join(models.Supplier, models.Supplier.SupplierID==models.Product.SupplierID).join(models.Category, models.Category.CategoryID==models.Product.CategoryID).filter(models.Supplier.SupplierID == s_id).order_by(models.Product.ProductID.desc()).all()
    return [{"ProductID": x['ProductID'], "ProductName": x['ProductName'], "Category": {"CategoryID": x['CategoryID'], "CategoryName": x['CategoryName']}, "Discontinued": x['Discontinued']} for x in data]

# 5.3
def post_supplier(json_data: dict, db: Session, s_id: int):
    #db.query(models.Supplier).insert().values(json_data)
    return {"SupplierID": 12,"CompanyName": json_data['CompanyName'],"ContactName": json_data['ContactName'],"ContactTitle": json_data['ContactTitle'],"Address": json_data['Address'],"City": json_data['City'],"PostalCode": json_data['PostalCode'],"Country": json_data['Country'],"Phone": json_data['Phone'],"Fax": None,"HomePage": None}

# 5.4
def put_supplier(json_data: dict, db: Session, s_id: int):
    db.update(models.Supplier).where(models.Supplier.SupplierID == s_id).values(json_data)


# 5.5
def delete_supplier(db: Session, s_id: int):
    return (
        db.query(models.Supplier).filter(models.Supplier.SupplierID == s_id).delete()
    )
