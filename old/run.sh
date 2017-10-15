ps aux | grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn} python | grep --color=auto --exclude-dir={.bzr,CVS,.git,.hg,.svn} -v "grep python" | awk '{print $2}' | xargs kill -9
rm -rf /tmp/scrape.out
nohup python3.6 -u scrape.py > /tmp/scrape.out &
sleep 2
tail -f /tmp/scrape.out