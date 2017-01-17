# Order Management Service (OMS)
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
status of an order as it goes through the search/OMT/IPviewer workflow are needed. Basically, the earkweb service of the OMS makes it possible to run the AIP to DIP conversion tasks from the OMT. It works as follows:

1. When a user has placed an order from "search", it will be visible in to the archivist in the OMT with order status "new".

2. When the archivist clicks on the order in the OMT (the "update order status" icon in the top right corner may need to be clicked first) he or she can click the "Process order" button. The order status will then change to "submitted" and the earkweb tasks AIPtoDIPReset, DIPAcquireAIPs and DIPExtractAIPs are initiated.

3. Content now have to be moved to the DIP.

4. When the "update order status" icon is clicked, the order status will change to "processing" (meaning that the archivist can now manipulate the files in the working area). It is now possible to view the package in the IPviewer.

5. When the archivist is satisfied with the DIP, the "Package DIP" button can be clicked. The earkweb tasks DIPMetadataCreation, DIPIdentifierAssignment, DIPPackaging and DIPStore tasks are run. The order status will now change to "packaging".

6. When the DIP is finished (click the "update order status" icon again) its status will change to "ready" and a "Browse"-button will appear on the order details page. When this is clicked, the order can be browsed in the IPviewer.

Internally, the OMS works with the following order statuses: (error) - new - submitted - processing - packaging - packaged - untarring - indexing - ready.

**POST /earkweb/createDIP**

Used to create the DIP. This can be called when the order is in the "processing" state. Should be used when the archivist is done manipulating the "DIP0" in the working area.

**POST /earkweb/submitOrder**

Used for submitting orders to earkweb by the archivist. Can only be called when to order has status "new". 
Consumes JSON containing the orderId, i.e. like this:
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

**GET /earkweb/updateAllOrderStatus**

Used to update the order statuses for all the orders in the OMT. As the orders are processed within earkweb the statuses of these change and the statuses within the OMT should be updated correspondingly. JSON containing info about any change in order statuses will be returned.
