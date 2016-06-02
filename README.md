# OMS
Backend (RESTful service) for the EARK Order Management Tool

## Order Service

**DELETE /deleteOrder?orderId=\<orderId\>**

**GET /getOrdersForUser?uid=\<uid\>**
Get the orderId's for a given user uid.

**GET /getOrderStatus?orderId=\<orderId\>**

**POST /newOrder**

Send JSON similar to [this](https://github.com/magenta-aps/OMS/blob/develop/examples/order.json)

**PUT /updateOrder**

Send JSON similar to [this](https://github.com/magenta-aps/OMS/blob/develop/examples/updateOrder.json). 
Include whatever properties you wish to change.

 