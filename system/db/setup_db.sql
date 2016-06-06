/* Setup MySQL DB to be used by the OMS
 * 
 * Author: Andreas Kring <andreas@magenta.dk>
 * */

DROP DATABASE IF EXISTS temp;
CREATE DATABASE temp default character set utf8 default collate utf8_general_ci;
USE temp;

/* Entity sets - see E/R diagram */

DROP TABLE IF EXISTS Person;
CREATE TABLE Person(
	uid VARCHAR(32) PRIMARY KEY,
	firstname VARCHAR(50),
	lastname VARCHAR(50),
	email VARCHAR(255)
);

DROP TABLE IF EXISTS EndUser;
CREATE TABLE EndUser(
	uid VARCHAR(32) PRIMARY KEY,
	FOREIGN KEY (uid) REFERENCES Person(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

DROP TABLE IF EXISTS Archivist;
CREATE TABLE Archivist(
	uid VARCHAR(32) PRIMARY KEY,
	FOREIGN KEY (uid) REFERENCES Person(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

-- All the access stuff should maybe be move to another entity set
DROP TABLE IF EXISTS Orders;
CREATE TABLE Orders(
	orderId VARCHAR(32) PRIMARY KEY,
	title VARCHAR(255),
	origin VARCHAR(12),
	orderDate DATETIME,
	validationDate DATETIME,
	plannedDate DATETIME,
	accessDate DATETIME,
	accessDateComments TEXT,
	-- accessRestrictionCode INT,
	-- accessRestriction
	orderStatus VARCHAR(10),
	accessEndDate DATETIME,
	deliveryFormat VARCHAR(30)
);

DROP TABLE IF EXISTS OrderItems;
CREATE TABLE OrderItems(
	refCode VARCHAR(32) PRIMARY KEY,
	title VARCHAR(255),
	aipURI VARCHAR(32),
	aipTitle VARCHAR(32),
	levelOfDescription TEXT
);


/* Relationships - see E/R diagram */

DROP TABLE IF EXISTS OrderedBy;
CREATE TABLE OrderedBy(
	uid VARCHAR(32),
	orderId VARCHAR(32),
	endUserOrderNote TEXT,
	PRIMARY KEY (uid, orderId),
	FOREIGN KEY (uid) REFERENCES Person(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (orderId) REFERENCES Orders(orderId)
		ON DELETE CASCADE
		ON UPDATE CASCADE
);

DROP TABLE IF EXISTS Responsible;
CREATE TABLE Responsible(
	uid VARCHAR(32),
	orderId VARCHAR(32),
	publicNote TEXT,
	privateNote TEXT,
	PRIMARY KEY (uid, orderId),
	FOREIGN KEY (uid) REFERENCES Person(uid)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	FOREIGN KEY (orderId) REFERENCES Orders(orderId)
		ON DELETE CASCADE
		ON UPDATE CASCADE	
);

DROP TABLE IF EXISTS BelongsTo;
CREATE TABLE BelongsTo(
	orderId VARCHAR(32),
	refCode VARCHAR(32),
	PRIMARY KEY (orderId, refCode),
	FOREIGN KEY (orderId) REFERENCES Orders(orderId)
		ON DELETE CASCADE
		ON UPDATE CASCADE,	
	FOREIGN KEY (refCode) REFERENCES OrderItems(refCode)
		ON DELETE CASCADE
		ON UPDATE CASCADE	
);

/* For testing */
INSERT INTO Person VALUES ('uid1', 'Clint', 'Eastwood', 'clint@hollywood.com');
INSERT INTO Person VALUES ('uid2', 'Bill', 'Clinton', 'bill@whitehouse.gov');
INSERT INTO Person VALUES ('uid3', 'Bruce', 'Lee', 'bruce@kungfu.org');
INSERT INTO Person VALUES ('uid4', 'Alex', 'T', 'alt@sa.dk');
INSERT INTO Person VALUES ('uid5', 'Anders Bo', 'Nielsen', 'abn@sa.dk');

INSERT INTO EndUser VALUES ('uid1');
INSERT INTO EndUser VALUES ('uid2');
INSERT INTO EndUser VALUES ('uid3');

INSERT INTO Archivist VALUES ('uid4');
INSERT INTO Archivist VALUES ('uid5');
/*
INSERT INTO Orders VALUES ('orderUUID1', 'Hydrogen', NULL, '2016-05-18 12:00:00', '2016-05-19 13:00:00', '2016-07-18 15:00:00', NULL, NULL, NULL, NULL, NULL);
INSERT INTO Orders VALUES ('orderUUID2', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO Orders VALUES ('orderUUID3', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO OrderedBy VALUES ('uid1', 'orderUUID1', 'This is a note...');
INSERT INTO OrderedBy VALUES ('uid1', 'orderUUID2', 'This is a note...');
INSERT INTO OrderedBy VALUES ('uid2', 'orderUUID3', 'This is a note...');
*/

source insert_data.sql;