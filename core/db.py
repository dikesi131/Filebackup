from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore
from .setting import Base, HighLevelFiles, MidLevelFiles, \
    LowLevelFiles, DB_URL, IsBackuped
from .global_vars import get_var  # type: ignore
from sqlalchemy.exc import SQLAlchemyError  # type: ignore
from typing import Any, Optional, List, Dict


class DatabaseExec:
    def __init__(self, db_url: str = DB_URL) -> None:
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.g_logger = get_var('g_logger')

    def add_high_level_files(self, files: List[Dict[str, str]]) -> None:
        '''
        Add high level files to database
        param files: List[Dict[str, str]], it contains all high level files
        '''
        session = self.Session()
        try:
            new_files = [HighLevelFiles(**file) for file in files]
            session.bulk_save_objects(new_files)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            self.g_logger.error(f"Error adding high level files: {e}")
        finally:
            session.close()

    def add_mid_level_files(self, files: List[Dict[str, str]]) -> None:
        '''
        Add mid level files to database
        param files: List[Dict[str, str]], it contains all mid level files
        '''
        session = self.Session()
        try:
            new_files = [MidLevelFiles(**file) for file in files]
            session.bulk_save_objects(new_files)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            self.g_logger.error(f"Error adding mid level files: {e}")
        finally:
            session.close()

    def add_low_level_files(self, files: List[Dict]) -> None:
        '''
        Add low level files to database
        param files: List[Dict], it contains all low level files
        '''
        session = self.Session()
        try:
            new_files = [LowLevelFiles(**file) for file in files]
            session.bulk_save_objects(new_files)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            self.g_logger.error(f"Error adding low level files: {e}")
        finally:
            session.close()

    def add_is_backuped(self, file_path: str) -> None:
        '''
        Add a file to is backuped table
        param file_path: str: The path to the file
        '''
        session = self.Session()
        try:
            session.add(IsBackuped(dst_path=file_path))
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            self.g_logger.error(f"Error adding is backuped: {e}")
        finally:
            session.close()

    def get_all_high_file_hashes(self) -> Optional[List[Any]]:
        '''
        Get all high file hashes
        return: list[Any]: A list of all high file hashes
        '''
        session = self.Session()
        try:
            files = session.query(HighLevelFiles).all()
            return [file.file_hash for file in files]
        except SQLAlchemyError as e:
            self.g_logger.error(f"Error getting all high file hashes: {e}")
            return None
        finally:
            session.close()

    def get_all_mid_file_paths(self) -> Optional[List[Any]]:
        '''
        Get all mid file paths
        return: list[Any]: A list of all mid file paths
        '''
        session = self.Session()
        try:
            files = session.query(MidLevelFiles).all()
            return [file.file_path for file in files]
        except SQLAlchemyError as e:
            self.g_logger.error(f"Error getting all mid file paths: {e}")
            return None
        finally:
            session.close()

    def get_all_backuped_dir_paths(self) -> Optional[List[Any]]:
        '''
        Get all backuped files
        return: list[Any]: A list of all backuped files
        '''
        session = self.Session()
        try:
            files = session.query(IsBackuped).all()
            return [file.dst_path for file in files]
        except SQLAlchemyError as e:
            self.g_logger.error(f"Error getting all backuped dir paths: {e}")
            return None
        finally:
            session.close()

    def get_all_high_file_size(self) -> Optional[List[Any]]:
        '''
        Get all high file sizes
        return: list[Any]: A list of all high file sizes
        '''
        session = self.Session()
        try:
            files = session.query(HighLevelFiles).all()
            return [file.file_size for file in files]
        except SQLAlchemyError as e:
            self.g_logger.error(f"Error getting all high file sizes: {e}")
            return None
        finally:
            session.close()

    def get_all_mid_file_size(self) -> Optional[List[Any]]:
        '''
        Get all mid file sizes
        return: list[Any]: A list of all mid file sizes
        '''
        session = self.Session()
        try:
            files = session.query(MidLevelFiles).all()
            return [file.file_size for file in files]
        except SQLAlchemyError as e:
            self.g_logger.error(f"Error getting all mid file sizes: {e}")
            return None
        finally:
            session.close()

    def get_all_high_file_count(self) -> Optional[int]:
        '''
        Get all high file count
        return: int: The count of all high files
        '''
        session = self.Session()
        try:
            return session.query(HighLevelFiles).count()
        except SQLAlchemyError as e:
            self.g_logger.error(f"Error getting all high file count: {e}")
            return None
        finally:
            session.close()

    def get_all_mid_file_count(self) -> Optional[int]:
        '''
        Get all mid file count
        return: int: The count of all mid files
        '''
        session = self.Session()
        try:
            return session.query(MidLevelFiles).count()
        except SQLAlchemyError as e:
            self.g_logger.error(f"Error getting all mid file count: {e}")
            return None
        finally:
            session.close()

    def get_all_modifed_high_files(self) -> Optional[List[Any]]:
        '''
        Get all modified high files
        return: list[Any]: A list of all modified high files
        '''
        session = self.Session()
        try:
            files = session.query(HighLevelFiles).filter_by(is_modified=True).all()  # noqa
            return [file.file_path for file in files]
        except SQLAlchemyError as e:
            self.g_logger.error(f"Error getting all modified high files: {e}")
            return None
        finally:
            session.close()

    def get_all_added_mid_files(self) -> Optional[List[Any]]:
        '''
        Get all added mid files
        return: list[Any]: A list of all added mid files
        '''
        session = self.Session()
        try:
            files = session.query(MidLevelFiles).filter_by(is_new_add=True).all()  # noqa
            return [file.file_path for file in files]
        except SQLAlchemyError as e:
            self.g_logger.error(f"Error getting all added mid files: {e}")
            return None
        finally:
            session.close()

    def update_high_file_hash(self, file_path: str,
                              new_hash: str, is_modfied: bool) -> None:
        '''
        Update high file hash
        param file_path: str: The path to the file
        param new_hash: str: The new hash value
        param is_modfied: bool: Whether the file is modified
        '''
        session = self.Session()
        try:
            file = session.query(HighLevelFiles).filter_by(file_path=file_path).first()  # noqa
            if file:
                # file may be deleted or rename by user
                file.file_hash = new_hash  # type: ignore
                file.is_modified = is_modfied  # type: ignore
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            self.g_logger.error(f"Error updating high file hash: {e}")
        finally:
            session.close()

    def clear_high_level_files(self) -> None:
        session = self.Session()
        try:
            session.query(HighLevelFiles).delete()
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            self.g_logger.error(f"Error clearing high level files: {e}")
        finally:
            session.close()

    def clear_mid_level_files(self) -> None:
        session = self.Session()
        try:
            session.query(MidLevelFiles).delete()
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            self.g_logger.error(f"Error clearing mid level files: {e}")
        finally:
            session.close()

    def clear_low_level_files(self) -> None:
        session = self.Session()
        try:
            session.query(LowLevelFiles).delete()
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            self.g_logger.error(f"Error clearing low level files: {e}")
        finally:
            session.close()
