. tests/common.sh

assert_zero_retcode python tests/mock_server.py -T 10 -u -a 127.0.0.1 -p 1514 &
assert_zero_retcode python tests/mock_server.py -T 10 -t -a 127.0.0.1 -p 1512 &

exit 0
