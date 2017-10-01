while true; do
    nohup python3.6 -u main.py &
    sleep 3600
    ps aux | grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn} python | grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn} -v "grep python" | awk '{print $2}' | xargs kill -9
done