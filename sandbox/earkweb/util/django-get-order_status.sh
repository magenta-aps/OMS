LOGIN_URL=http://localhost:8001/earkweb/admin/login/
YOUR_USER='eark'
YOUR_PASS='eark'
COOKIES=cookies/cookies.txt
CURL_BIN="curl -i -s -c $COOKIES -b $COOKIES -e $LOGIN_URL"

echo "Django Auth: get csrftoken ..."
$CURL_BIN $LOGIN_URL > /dev/null
# After this line a cookie file has been created and contains the csrftoken

DJANGO_TOKEN="csrfmiddlewaretoken=$(grep csrftoken $COOKIES | sed 's/^.*csrftoken\s*//')"
echo DJANGO_TOKEN: $DJANGO_TOKEN

echo " perform login ..."
$CURL_BIN \
    -d "$DJANGO_TOKEN&username=$YOUR_USER&password=$YOUR_PASS" \
    -X POST $LOGIN_URL


echo -n " do something while logged in ..."

# Query an order status

$CURL_BIN -b $DJANGO_TOKEN http://localhost:8001/earkweb/search/order_status?process_id=b62a7d5e-b403-461e-8258-5ae811fa17bc

echo " logout"
rm $COOKIES
