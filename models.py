import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship

from database import Base


class UserType(enum.Enum):
    PATIENT = 'PATIENT'
    DOCTOR = 'DOCTOR'
    LABORATORY = 'LABORATORY'


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(50), unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    type = Column('type', Enum(UserType))

    def __repr__(self):
        return f'<User {self.username}>'


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

    user = relationship('User', back_populates='analyses')
    laboratory = relationship('Laboratory', back_populates='analyses')

    def __repr__(self):
        return f'<Analysis of {self.user.username}>'


class TestStatus(enum.Enum):
    CREATED = 'CREATED'
    PROCESSING = 'PROCESSING'
    DONE = 'DONE'


class Test(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True)
    analysis_id = Column(Integer, ForeignKey('analysis.id'))
    value = Column(Float)
    result = Column(Boolean, nullable=True)
    status = Column('status', Enum(TestStatus))

    analysis = relationship('Analysis', back_populates='tests')
    parameter = relationship('TestParameter', back_populates='test')

    def __repr__(self):
        return f'<Test for analysis {self.analysis.id}>'


class ParameterType(enum.Enum):
    INT = 'INT'
    INT_BOOL = 'INT_BOOL'


class Parameter(Base):
    __tablename__ = 'parameter'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    description = Column(String(300))
    type = Column('type', Enum(ParameterType))

    test = relationship('TestParameter', back_populates='parameter')

    def __repr__(self):
        return f'<Parameter {self.name}>'


class TestParameter(Base):
    __tablename__ = 'test_parameter'

    test_id = Column(Integer, primary_key=True)
    parameter_id = Column(Integer, primary_key=True)

    test = relationship('Test', back_populates='parameter')
    parameter = relationship('Parameter', back_populates='test')

    def __repr__(self):
        return f'<Parameter {self.parameter.name} for test {self.test.id}>'


class Sharing(Base):
    __tablename__ = 'sharing'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('user.id'))
    viewer_id = Column(Integer, ForeignKey('user.id'))
    analysis_id = Column(Integer, ForeignKey('analysis.id'))

    analysis = relationship('Analysis', back_populates='sharings')
    owner = relationship('User', back_populates='owner_sharings')
    viewer = relationship('User', back_populates='viewer_sharings')

    def __repr__(self):
        return f'<{self.owner.username} shared analysis {self.analysis.id} with {self.viewer.username}>'
