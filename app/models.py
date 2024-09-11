from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class Order(Base):
    __tablename__ = 'orders'

    id_order = Column(Integer, primary_key=True, index=True)
    customerId = Column(Integer, nullable=False)
    createdAt = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    status = Column(Integer, nullable=False)

    # Relation pour accéder aux produits de la commande
    order_products = relationship("OrderProduct", back_populates="order")

class OrderProduct(Base):
    __tablename__ = 'order_products'

    id_order_products = Column(Integer, primary_key=True, index=True)
    productId = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    id_order = Column(Integer, ForeignKey('orders.id_order'))

    # Relation pour accéder à la commande
    order = relationship("Order", back_populates="order_products")