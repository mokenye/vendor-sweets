# models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from sqlalchemy import MetaData

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Vendor(db.Model,SerializerMixin ):
    __tablename__ = 'vendor'

    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String(255), nullable=False)
    create_at=db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    update_at=db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    vendor_sweets = db.relationship('VendorSweet', back_populates='vendor')

    serialize_rules = ('-vendor_sweets.vendor',)

class Sweet(db.Model,SerializerMixin ):
    __tablename__ = 'sweet'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    vendor_sweets = db.relationship('VendorSweet', back_populates='sweet')

class VendorSweet(db.Model,SerializerMixin ):
    __tablename__ = 'vendor_sweet'

    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    sweet_id = db.Column(db.Integer, db.ForeignKey('sweet.id'), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    vendor = db.relationship('Vendor', back_populates='vendor_sweets')
    sweet = db.relationship('Sweet', back_populates='vendor_sweets')

    serialize_rules = ('-vendor', '-sweet')

    @db.validates('price')
    def validate_price(self, key, value):
        if not value:
            raise ValueError('Price cannot be blank')
        if value < 0:
            raise ValueError("Price can't be negative number")
        return value