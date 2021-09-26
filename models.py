import enum
from dataclasses import dataclass
from datetime import datetime
from typing import Type, List, TypeVar, Union

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum, DateTime, Boolean, select, update
from sqlalchemy.orm import relationship, scoped_session, validates

from database import Base

T = TypeVar('T')


def get_all(model: Type[T], db_session: scoped_session) -> List[T]:
    selected = db_session.execute(select(model))

    return selected.scalars().all()


def get_by_id(model: Type[T], db_session: scoped_session, id_: int) -> T:
    selected = db_session.execute(
        select(model).where(model.id == id_)
    )

    return selected.scalar()


def create(model: Type[T], db_session: scoped_session, data: dict) -> T:
    object_ = model(**data)
    db_session.add(object_)
    db_session.commit()

    return object_


def update_by_id(model: Type[T], db_session: scoped_session, id_: int, data: dict) -> Union[T, None]:
    object_ = get_by_id(model, db_session, id_)

    if not object_:
        return

    db_session.execute(
        update(model).where(model.id == id_).values(**data)
    )
    db_session.commit()

    return object_


def delete_by_id(model: Type[T], db_session: scoped_session, id_: int) -> Union[T, None]:
    object_ = get_by_id(model, db_session, id_)

    if not object_:
        return

    db_session.delete(object_)
    db_session.commit()

    return object_


class UserType(enum.Enum):
    patient = 'patient'
    doctor = 'doctor'
    laboratory = 'laboratory'

    def __deepcopy__(self, memo):  # to able to serialize
        return self.value


@dataclass
class User(Base):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    type: UserType

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    type = Column('type', Enum(UserType))

    def __repr__(self):
        return f'<User id: {self.id}, ' \
               f'username: {self.username}, ' \
               f'email: {self.email}, ' \
               f'first_name: {self.first_name}, ' \
               f'last_name: {self.last_name}, ' \
               f'type: {self.type.value}>'

    # Doesn't work on update
    @validates('username')
    def validates_username(self, key, value):
        if self.username and self.username != value:
            raise ValueError('Username cannot be modified')

        return value


class Laboratory(Base):
    __tablename__ = 'laboratory'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    address = Column(String(100))

    def __repr__(self):
        return f'<Laboratory {self.name}>'


class Analysis(Base):
    __tablename__ = 'analysis'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    laboratory_id = Column(Integer, ForeignKey('laboratory.id'))
    timestamp = Column(DateTime, default=datetime.now)

    user = relationship('User', backref='analyses')
    laboratory = relationship('Laboratory', backref='analyses')

    def __repr__(self):
        return f'<Analysis of {self.user.username}>'


class TestStatus(enum.Enum):
    created = 'created'
    processing = 'processing'
    done = 'done'


class Test(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True)
    analysis_id = Column(Integer, ForeignKey('analysis.id'))
    value = Column(Float)
    result = Column(Boolean, nullable=True)
    status = Column('status', Enum(TestStatus))

    analysis = relationship('Analysis', backref='tests')
    parameters = relationship('TestParameter', back_populates='test')

    def __repr__(self):
        return f'<Test for analysis {self.analysis.id}>'


class ParameterType(enum.Enum):
    int = 'int'
    int_bool = 'int_bool'


class Parameter(Base):
    __tablename__ = 'parameter'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    description = Column(String(300))
    type = Column('type', Enum(ParameterType))

    tests = relationship('TestParameter', back_populates='parameter')

    def __repr__(self):
        return f'<Parameter {self.name}>'


class TestParameter(Base):
    __tablename__ = 'test_parameter'

    test_id = Column(Integer, ForeignKey('test.id'), primary_key=True)
    parameter_id = Column(Integer, ForeignKey('parameter.id'), primary_key=True)

    test = relationship('Test', back_populates='parameters')
    parameter = relationship('Parameter', back_populates='tests')

    def __repr__(self):
        return f'<Parameter {self.parameter.name} for test {self.test.id}>'


class Sharing(Base):
    __tablename__ = 'sharing'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('user.id'))
    viewer_id = Column(Integer, ForeignKey('user.id'))
    analysis_id = Column(Integer, ForeignKey('analysis.id'))

    analysis = relationship('Analysis', backref='sharings')
    owner = relationship('User', backref='owner_sharings', foreign_keys=[owner_id])
    viewer = relationship('User', backref='viewer_sharings', foreign_keys=[viewer_id])

    def __repr__(self):
        return f'<{self.owner.username} shared analysis {self.analysis.id} with {self.viewer.username}>'
