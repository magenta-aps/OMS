# OMS
Backend (RESTful service) for the EARK Order Management Tool

## Items Service

**GET /getItems?orderId=\<orderId\>**

Gets all the items belonging to the given orderId.

## Order Service

**DELETE /deleteOrder?orderId=\<orderId\>**

**GET /getOrders?userName=\<userName\>&status=\<status\>&notStatus=\<status\>&assignee=\<assignee\>**

Can be called without parameters in which case all orders are returned. Provide exactly one of the 
specified parameter for filtering search results (further filtering should be done from the Anguler front-end). 

**GET /getOrderData?orderId=\<orderId\>**

**POST /newOrder**

Send JSON similar to [this](https://github.com/magenta-aps/OMS/blob/develop/examples/order.json)

**PUT /updateOrder**

Send JSON similar to [this](https://github.com/magenta-aps/OMS/blob/develop/examples/updateOrder.json). 
Include whatever properties you wish to change.

## Person Service

**DELETE /deletePerson?userName=\<userName\>**

**GET /getArchivists**

Gets all the archivists.

**GET /getPerson?userName=\<userName\>**

**POST /newPerson**

Consumes JSON like [this](https://github.com/magenta-aps/OMS/blob/develop/examples/person.json) (if the user type is an enduser). 
If the person is an archivist the type must be set to "archivist" 
