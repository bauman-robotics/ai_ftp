
#=== Crontab -e =====================================================
# m h  dom mon dow 
*/1 * * * *  - the same every one minutes 

SHELL=/bin/bash
* * * * * source /home/arkhan/Andrey/venv/bin/activate && /home/arkhan/Andrey/venv/bin/python3 /home/arkhan/Andrey/ai_ftp/server.py >> /home/arkhan/Andrey/ai_ftp/cronout.log 2>&1

https://techstuff.leighonline.net/2023/06/11/python-virtual-environment-from-crontab/

#=== venv ===
/home/arkhan/Andrey/venv/

#=== Server ===
/home/arkhan/Andrey/ai_ftp/server.py

#=== Python ? ===
venv/bin/python3

#=== Log ===
server.py >> /home/arkhan/Andrey/ai_ftp/cronout.log 2>&1


#=== Not Tested =====
https://www.reddit.com/r/learnpython/comments/abxu08/run_python_script_from_crontab_using_virtual_env/

#=== resuirement ===============
pip freeze > requirements.txt
pip3 install -r requirements.txt

