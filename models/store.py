from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic")
    # benefit: load speed
    # drawback: accessing the items in store isn't as easy
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")

