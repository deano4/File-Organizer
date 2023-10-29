'''
    Sorts files by name, date, type
'''
from pathlib import Path 
from datetime import datetime

def sort_indiv(sort_func: callable):
    """Gets the file in the given directory"""
    def sort_function(directory: str, *args):
        sorted_files = []
        directory = Path(directory)
        unsorted_files = directory.iterdir()
        unsorted_files = [x for x in unsorted_files if x.is_file()]
        for dir_file in unsorted_files:
            sort_result = sort_func(dir_file, *args)
            if sort_result:
                sorted_files.append(sort_result)
        return sorted_files
    return sort_function


@sort_indiv
def sort_name(dir_file: Path, name: str) -> list[Path]:
    '''Sorts files by name'''
    if name in str(dir_file):
        return dir_file


@sort_indiv
def sort_date(dir_file: Path, date: dict) -> list[Path]:
    '''Sorts files by date'''
    test = True
    file_mt = datetime.fromtimestamp(dir_file.stat().st_mtime)
    file_mt = {
        "day": file_mt.day,
        "month": file_mt.month,
        "year": file_mt.year
    }
    for key, value in date.items():
        if file_mt[key] != value:
            test = False
    if test:
        return dir_file


@sort_indiv
def sort_type(dir_file: Path, extension: str) -> list[Path]:
    '''Sorts by file extension'''
    if dir_file.suffix == extension:
            return dir_file


def sort_group(sort_func: callable):
    '''Creates a sort group function'''
    def sort_function(directory: str, *args):
        sorted_files = {}
        directory = Path(directory)
        unsorted_files = directory.iterdir()
        unsorted_files = [x for x in unsorted_files if x.is_file()]
        for dir_file in unsorted_files:
            sort_result = sort_func(dir_file, *args)
            if sort_result not in sorted_files:
                sorted_files[sort_result] = [dir_file]
            else:
                sorted_files[sort_result].append(dir_file)
        return sorted_files
    return sort_function

@sort_group
def sort_all_date(dir_file: Path) -> dict:
    '''Sort all files by name'''
    file_mt = datetime.fromtimestamp(dir_file.stat().st_mtime)
    file_mt = f"{file_mt.month}/{file_mt.day}/{file_mt.year}"
    return file_mt

@sort_group
def sort_all_type(dir_file: Path) -> dict:
    '''Sort all files by name'''
    return dir_file.suffix 

def organize(folders: dict) -> dict:
    '''Creates folders and organizes files into them'''
    print(folders.values())
    new_paths = {
        "folders": [],
        "files": []
    }
    parent = list(folders.values())[0][0].parent
    for key, value in folders.items():
        # Counter for existing folders with that name
        count = 0
        while True:
            try:
                print(count)
                if count > 0:
                    new_folder = parent / (key + str(count))
                    new_folder.mkdir()
                    new_paths["folders"].append(new_folder)
                    break
                else:
                    new_folder = parent / key
                    new_folder.mkdir()
                    new_paths["folders"].append(new_folder)
                    break
            except:
                count += 1
        for file in value:
            new_path = file.parent / new_folder / file.name
            file.rename(new_path)
            new_paths["files"].append(new_path)
    return new_paths

def undo(folders: dict):
    '''Undo the organization function'''
    parent = folders["folders"][0].parent
    for file in folders["files"]:
        old_path = parent / file.name
        file.rename(old_path)
    for folder in folders["folders"]:
        Path.rmdir(folder)