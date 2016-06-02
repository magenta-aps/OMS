# OMS
Backend (RESTful service) for the EARK Order Management Tool

## Order Service

**DELETE /deleteOrder?orderId=\<orderId\>**

**GET /getOrder?uid=\<uid\>&status=\<status\>&notStatus=\<status\>&assignee=\<assignee\>**

Can be call without parameters in which case all orders are returned. Provide exactly one of the 
specified parameter for filter search results (further filtering should be done from the Anguler front-end). 

**GET /getOrderStatus?orderId=\<orderId\>**

**POST /newOrder**

Send JSON similar to [this](https://github.com/magenta-aps/OMS/blob/develop/examples/order.json)

**PUT /updateOrder**

Send JSON similar to [this](https://github.com/magenta-aps/OMS/blob/develop/examples/updateOrder.json). 
Include whatever properties you wish to change.

 