######################################################
######################################################
### Make folders for Test Images for work in server
import shutil
import os
import numpy as np
from PIL import Image


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
	info_Count_files = "Count_files - " + str(num_test_files)
	first_file_name = "First_file_name - " + test_files[0]
	file_count = 0
	
	res_flie = open(result_directory + result_file_name, mode="w")
	res_flie.write(info_Count_files  +'\n')    
	res_flie.write(first_file_name   +'\n') 
	#res_flie.close()
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
	#res_flie = open(result_directory + result_file_name, mode="a")	    
	res_flie.write("Warning: MAX_COUNT_TEST_IMGS = " + str(MAX_COUNT_TEST_IMGS)  +'\n')
	ok_list = "#=== Ok file list =========="
	ok_num = str(len(f_name_ok))
	res_flie.write(ok_list   +'\n')
	res_flie.write("count = " + str(file_ok_count)   +'\n')
	for file_count in range(file_ok_count):
		ok_name = str(file_count) + "   " + f_name_ok[file_count]
		res_flie.write(ok_name   +'\n')
		#===
		list_of_good_test_files[file_count] = f_name_ok[file_count]
		#===		
	res_flie.write("#============================"   +'\n')
	#=============================================================
	#=== Check OBad file list 
	#res_flie = open(result_directory + result_file_name, mode="w")
	bad_list = "#=== Bad file list =========="
	bad_num = str(len(f_name_bad))
	res_flie.write(bad_list   +'\n')
	res_flie.write("count = " + str(file_bad_count)   +'\n')
	for file_count in range(file_bad_count):
		bad_name = str(file_count) + "   " + f_name_bad[file_count]
		res_flie.write(bad_name   +'\n')
	res_flie.write("#============================"   +'\n') 
	res_flie.close()
	#=============================================================
	count_of_good_test_files = file_ok_count
	return count_of_good_test_files
#=============================================================
#=============================================================

def Save_Result(predictions) :  
	global list_of_good_test_files
	global count_of_good_test_files
	global result_file_name
	global result_directory	
	res_flie = open(result_directory + result_file_name, mode="a")
	res_flie.write('#######################'   +'\n')
	for p_num in range (count_of_good_test_files):
		res_flie.write('#######################'   +'\n')
		res_flie.write('File_Name = ' + str(list_of_good_test_files[p_num])  +'\n')
		for i in range (10):
			line = 'is ' + str(i) + '---' + "%.3f" %(predictions[p_num][i])  +'\n'
			res_flie.write(line)
#=============================================================================================
#=============================================================================================

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
	with open(output_file, 'w') as file:
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
