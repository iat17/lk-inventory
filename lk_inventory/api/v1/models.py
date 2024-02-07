from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)


class User(BaseModel):
    __tablename__ = 'user'

    user_id = sa.Column(sa.String, nullable=False)
    password = sa.Column(sa.LargeBinary, nullable=False)
    phone = sa.Column(sa.String(50), nullable=False)
    email = sa.Column(sa.String(length=50), nullable=False, unique=True)
    name = sa.Column(sa.String(length=50), nullable=False)
    last_name = sa.Column(sa.String(length=70), nullable=False)
    updated_at = sa.Column(sa.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)

    account = relationship(
        'Account', back_populates='user'
    )


class Account(BaseModel):
    __tablename__ = 'account'

    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    balance = sa.Column(sa.Float, nullable=False, default=0)

    user = relationship('User', back_populates='account')
    services = relationship('ServiceAccountLink', back_populates='account',
                            lazy='joined', order_by='ServiceAccountLink.updated_at.desc()')


class Service(BaseModel):
    __tablename__ = 'service'

    name = sa.Column(sa.String(150), nullable=False)
    description = sa.Column(sa.Text, nullable=True)

    plans = relationship('Plan', back_populates='service', lazy='joined')
    service_account_link = relationship('ServiceAccountLink', back_populates='service_details')


class ServiceAccountLink(BaseModel):
    __tablename__ = 'service_account_link'
    __table_args__ = (UniqueConstraint('service_id', 'account_id', 'plan_id', name='_service_account_uc'),
                      UniqueConstraint('service_id', 'account_id', name='_service_uc'))

    service_id = sa.Column(sa.Integer, sa.ForeignKey(Service.id), nullable=False)
    account_id = sa.Column(sa.Integer, sa.ForeignKey(Account.id), nullable=False)
    updated_at = sa.Column(sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    plan_id = sa.Column(sa.ForeignKey('plan.id'), nullable=False)

    service_details = relationship('Service', back_populates='service_account_link', lazy='joined')
    account = relationship('Account', back_populates='services')


class Plan(BaseModel):
    __tablename__ = 'plan'

    name = sa.Column(sa.String(150), nullable=False)
    price = sa.Column(sa.Integer, nullable=False)
    service_id = sa.Column(sa.ForeignKey(Service.id), nullable=False)

    service = relationship('Service', back_populates='plans')
