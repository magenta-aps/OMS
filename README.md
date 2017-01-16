# Order Management Servive (OMS)
The Order Management Service is the backend for the Order Management Tool (OMT) in the [EARK project](http://eark-project.com/). It is a RESTful service written in Python/Flask. As an enduser of the 
[E-Ark-Platform UI](https://github.com/magenta-aps/E-Ark-Platform-UI) it is not necessary to worry about 
the OMS, but below the API used by the frontend developers is described (all the services respond with JSON).

## Items Service

**GET /getItems?orderId=\<orderId\>**

Gets all the items belonging to the given orderId.

## Order Service

**DELETE /deleteOrder?orderId=\<orderId\>**

Delete the order with the given orderId.

**GET /getOrders?userName=\<userName\>&status=\<status\>&notStatus=\<status\>&assignee=\<assignee\>**

Can be called without parameters in which case all orders are returned. Provide exactly one of the 
specified parameter for filtering search results (further filtering should be done from the Anguler front-end). 

**GET /getOrderData?orderId=\<orderId\>**

Gets the order data for the order with the given orderId.

**POST /newOrder**

Send JSON similar to [this](https://github.com/magenta-aps/OMS/blob/develop/examples/order.json)

**PUT /updateOrder**

Send JSON similar to [this](https://github.com/magenta-aps/OMS/blob/develop/examples/updateOrder.json). 
Include whatever properties you wish to change.

## Person Service

**DELETE /deletePerson?userName=\<userName\>**

Delete the user (enduser or archivist) with the given username.

**GET /getArchivists**

Gets all the archivists.

**GET /getPerson?userName=\<userName\>**

Get the details for the person (both users and archivists) with the given username.

**POST /newPerson**

Consumes JSON like [this](https://github.com/magenta-aps/OMS/blob/develop/examples/person.json) (if the user type is an enduser). 
If the person is an archivist the type must be set to "archivist" 

## Earkweb Service

The services described in this section takes care of the communication to [earkweb](https://github.com/eark-project/earkweb). These services are used to submit orders, query the status of these etc. A few words on the 
status of an order as it goes through the search/OMT/IPviewer workflow are needed. More to follow...

**POST /earkweb/createDIP**

Used to create the DIP. This can be called when the order is in the "processing" state.

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

**GET /earkweb/orderStatus?orderId=\<orderId\>**

Gets the status of the order at earkweb. Will return JSON like this if the request was a success:
```
{
	"success": true,
	"processStatus": "processing"
}
```
In case of an error, the `success` will be `false` and an appropriate `message` will 
indicate what went wrong.  
