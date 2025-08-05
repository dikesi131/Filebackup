import hashlib


class FileHasher:
    def __init__(self):
        # default chunk size is 8192 bytes
        self.chunk_size = 8192

    def calculate_md5(self, file_path: str) -> str:
        '''
        Calculate the md5 hash of a file
        param file_path: The path of the file
        return: The md5 hash of the file
        '''
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            while chunk := f.read(self.chunk_size):
                md5.update(chunk)
        return md5.hexdigest()
