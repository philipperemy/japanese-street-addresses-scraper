rm -rf /tmp/scrape.out
rm -rf /tmp/addresses.txt
nohup python3.6 -u scrape.py > /tmp/scrape.out &
sleep 2
tail -f /tmp/scrape.out