if not defined in_subprocess (cmd /k set in_subprocess=y ^& %0 %*) & exit )
python server.py