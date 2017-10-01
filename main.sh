while true; do
    echo Starting the program
    nohup python3.6 -u main.py &
    echo Going to sleep for one hour now
    sleep 3600
    echo I am awake now lets go
    ps aux | grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn} python | grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn} -v "grep python" | awk '{print $2}' | xargs kill -9
    echo Program should be dead by now
done