import glob
import os
from typing import List


def get_files(directory: str, extension: str = None) -> List[str]:
    """
    Retorna uma lista de arquivos com a extensão especificada.
    """

    if not os.path.exists(directory):
        print('Directory does not exist')
        return None

    if extension is None:
        extension = '*'

    pattern_fetch = os.path.join(directory, '*.' + extension)
    files = glob.glob(pattern_fetch)

    return files
