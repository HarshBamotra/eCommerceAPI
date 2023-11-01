# eCommerceAPI

### Introduction
Introducing "eCommerceAPI"

eCommerceAPI is a CRUD API designed to perform operations like user registration, user login, product management etc. for an ECommerce shopping website.


### Project Support Features
* Users can signup and login to their accounts.
* Authenticated users can access, update and delete thier information.
* Sellers can add, update and remove product information in the database.
* Buyers can buy a product from the list of the products and many more.

  
### Buyer Endpoints
| Endpoints | HTTP Method | Requires Auth | Purpose | Usage |
| --- | --- | --- | --- | --- |
| /buyer/register/ | POST | No | Buyer registration | Accepts basic buyer information|
| /buyer/login/ | POST | No | Buyer login and access token generation |Accepts email and password and returns JWT token |
| /buyer/logout/?token= | GET | Yes | Buyer logout and revokes access token |Accepts JWT token as query parameter and revoks access token for the session |
| /buyer/me/?token= | GET | Yes | Get buyer information |Accepts JWT token as query parameter and returns user information except sensitive ones |
| /buyer/me/?token= | PUT | Yes | Update buyer information |Accepts JWT token as query parameter and update user information except sensitive ones |
| /buyer/me/?token= | DELETE | Yes | Delete buyer information |Accepts JWT token as query parameter and delete user |
| /buyer/buy/?token= | POST | Yes | Let buyers buy a product |Accepts JWT token as query parameter and updates the transactions table |

### Seller Endpoints
| Endpoints | HTTP Method | Requires Auth | Purpose | Usage |
| --- | --- | --- | --- | --- |
| /seller/register/ | POST | No | Seller registration | Accepts basic buyer information|
| /seller/login/ | POST | No | Seller login and access token generation |Accepts email and password and returns JWT token |
| /seller/logout/?token= | GET | Yes | Seller logout and revokes access token |Accepts JWT token as query parameter and revoks access token for the session |
| /seller/me/?token= | GET | Yes | Get Seller information |Accepts JWT token as query parameter and returns user information except sensitive ones |
| /seller/me/?token= | PUT | Yes | Update Seller information |Accepts JWT token as query parameter and update user information except sensitive ones |
| /seller/me/?token= | DELETE | Yes | Delete Seller information |Accepts JWT token as query parameter and delete user |
| /seller/product/?token= | GET | Yes | Get all product data |Accepts JWT token as query parameter and returns all the products added by seller |
| /seller/product/?token= | POST | Yes | Add a new product |Accepts JWT token as query parameter and adds a new product |
| /seller/product/manage/?token= | PUT | Yes | Update an existing product |Accepts JWT token as query parameter and updates information of an extisting product |
| /seller/product/manage/?token= | POST | Yes | Deletes a product |Accepts JWT token as query parameter and deletes a product |

### Product Endpoints
| Endpoints | HTTP Method | Requires Auth | Purpose | Usage |
| --- | --- | --- | --- | --- |
| /product/ | POST | No | Get all product | Get all product information present on the website|
| /product/?id= | POST | No | Get product by id | Search a particular product by id |


### Technologies Used
* [Django](https://www.djangoproject.com/) 
* [Django-Rest Framework](https://www.django-rest-framework.org) 
* [MySql](https://www.mysql.com) 
* [JWT](https://jwt.io/) 
