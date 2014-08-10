. tests/common.sh

DATE=$(date +%Y.%m.%d)
HOST="127.0.0.1"
EXPECTED_FILENAME="/var/logg/${DATE}/${HOST}.log"
MESSAGE="Hello world"

assert_zero_retcode echo -n $MESSAGE > /dev/udp/127.0.0.1/1524

echo "Sent UDP message"
#echo "Testing: $EXPECTED_FILENAME"
#assert_zero_retcode test -f "$EXPECTED_FILENAME"
#echo "Expected file exists"
#assert_zero_retcode cat "$EXPECTED_FILENAME" | grep "$MESSAGE"
#echo "File content matches"

exit 0
