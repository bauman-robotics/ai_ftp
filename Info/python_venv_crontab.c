
#* * * * * /usr/bin/python3 /home/andrey/projects/ai/ai_ftp/server.py >> /home/andrey/projects/ai/ai_ftp/logfile.log 2>&1

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

You don't need to activate, you can set which python interpreter 
to use via the shebang line at the top of your script. 
Commonly, you will see #!/usr/bin/python 
in scripts because this is where linux pre-installs python. 
However, you can just use a different path, for example, 
script.py

#!/home/ubuntu/scripts/venv/bin/python (or python3)
https://www.reddit.com/r/learnpython/comments/abxu08
/run_python_script_from_crontab_using_virtual_env/

chmod +x script.py

08 15 * * * /home/ubuntu/scripts/localscripts/script.py > /home/ubuntu/scripts/localscripts/logs/script.log  2>&1 | logger -t mycmd

 Sources:

    https://en.wikipedia.org/wiki/Shebang_(Unix)

    https://bash.cyberciti.biz/guide/Shebang

#===================================================================

#=== resuirement ===============
pip freeze > requirements.txt
pip3 install -r requirements.txt

