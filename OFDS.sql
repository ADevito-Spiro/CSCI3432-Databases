/* Online Food Delivery Service  */
create database OFDS;
use OFDS;

/* Customer Table */
CREATE TABLE Customer(
    CustomerID INT not null, /* ensures unique idenfier if NOS */
    CustomerName varchar(50),
    CustomerEmail varchaR(50), 
    CustomerAddress varchar(50),
    CustomerPaymentInfo varchar(100),
    PRIMARY KEY (CustomerID),
    check (length((CustomerID))=4)
);

/* Restarant */
CREATE TABLE Restaurant(
    RestaurantID INT not null,
    RestaurantName varchar(50),
    RestaurantDesc varchar(800),
    RestaurantStarRating enum('0','1', '2', '3', '4', '5','6') NOT NULL, -- [0,5] inclusive 
    RestaurantLocation varchar(50),
    PRIMARY KEY (RestaurantID),
    check (length((RestaurantID))=4)
);

/* Menu */
CREATE TABLE Menu(
    MenuID INT not null, -- can start w 3 for example 
    RestaurantID INT not null,
    MenuItem varchar(50),
    MenuItemDesc varchar(500),
    PRIMARY KEY (MenuID),
    FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID), /* Many-to-Many */
	check(length((RestaurantID))=4)
);



/* Orders naming conv. is plural not to confuse with keyword. Also every naming conv. that references orders is plural */
CREATE TABLE Orders(
    OrdersID INT not null,
    CustomerID INT not null,
    RestaurantID INT not null,
    OrdersDate DATE,
    TotalPrice decimal(10, 2), -- add mechanic in application logic 
    OrdersStatus enum("RECIEVED","PENDING","DELIVERED","IN-TRANSIT","CANCELED") NOT NULL,
    CustomerComment varchar(1000),
    primary key (OrdersID),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID), /* One-to-One for brevity's sake */
    FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID), /* One-to-Many */
    check (length((OrdersID))=4),
    check (length((CustomerID))=4),
    check (length((RestaurantID))=4)
);

alter table Menu 
add column MenuItemPrice decimal(10,2);


/* Driver */
CREATE TABLE Driver(
    DriverID INT not null, -- can start with 4 for example 
    CurrentDriverLocation varchar(60), /* you can change later if you want it to be corrdinates/regex */
    DriverName varchar(100),
    DriverDesc varchar(300),
    OrderIsReceived bool,
    DriverStarRating enum('0','1', '2', '3', '4', '5') NOT NULL, /*possible values*/
    OrdersID INT not null,
    PRIMARY KEY (DriverID),
    FOREIGN KEY (OrdersID) REFERENCES Orders(OrdersID), /* One-to-One also for brevity */ 
    check(length((DriverID))=4),
    check(length((OrdersID))=4)
);

-- Create LocationDelivery table
CREATE TABLE LocationDelivery(
    OrdersID INT auto_increment not null PRIMARY KEY,
    DeliveryAddress VARCHAR(300),
    PickupAddress VARCHAR(300),
    FOREIGN KEY (OrdersID) REFERENCES Orders(OrdersID)
);

CREATE TABLE Price(
    OrdersID INT not null,
    TotalCart DECIMAL(10, 2),
    FOREIGN KEY (OrdersID) REFERENCES Orders(OrdersID),
    PRIMARY KEY (OrdersID),
	check (length((OrdersID))=4)
);

/* Private/protected access modifyer in application logic, last four digits whatever you like to store it as */
CREATE TABLE PaymentInformation(
    CustomerID INT auto_increment PRIMARY KEY,
    CardNum int not null 
    check(length(CardNum)=19), /* XXXX XXXX XXXX XXXX (Not including outer delimiter whitespace, just the 3 inner spaces) */ 
    CardName varchar(30),
    CardExpireDate varchar(5), /* MM/YY */
    CardCCN INT 
    check(length(CardCCN)=3),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);

-- CREATE TABLE Status(
--     OrdersID INT PRIMARY KEY,
--     Status enum("",""),
--     FOREIGN KEY (OrdersID) REFERENCES Orders(OrdersID)
-- );


