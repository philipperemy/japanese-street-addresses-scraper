ps aux | grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn} python | grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn} -v "grep python" | awk '{print $2}' | xargs kill -9
rm -rf /tmp/brute.out
nohup python3.6 -u brute_force_all_endpoints_mt.py > /tmp/brute.out &
sleep 2
tail -f /tmp/brute.out