######################################################
######################################################
### Make folders for Test Images for work in server
import shutil
import os
import numpy as np
from PIL import Image
import glob

file_h = 28
file_w = 28
MAX_COUNT_TEST_IMGS = 100

#=== This path is send by up level ===
work_directory = "/home/andrey/projects/ai/ai_ftp"
#=====================================
#=== Input Path ===
input_test_folded_name = "/Upload/"
input_directory = work_directory + input_test_folded_name

#=== Output Path ===
output_result_folder_name = "/Upload/"
result_directory = work_directory + output_result_folder_name
result_file_name = "result.c"
#===================

list_of_good_test_files = ['' for _ in range(MAX_COUNT_TEST_IMGS)]
count_of_good_test_files = 0

#f_name_ok  = ['' for _ in range(MAX_COUNT_TEST_IMGS)]
#file_ok_count = 0
#-------------------------------
def Test_Imgs_Get(path, f_name_ok) :    
	#-------------------------------
	#file_ok_count = 0
	#-------------------------------
	f_name_bad = ['' for _ in range(MAX_COUNT_TEST_IMGS)]
	file_bad_count = 0
	#-------------------------------
	global work_directory
	global input_directory 
	global result_directory
	global result_file_name
	global list_of_good_test_files
	global count_of_good_test_files
	work_directory = path
	input_directory = str(work_directory) + str(input_test_folded_name)     #"/web_test_imgs/"
	result_directory = str(work_directory) + str(output_result_folder_name) #"/web_results" 
	#result_file_name = "/result.c"
	try:   
	    os.mkdir(input_directory)
	except OSError as error:
	    do_nothing = 1
	#-------------------------------
	try:   
	    os.mkdir(result_directory)
	except OSError as error:
	    # shutil.rmtree(result_directory)
	    # os.mkdir(result_directory)
	    do_nothing = 1
	#-------------------------------
	#=============================================================
	#=== Get list of test files 
	test_files = os.listdir(input_directory)
	num_test_files = len(test_files)

	#first_file_name = "First_file_name - " + test_files[0]
	file_count = 0
	
	#=============================================================
	# Try to find test image File in folder "./web_test_imgs" 
	#=== Check if it right test_files 
	file_ok_count = 0
	for file_count in range(num_test_files):
		file_is_img = 0
		try: 			
			test_img = np.asarray(Image.open(input_directory + test_files[file_count]).convert('L'))
			file_shape = test_img.shape
			file_dim = test_img.ndim
			file_is_img = 1
		except:
			do_nothing = 1

		if ((file_is_img == 1) and (file_shape[0] == file_w) and (file_shape[1] == file_h) and (file_dim == 2)) :  # may be wrong w and h place 
			f_name_ok[file_ok_count] = test_files[file_count]
			file_ok_count = file_ok_count + 1
		else :
			f_name_bad[file_bad_count] = test_files[file_count];
			file_bad_count = file_bad_count + 1
	#=============================================================
	#=== Check Ok file list 
	res_flie = open(result_directory + result_file_name, mode="w")
	res_flie.write("Max number of files = " + str(MAX_COUNT_TEST_IMGS)  +'\n')
	info_Count_files = "Total number of files - " + str(num_test_files)
	res_flie.write(info_Count_files  +'\n')    
	res_flie.write("Ok number of files = " + str(file_ok_count)   +'\n')
	for file_count in range(file_ok_count):
		list_of_good_test_files[file_count] = f_name_ok[file_count]

	#=============================================================
	res_flie.write("Bad number of files = " + str(file_bad_count)   +'\n')
	res_flie.close()
	#=============================================================
	count_of_good_test_files = file_ok_count
	return count_of_good_test_files
#=============================================================
#=============================================================

#def write_table(pred, file_names, output_file):
def write_table(pred):	
	global list_of_good_test_files
	global result_file_name
	global result_directory
	file_names = list_of_good_test_files
	output_file = result_directory + result_file_name
	# Ширина первого столбца
	w_first_row = max([len(name) for name in file_names]) + 2

	# Открываем файл 'result.txt' в режиме записи
	with open(output_file, 'a') as file:
		# Записываем горизонтальные линии таблицы, учитывая w_first_row
		file.write('+' + '-'*w_first_row + '+' + '+-------' * 10 + '+\n')

		# Записываем заголовок таблицы с номерами ячеек, учитывая w_first_row
		file.write('| ' + 'File'.ljust(w_first_row - 2) + ' |')
		for i in range(10):
			file.write('|  ' + str(i).center(4) + ' ')
		file.write('|\n')

		# Записываем горизонтальные линии таблицы
		file.write('+' + '-'*w_first_row + '+' + '+-------' * 10 + '+\n')

		# Записываем данные из массива pred[] в таблицу, учитывая w_first_row
		for i, row in enumerate(pred):
			max_value = max(row)
			file.write('| ' + file_names[i].ljust(w_first_row - 2) + ' |')
			for value in row:
				if value == max_value:
					file.write('|' + '"{:.3f}"'.format(value).rjust(4) + '')
				else:
					file.write('| ' + '{:.3f}'.format(value).rjust(4) + ' ')
			file.write('|\n')

			# Записываем горизонтальные линии таблицы после каждой строки данных
			file.write('+' + '-'*w_first_row + '+' + '+-------' * 10 + '+\n')

#=============================================================
#=============================================================
	
def Get_Input_Folder_Path() :  
	global input_directory
	return input_directory

def Get_Output_Folder_Path() :  
	global output_result_folder_name
	return output_result_folder_name	

#=============================================================
#=============================================================



def delete_all_files_in_folder():
	"""
	Удаляет все файлы из указанной папки, кроме указанного файла.

	:param folder_path: Путь к папке, из которой нужно удалить все файлы.
	:param exclude_filename: Имя файла, который не нужно удалять.
	"""
	exclude_filename = 'readme.txt'
	global input_directory
	folder_path = input_directory
	print('input_directory', input_directory)
	try:
		# Получаем список всех файлов в папке
		files = glob.glob(os.path.join(folder_path, '*'))

		# Удаляем каждый файл, кроме указанного
		for file in files:
			if os.path.isfile(file) and os.path.basename(file) != exclude_filename:
				os.remove(file)
				print(f'Файл {file} успешно удален.')
			elif os.path.basename(file) == exclude_filename:
				print(f'Файл {file} не будет удален.')

		print('Все файлы, кроме указанного, успешно удалены.')
	except Exception as e:
		print(f'Произошла ошибка при удалении файлов: {e}')

