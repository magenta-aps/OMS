LOGIN_URL=http://localhost:8000/earkweb/admin/login/
YOUR_USER='eark'
YOUR_PASS='eark'
COOKIES=cookies/cookies.txt
CURL_BIN="curl -i -s -c $COOKIES -b $COOKIES -e $LOGIN_URL"
#CURL_BIN="curl -i -s -c $COOKIES -e $LOGIN_URL" # When the -b flag is removed, the Cookie-header will not be set

echo "Django Auth: get csrftoken ..."
$CURL_BIN $LOGIN_URL > /dev/null
# After this line a cookie file has been created and contains the csrftoken

DJANGO_TOKEN="csrfmiddlewaretoken=$(grep csrftoken $COOKIES | sed 's/^.*csrftoken\s*//')"
echo DJANGO_TOKEN: $DJANGO_TOKEN


echo " perform login ..."
$CURL_BIN \
    -d "$DJANGO_TOKEN&username=$YOUR_USER&password=$YOUR_PASS" \
    -X POST $LOGIN_URL


exit

echo -n " do something while logged in ..."

# Query an order status

#$CURL_BIN -b $DJANGO_TOKEN http://localhost:8000/earkweb/search/order_status?process_id=xyz

# Place a new order
$CURL_BIN \
    -b $DJANGO_TOKEN \
    -d	"{\"order_title\":\"example title_1\",\"aip_identifiers\":[\"b7738768-032d-3db1-eb42-b09611e6e6c6\",\"916c659c-909d-ad94-2289-c7ee8e7482d9\"]}" \
    -X POST http://localhost:8000/earkweb/search/submit_order/

echo " logout"
rm $COOKIES
