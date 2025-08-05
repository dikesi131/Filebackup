from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

DB_URL = 'sqlite:///backup.db'

Base = declarative_base()


class HighLevelFiles(Base):  # type: ignore
    __tablename__ = 'HIGH_LEVEL_FILES'
    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    file_path = Column(String)
    file_size = Column(Integer)
    file_hash = Column(String)
    is_new_add = Column(Boolean, default=False)
    is_modified = Column(Boolean, default=False)


class MidLevelFiles(Base):  # type: ignore
    __tablename__ = 'MID_LEVEL_FILES'
    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    file_path = Column(String)
    file_size = Column(Integer)
    is_new_add = Column(Boolean, default=False)


class LowLevelFiles(Base):  # type: ignore
    __tablename__ = 'LOW_LEVEL_FILES'
    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    file_path = Column(String)
    file_size = Column(Integer)


class IsBackuped(Base):  # type: ignore
    __tablename__ = 'IS_BACKUPED'
    id = Column(Integer, primary_key=True)
    # check if the file is backuped
    dst_path = Column(String)