CREATE TABLE DateOrder(
    OrdersID INT NOT NULL,
    TimeOfOrder DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY Key (OrdersID),
    FOREIGN KEY (OrdersID) REFERENCES Orders(OrdersID),
    CHECK (length(OrdersID)=4)
);


 
CREATE TABLE Quantity(
    OrdersID INT not null 
    check(length(OrdersID)=4) PRIMARY KEY,
    Item VARCHAR(200),
    Quantity INT,
    FOREIGN KEY (OrdersID) REFERENCES Orders(OrdersID)
);

-- TEST CASES (Dont feel obligated to keep the names lol) 
-- Customer Table
INSERT INTO Customer(CustomerID, CustomerName, CustomerEmail, CustomerAddress, CustomerPaymentInfo)
VALUES(1001,"Austin S.", "austin123@gmail.com", "123 Main St", "CashApp");

INSERT INTO Customer(CustomerID, CustomerName, CustomerEmail, CustomerAddress, CustomerPaymentInfo)
VALUES(1002,"Dartagnan S.", "sams456@hotmail.com", "456 South Blvd", "Credit Card");

INSERT INTO Customer(CustomerID, CustomerName, CustomerEmail, CustomerAddress, CustomerPaymentInfo)
VALUES(1003,"Vale S.", "vale789@gmail.com", "789 West Pt", "Cash");

INSERT INTO Customer(CustomerID, CustomerName, CustomerEmail, CustomerAddress, CustomerPaymentInfo)
VALUES(1004,"Lilli G.", "lilli012@yahoo.com", "012 North Ave", "Debit Card");

desc Customer;
Select * from Customer;

-- Restarant Table
insert into Restaurant(RestaurantID, RestaurantName, RestaurantDesc, RestaurantStarRating, RestaurantLocation)
values(2000,"The Binary Burrito","An award-winning, casual dining spot serving Mexican food with an American Southern influence",4,"859 Brefield Way");

insert into Restaurant(RestaurantID, RestaurantName, RestaurantDesc, RestaurantStarRating, RestaurantLocation)
values(2001,"Cartesian Grill","A fast-casual burger joint offering over 10k order combinations",5,"114 Cheshire Pt");

insert into Restaurant(RestaurantID, RestaurantName, RestaurantDesc, RestaurantStarRating, RestaurantLocation)
values(2002,"The Java Hut","A cafe that sources artisan-selected beans to brew specialty coffee and espresso-based drinks",5,"114 Tortuga Blvd");

select * from Restaurant;

-- Menu, RestID <-> RetstID
insert into Menu(MenuID, RestaurantID, MenuItem, MenuItemDesc,MenuItemPrice)
values(3000,2000,"Burrito Bowl","Burrito bowl with your choice of chicken, barbacoa, or steak",13.99);
insert into Menu(MenuID, RestaurantID, MenuItem, MenuItemDesc,MenuItemPrice)
values(3001,2001,"Double-Quarter Pounder with Cheese","Two 1/4 pound angus beef patties, lettace, tomato, and American cheese. Comes with fries",14.99);
insert into Menu(MenuID, RestaurantID, MenuItem, MenuItemDesc,MenuItemPrice)
values(3002,2002,"Brown Sugar Shaken Expresso","Two pumps of our signature brown sugar syrup, blonde roast expresso, a splash of oatmilk, topped with sweet cream cinimon vanilla cold foam",8.99);

select * from Menu;

alter table Orders
modify OrdersDate DATETIME default current_timestamp;

-- Orders (Most Foirien Key Connections)
insert into Orders(OrdersID, CustomerID, RestaurantID, OrdersDate, TotalPrice, OrdersStatus, CustomerComment)
values(4000,1001,2000,current_timestamp(),13.99,"PENDING","Extra chicken, please");

insert into Orders(OrdersID, CustomerID, RestaurantID, OrdersDate, TotalPrice, OrdersStatus, CustomerComment)
values(4001,1002,2001,current_timestamp(),14.99,"DELIVERED","No pickels or mustard, please. Fries extra crispy");

