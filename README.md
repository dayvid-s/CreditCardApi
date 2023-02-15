## ⚡ Starting project

<p align="center">
  <img style="float: right;" src="https://media.istockphoto.com/id/1203763961/photo/stacked-credit-cards.jpg?s=612x612&w=0&k=20&c=bEEGZwG120WKDClhmltyAtP0kPMzNir49P4JO3pcies=" />
</p>

The first step in building our project is to create a SQL database on your machine. for this, create a database on localhost with the name: credit-card-bd, this name needs to be exact to match the settings already made in the code...


You can create your user, but if you do that, change the settings you have in the project. the default user at the moment is: Dayvid, with the password: 083a609da@

## 🚧 Database table

After the above settings, run the following commands to create the main table in the database:

CREATE TABLE `credit-card-bd`.`creditcardss` (
  `idcreditcard` INT NOT NULL,
  `exp_date` DATE NOT NULL,
  `holder` VARCHAR(50) NOT NULL,
  `cvv` INT NULL,
  `number` VARCHAR(500) NOT NULL,
  `cvv` INT NOT NULL,
  `brand` VARCHAR(60) NULL,
  PRIMARY KEY (`idcreditcard`),
  UNIQUE INDEX `idcreditcards_UNIQUE` (`idcreditcard` ASC) VISIBLE,
  UNIQUE INDEX `number_UNIQUE` (`number` ASC) VISIBLE);
  
  
  
  
Once that's done, we'll have our database prepared, now it's with python.

Clone the project, and let's start adding dependencies.

### ⚡ Flask

#### What is?

Flask is a small web framework written in Python. It is classified as a microframework because it requires no particular tools or libraries, keeping a simple yet extensible core.

#### What is it for??

Flask will be responsible for our routes, authenticating their own. Framework is very simple to use and with several operations that help in web development

#### How to install?

Run the command :

```
$ pip install Flask

```



### 🦋 MySql Connector

#### What is?

Python needs a MySQL driver to access the MySQL database
In this api we will use the driver "MySQL Connector".
We recommend that you use PIP to install "MySQL Connector"

#### How to install?

Run the command:

```
pip install mysql-connector-python
```


### ⚡ JWT TOKEN

#### What is?

The JSON Web Token is an Internet standard for creating optionally signed and/or encrypted data whose payload contains JSON that asserts some number of claims. Tokens are signed using a private secret or public/private key

#### What is it for?

Let's use it to apply authorization to routes.

#### How to install?

Run the command:

```
$ pip install jwt

```



### ⚡ OneTimepad

#### What is?

One-time pad (OTP), or one-time-key cipher, is an encryption algorithm where the plaintext is combined with a random key or “pad” that is as long as the plaintext and is used only once. Modular addition (eg XOR) is used to combine the plaintext with the pad.

#### What is it for?

Let's use it to encrypt the number field in the database.


#### How to install?

Run the command:

```
pip install onetimepad
```


### ⚡ Python-creditcard


#### What is?

A simple credit cards validation library in Python.


#### What is it for?

We are going to use it to check if the card numbers are valid, and the brands of the cards themselves.

#### How to install?

Run the command:

```
pip install git+https://github.com/maistodos/python-creditcard.git@main
```




🦋  All steps completed. Now just test!


## ⚡ Getting started


First, accesses the login route by placing the username and password in the body of the request, which is available, put them in JSON format.

By doing this, you will receive a token, and use it to be authorized to access the other routes.



### How to add a credit card?
with your token saved and present in the authorization part, enter the route:
http://localhost:5000/api/v1/credit-cards
and test by registering this credit card:


{       <br/> 
     "exp_date": "2025-08",         <br/> 
     "holder": "Jose Alves",          <br/> 
     "number": "4539578763621486",    <br/> 
     "cvv": 181           <br/> 
}    

