import os, os.path
import inspect
from file_reader_import import get_cash, get_date, first_word_search, breakdown_file, build_path_list, execute_transfer, final
import pdb

path_list = build_path_list()
execute_transfer(path_list)