insert into Orders(OrdersID, CustomerID, RestaurantID, OrdersDate, TotalPrice, OrdersStatus, CustomerComment)
values(4002,1003,2002,current_timestamp(),8.99,"IN-TRANSIT","Light ice, no cold foam, please");

insert into Orders(OrdersID, CustomerID, RestaurantID, OrdersDate, TotalPrice, OrdersStatus, CustomerComment)
values(4003,1004,2000,current_timestamp(),13.99,"CANCELED","You guys always forget to add enough cheese");

select * from Orders;

alter table Driver
add column ServiceFee decimal(10,2);

-- Driver (Should Allow Multiple instances of DriverID)     
insert into Driver(DriverID, CurrentDriverLocation, DriverName, DriverDesc, OrderIsReceived, DriverStarRating, OrdersID,ServiceFee)
values(7000, "(34.0522° N, 118.2437° W)", "Kyle R.","I deliver within a 15 mile radius by car",TRUE,4,4003,8.99);

insert into Driver(DriverID, CurrentDriverLocation, DriverName, DriverDesc, OrderIsReceived, DriverStarRating, OrdersID,ServiceFee)
values(7001, "(39.0542° S, 256.2177° E)", "Yanin E.","I deliver on the southside within a 5 mile radius by motorbike",TRUE,4,4002,10.00);

insert into Driver(DriverID, CurrentDriverLocation, DriverName, DriverDesc, OrderIsReceived, DriverStarRating, OrdersID,ServiceFee)
values(7002, "(40.0542° S, 256.5952° E)", "Yanin E.","I deliver on the southside within a 5 mile radius by motorbike",FALSE,4,4001,10.00);

insert into Driver(DriverID, CurrentDriverLocation, DriverName, DriverDesc, OrderIsReceived, DriverStarRating, OrdersID,ServiceFee)
values(7003, "(65.4762° N, 159.2470° W)", "Ian R.","I deliver within a 7 mile radius by e-bike",TRUE,5,4000,6.99);

select * from Driver;

-- Price
insert into Price(OrdersID, TotalCart)
values(4000,20.00);

insert into Price(OrdersID, TotalCart)
values(4001,65.99);

insert into Price(OrdersID, TotalCart)
values(4002,8.99);

insert into Price(OrdersID, TotalCart)
values(4003,13.99);

select * from Price;


alter table PaymentInformation 
modify CardNum varchar(19);

-- PaymentInformation
insert into PaymentInformation(CustomerID,CardNum,CardName,CardExpireDate,CardCCN)
values(1001,"1234 5678 9101 1123","Austin S.","05/28",123);

insert into PaymentInformation(CustomerID,CardNum,CardName,CardExpireDate,CardCCN)
values(1002,"9999 8888 7777 3333","Dartagnan S.","11/30",142);

insert into PaymentInformation(CustomerID,CardNum,CardName,CardExpireDate,CardCCN)
values(1003,"1561 4489 6516 6511","Vale S.","06/27",415);

insert into PaymentInformation(CustomerID,CardNum,CardName,CardExpireDate,CardCCN)
values(1004,"2656 1656 4982 1615","Lilli G.","07/26",845);

SELECT * FROM Customer where CustomerID = 4000;
select * from PaymentInformation;

-- DateOrder

insert into DateOrder(OrdersID,TimeofOrder)
values(4000,current_timestamp()); 

insert into DateOrder(OrdersID,TimeofOrder)
values(4001,current_timestamp()); 

insert into DateOrder(OrdersID,TimeofOrder)
values(4002,current_timestamp()); 

insert into DateOrder(OrdersID,TimeofOrder)
values(4003,current_timestamp()); 

select * from DateOrder;
-- Quantity 

insert into Quantity(OrdersID,Item,Quantity)
values(4000,"Burrito Bowl",1);

insert into Quantity(OrdersID,Item,Quantity)
values(4001,"Burger Combo",2);

insert into Quantity(OrdersID,Item,Quantity)
values(4002,"Coffee",1);

insert into Quantity(OrdersID,Item,Quantity)
values(4003,"Burrito Bowl",1);
select * from Quantity;