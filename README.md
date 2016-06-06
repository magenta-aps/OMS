# OMS
Backend (RESTful service) for the EARK Order Management Tool

## Order Service

**DELETE /deleteOrder?orderId=\<orderId\>**

**GET /getOrders?uid=\<uid\>&status=\<status\>&notStatus=\<status\>&assignee=\<assignee\>**

Can be called without parameters in which case all orders are returned. Provide exactly one of the 
specified parameter for filtering search results (further filtering should be done from the Anguler front-end). 

**GET /getOrderData?orderId=\<orderId\>**

**POST /newOrder**

Send JSON similar to [this](https://github.com/magenta-aps/OMS/blob/develop/examples/order.json)

**PUT /updateOrder**

Send JSON similar to [this](https://github.com/magenta-aps/OMS/blob/develop/examples/updateOrder.json). 
Include whatever properties you wish to change.

## Person Service

**DELETE /deletePerson?uid=\<uid\>**

**GET /getPerson?uid=\<uid\>**

**POST /newPerson**
Consumes JSON like [this](https://github.com/magenta-aps/OMS/blob/develop/examples/person.json) (if the user type is an enduser). 
If the person is an archivist the type must be set to "archivist" 
