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

## Earkweb Service

**POST /earkweb/submitOrder**

Used for submitting orders to earkweb. Consumes JSON containing the orderId, i.e. like this:
```
{
	"orderId": "2a48e52cf7914fc886e8a632abf0826c"
}
```
If the request was successful the server responds with JSON like this:
```
{
	"success": true,
	"message": "The order was successfully submitted"
}
```
In case of an error, the `success` will be `false` and an appropriate `message` will 
indicate what went wrong.  

** GET /earkweb/orderStatus?orderId=\<orderId\>**

Gets the status of the order at earkweb. Will return JSON like this if the request was a success:
```
{
	"success": true,
	"processStatus": "Processing"
}
```
In case of an error, the `success` will be `false` and an appropriate `message` will 
indicate what went wrong.  
