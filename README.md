# Shop API Documentation


## Authentication
**HTTP:** *Bearer*\
**HTTP Authorization Scheme:** *bearer*\
**Bearer format:** *JWT*

====================
=

## Admin
***Authentication** is needed to perform Admin actions.*


### Users List
**method:** `GET`\
**URL:** `/api/v1/users`

#### Responses
|Status|Meaning|Description| Schema        |
|---|---|---|---------------|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|List of User objects| List of users |
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|User Error| Error message |
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|General Error| Error message |


#### Response Schema
###### 200  
```json
{
  "users": [
    {
      "id": 1,
      "email": "shoppa@shoppa.pro",
      "password": "AAaa1234!@",
      "blocked": false,
      "create_at": "10/10/2022",
      "last_login": "13/10/2022"
    }
  ]
}
```
###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
-------------------------------------
### Blocked Users List
**method:** `GET`\
**URL:** `/api/v1/users/blocked`

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|List of User objects| List of users |
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|User Error| Error message |
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|General Error| Error message |

#### Response Schema
###### 200  
```json
{
  "users": [
    {
      "id": 1,
      "email": "shoppa@shoppa.pro",
      "password": "AAaa1234!@",
      "blocked": false,
      "create_at": "10/10/2022",
      "last_login": "13/10/2022"
    }
  ]
}
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
----------------


### Allowed Users List
**method:** `GET`\
**URL:** `/api/v1/users/allowed`

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|List of User objects| List of users |
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|User Error| Error message |
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|General Error| Error message |

#### Response Schema
###### 200  
```json
{
  "users": [
    {
      "id": 1,
      "email": "shoppa@shoppa.pro",
      "password": "AAaa1234!@",
      "blocked": false,
      "create_at": "10/10/2022",
      "last_login": "13/10/2022"
    }
  ]
}
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
----------------

### Block User
**method:** `POST`\
**URL:** `/api/v1/block`

#### Responses
|Status|Meaning|Description| Schema        |
|---|---|---|---------------|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|User Blocked| Error message |
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error| Error message |
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Admin Error| Error message |

#### Request Schema
```json
{
"user_id": 1
}
```

#### Response Schema
###### 200  
```json
{
"message": "User Blocked/Unblocked Successfully"
}
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```

____

### Unblock User
**method:** `DELETE`\
**URL:** `/api/v1/block`

#### Responses
|Status|Meaning|Description| Schema        |
|---|---|---|---------------|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|User Blocked| Error message |
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error| Error message |
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Admin Error| Error message |

#### Request Schema
```json
{
"user_id": 1
}
```

#### Response Schema
###### 200  
```json
{
"message": "User Blocked/Unblocked Successfully"
}
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
____

### Send Advertising to Subscribers
**method:** `POST`\
**URL:** `/api/v1/promo`

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|No registered subscribers|None|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|Advertising sent to Subscribers|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Admin Error|None|

#### Response Schema
###### 200  
```json
{
"message": "no registered subscribers"
}
```
##### 201
```json
{
"subscribers_amount": 152,
"item": "JetSky SEAWOO blue"
}
```
###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
____


### Payments List
**method:** `GET`\
**URL:** `/api/v1/all-payments`

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|List of Payments objects|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Admin Error|None|

#### Response Schema
###### 200  
```json
{
  "payments": [
    {
      "id": 1,
      "amount": 115,
      "total_quantity": 8,
      "payment_at": 11654.200012,
      "state": "pending",
      "transaction_id": "laskdmoashdmoasndasd#@$#@sda___Asdasd",
      "refund_at": 11654.200012,
      "user_id": 1,
      "items": [
        {
          "id": 1,
          "title": "JetSky SEAWOO blue",
          "manufacturer": "SEAWOO",
          "on_sale": false,
          "on_stock": true,
          "sold": false,
          "engine_hs_power": 300,
          "original_price": 300,
          "discount": 12,
          "file_path": "C:\\temp\\photo.png",
          "new_price": 258,
          "user_id": 258,
          "created_at": "10/10/2022",
          "last_modified": "10/10/2022"
        }
      ]
    }
  ]
}
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
____

### Paid Payments List
**method:** `GET`\
**URL:** `/api/v1/paid-payments`

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|List of Payments objects|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Admin Error|None|

#### Response Schema
###### 200  
```json
{
  "payments": [
    {
      "id": 1,
      "amount": 115,
      "total_quantity": 8,
      "payment_at": 11654.200012,
      "state": "pending",
      "transaction_id": "laskdmoashdmoasndasd#@$#@sda___Asdasd",
      "refund_at": 11654.200012,
      "user_id": 1,
      "items": [
        {
          "id": 1,
          "title": "JetSky SEAWOO blue",
          "manufacturer": "SEAWOO",
          "on_sale": false,
          "on_stock": true,
          "sold": false,
          "engine_hs_power": 300,
          "original_price": 300,
          "discount": 12,
          "file_path": "C:\\temp\\photo.png",
          "new_price": 258,
          "user_id": 258,
          "created_at": "10/10/2022",
          "last_modified": "10/10/2022"
        }
      ]
    }
  ]
}
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
____

### Pending Payments List
**method:** `GET`\
**URL:** `/api/v1/pending-payments`

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|List of Payments objects|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Admin Error|None|

#### Response Schema
###### 200  
```json
{
  "payments": [
    {
      "id": 1,
      "amount": 115,
      "total_quantity": 8,
      "payment_at": 11654.200012,
      "state": "pending",
      "transaction_id": "laskdmoashdmoasndasd#@$#@sda___Asdasd",
      "refund_at": 11654.200012,
      "user_id": 1,
      "items": [
        {
          "id": 1,
          "title": "JetSky SEAWOO blue",
          "manufacturer": "SEAWOO",
          "on_sale": false,
          "on_stock": true,
          "sold": false,
          "engine_hs_power": 300,
          "original_price": 300,
          "discount": 12,
          "file_path": "C:\\temp\\photo.png",
          "new_price": 258,
          "user_id": 258,
          "created_at": "10/10/2022",
          "last_modified": "10/10/2022"
        }
      ]
    }
  ]
}
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
____

### Fail Payments List
**method:** `GET`\
**URL:** `/api/v1/fail-payments`

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|List of  Payments objects|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Admin Error|None|

#### Response Schema
###### 200  
```json
{
  "payments": [
    {
      "id": 1,
      "amount": 115,
      "total_quantity": 8,
      "payment_at": 11654.200012,
      "state": "pending",
      "transaction_id": "laskdmoashdmoasndasd#@$#@sda___Asdasd",
      "refund_at": 11654.200012,
      "user_id": 1,
      "items": [
        {
          "id": 1,
          "title": "JetSky SEAWOO blue",
          "manufacturer": "SEAWOO",
          "on_sale": false,
          "on_stock": true,
          "sold": false,
          "engine_hs_power": 300,
          "original_price": 300,
          "discount": 12,
          "file_path": "C:\\temp\\photo.png",
          "new_price": 258,
          "user_id": 258,
          "created_at": "10/10/2022",
          "last_modified": "10/10/2022"
        }
      ]
    }
  ]
}
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
____

### Sold Items List
**method:** `GET`\
**URL:** `/api/v1/admin-sold-items`

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|List of Item objects|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Admin Error|None|

#### Response Schema
###### 200  
```json
{
  "items": [
    {
      "id": 1,
      "title": "JetSky SEAWOO blue",
      "manufacturer": "SEAWOO",
      "on_sale": false,
      "on_stock": true,
      "sold": false,
      "engine_hs_power": 300,
      "original_price": 300,
      "discount": 12,
      "file_path": "C:\\temp\\photo.png",
      "new_price": 258,
      "user_id": 258,
      "created_at": "10/10/2022",
      "last_modified": "10/10/2022"
    }
  ]
}
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
____


### Carts List
**method:** `GET`\
**URL:** `/api/v1/carts`

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|List of Cart objects|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Admin Error|None|

#### Response Schema
###### 200  
```json
{
  "carts": [
    {
      "id": 1,
      "created_at": 11654.200012,
      "last_modified": 11654.200012,
      "user_id": 1,
      "items": [
        {
          "id": 1,
          "title": "JetSky SEAWOO blue",
          "manufacturer": "SEAWOO",
          "on_sale": false,
          "on_stock": true,
          "sold": false,
          "engine_hs_power": 300,
          "original_price": 300,
          "discount": 12,
          "file_path": "C:\\temp\\photo.png",
          "new_price": 258,
          "user_id": 258,
          "created_at": "10/10/2022",
          "last_modified": "10/10/2022"
        }
      ]
    }
  ]
}
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
____

### Available Items List
**method:** `GET`\
**URL:** `/api/v1/admin-items`

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|List of Items objects|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Admin Error|None|
#### Response Schema
###### 200  
```json
{
  "items": [
    {
      "id": 1,
      "title": "JetSky SEAWOO blue",
      "manufacturer": "SEAWOO",
      "on_sale": false,
      "on_stock": true,
      "sold": false,
      "engine_hs_power": 300,
      "original_price": 300,
      "discount": 12,
      "file_path": "C:\\temp\\photo.png",
      "new_price": 258,
      "user_id": 258,
      "created_at": "10/10/2022",
      "last_modified": "10/10/2022"
    }
  ]
}
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```

====================
=

## User


### Registration
**method:** `POST`\
**URL:** `/api/v1/register`

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successfully registration|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|User Error|None|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|No connection Error|None|

#### Request Schema
```json
{
  "email": "shoppa@shoppa.pro",
  "password": "AAaa1234!@"
}
```

#### Response Schema
###### 200  
```json
{
  "message": "User successfully Registered!"
}
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
###### 500
```json
{
"message": "Error occurred.",
"details": "details"
}
```
____



### User Login
**method:** `POST`\
**URL:** `/api/v1/login`

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successfully login|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|User Error|None|

#### Request Schema
```json
{
  "email": "shoppa@shoppa.pro",
  "password": "AAaa1234!@"
}
```

#### Response Schema
###### 200  
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
----

### User Logout
**method:** `POST`\
**URL:** `/api/v1/logout`

***Authentication** is needed to perform Admin actions.*

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successfully Logout|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|

#### Response Schema
###### 200  
```json
{
  "message": "User successfully logged out."
}
```

###### 400
```json
{
"message": "Error occurred.",
"details": "details"
}
```
----

### User Token Refresh
**method:** `GET`\
**URL:** `/api/v1/refresh`

***Authentication** is needed to perform Admin actions.*

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successfully Refresh|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|

#### Response Schema
###### 200  
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

###### 400
```json
{
"message": "Error occurred.",
"details": "details"
}
```
----


### Change Password
**method:** `PUT`\
**URL:** `/api/v1/change-password`

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|Successfully Confirm|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|

#### Request Schema
```json
{
  "confirmation": "asdasldhaosfh123213WQDSAD",
  "password": "AAaa1234!@",
  "confirm_password": "AAaa1234!@"
}
```

#### Response Schema
###### 201  
```json
{
  "message": "Password Changed"
}
```

###### 400
```json
{
"message": "Error occurred.",
"details": "details"
}
```
----

### Send Password Email Confirmation
**method:** `POST`\
**URL:** `/api/v1/change-password`

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successfully Confirm|string|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|

#### Request Schema
```json
{
  "email": "shoppa@shoppa.pro"
}
```

#### Response Schema
###### 200  
```json
{
  "message": "Successful Confirm"
}
```

###### 400
```json
{
"message": "Error occurred.",
"details": "details"
}
```
----

### Register Subscriber
**method:** `POST`\
**URL:** `/api/v1/subscriber`

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|Registration Successfully Confirm|string|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|User Error|None|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|General Error|None|

#### Request Schema
```json
{
  "email": "shoppa@shoppa.pro"
}
```

#### Response Schema
###### 201  
```json
{
  "message": "Registration Successful Confirm"
}
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
----

### Remove Subscriber
**method:** `DELETE`\
**URL:** `/api/v1/subscriber`

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|Registration Successfully Confirm|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|User Error|None|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|General Error|None|

#### Request Schema
```json
{
  "email": "shoppa@shoppa.pro"
}
```

#### Response Schema
###### 201  
```json
{
  "message": "Subscriber Request Processed Successfully"
}
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
----

### User Payments
**method:** `GET`\
**URL:** `/api/v1/payment`

***Authentication** is needed to perform Admin actions.*

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|List of User pending or paid Payment objects|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|

#### Response Schema
###### 200  
```json
{
  "payments": [
    {
      "id": 1,
      "amount": 115,
      "total_quantity": 8,
      "payment_at": 11654.200012,
      "state": "pending",
      "transaction_id": "laskdmoashdmoasndasd#@$#@sda___Asdasd",
      "refund_at": 11654.200012,
      "user_id": 1,
      "items": [
        {
          "id": 1,
          "title": "JetSky SEAWOO blue",
          "manufacturer": "SEAWOO",
          "on_sale": false,
          "on_stock": true,
          "sold": false,
          "engine_hs_power": 300,
          "original_price": 300,
          "discount": 12,
          "file_path": "C:\\temp\\photo.png",
          "new_price": 258,
          "user_id": 258,
          "created_at": "10/10/2022",
          "last_modified": "10/10/2022"
        }
      ]
    }
  ]
}
```

###### 400
```json
{
"message": "Error occurred.",
"details": "details"
}
```
----

### User Payment
**method:** `POST`\
**URL:** `/api/v1/payment`

***Authentication** is needed to perform Admin actions.*

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|User Payment object|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|User Error|None|
|402|[Payment Required](https://tools.ietf.org/html/rfc7231#section-6.5.2)|Cart Error|None|

#### Request Schema
```json
{
  "token": "uhsadmoajsdSADSA14342"
}
```

#### Response Schema
###### 200  
```json
{
  "payment": {
    "id": 1,
    "amount": 115,
    "total_quantity": 8,
    "payment_at": 11654.200012,
    "state": "pending",
    "transaction_id": "laskdmoashdmoasndasd#@$#@sda___Asdasd",
    "refund_at": 11654.200012,
    "user_id": 1,
    "items": [
      {
        "id": 1,
        "title": "JetSky SEAWOO blue",
        "manufacturer": "SEAWOO",
        "on_sale": false,
        "on_stock": true,
        "sold": false,
        "engine_hs_power": 300,
        "original_price": 300,
        "discount": 12,
        "file_path": "C:\\temp\\photo.png",
        "new_price": 258,
        "user_id": 258,
        "created_at": "10/10/2022",
        "last_modified": "10/10/2022"
      }
    ]
  }
}
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
----

### User Refunds
**method:** `GET`\
**URL:** `/api/v1/refund`

***Authentication** is needed to perform Admin actions.*

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|List of User refund Payment objects|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|

#### Response Schema
###### 200  
```json
{
  "refunds": [
    {
      "id": 1,
      "amount": 115,
      "total_quantity": 8,
      "payment_at": 11654.200012,
      "state": "pending",
      "transaction_id": "laskdmoashdmoasndasd#@$#@sda___Asdasd",
      "refund_at": 11654.200012,
      "user_id": 1,
      "items": [
        {
          "id": 1,
          "title": "JetSky SEAWOO blue",
          "manufacturer": "SEAWOO",
          "on_sale": false,
          "on_stock": true,
          "sold": false,
          "engine_hs_power": 300,
          "original_price": 300,
          "discount": 12,
          "file_path": "C:\\temp\\photo.png",
          "new_price": 258,
          "user_id": 258,
          "created_at": "10/10/2022",
          "last_modified": "10/10/2022"
        }
      ]
    }
  ]
}
```

###### 400
```json
{
"message": "Error occurred.",
"details": "details"
}
```
----

### User Refund
**method:** `POST`\
**URL:** `/api/v1/refund`

***Authentication** is needed to perform Admin actions.*

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|User Payment object|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|User Error|None|
|402|[Payment Required](https://tools.ietf.org/html/rfc7231#section-6.5.2)|Payment Error|None|

#### Request Schema
```json
{
  "transaction_id": "uhsadmoajsdSADSA14342"
}
```

#### Response Schema
###### 200  
```json
{
  "refund": {
    "id": 1,
    "amount": 115,
    "total_quantity": 8,
    "payment_at": 11654.200012,
    "state": "pending",
    "transaction_id": "laskdmoashdmoasndasd#@$#@sda___Asdasd",
    "refund_at": 11654.200012,
    "user_id": 1,
    "items": [
      {
        "id": 1,
        "title": "JetSky SEAWOO blue",
        "manufacturer": "SEAWOO",
        "on_sale": false,
        "on_stock": true,
        "sold": false,
        "engine_hs_power": 300,
        "original_price": 300,
        "discount": 12,
        "file_path": "C:\\temp\\photo.png",
        "new_price": 258,
        "user_id": 258,
        "created_at": "10/10/2022",
        "last_modified": "10/10/2022"
      }
    ]
  }
}
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
----


### Show User Cart
**method:** `GET`\
**URL:** `/api/v1/cart`

***Authentication** is needed to perform Admin actions.*

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Show Cart|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|
|403|[Forbidden](https://tools.ietf.org/html/rfc7231#section-6.5.3)|Cart Error|None|

#### Response Schema
###### 200  
```json
{
  "items": [
    {
      "ids": [
        [
          2,
          5,
          8
        ]
      ],
      "quantity": 3,
      "title": "JetSky SEAWOO blue",
      "manufacturer": "SEAWOO",
      "on_sale": false,
      "on_stock": true,
      "sold": false,
      "engine_hs_power": 300,
      "original_price": 300,
      "discount": 12,
      "file_path": "C:\\temp\\photo.png",
      "new_price": 258,
      "user_id": 258,
      "created_at": "10/10/2022",
      "last_modified": "10/10/2022"
    }
  ],
  "quantity": 6,
  "amount": 2555
}
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
----

### Remove User Cart
**method:** `DELETE`\
**URL:** `/api/v1/cart`

***Authentication** is needed to perform Admin actions.*

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Remove Cart|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|

#### Response Schema
###### 200  
```json
[
  {
    "items": [],
    "quantity": 0,
    "amount": 0
  }
]
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
----

### Add Item to Cart
**method:** `POST`\
**URL:** `/api/v1/cart/item`

***Authentication** is needed to perform Admin actions.*

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Show Cart|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Cart Error|None|
|402|[Payment Required](https://tools.ietf.org/html/rfc7231#section-6.5.2)|Item Error|None|

#### Request Schema
```json
{
  "item_id": 7
}
```

#### Response Schema
###### 200  
```json
{
  "message": "Item Add/Removed successfully"
}
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
----

### Remove Item to Cart
**method:** `DELETE`\
**URL:** `/api/v1/cart/item`

***Authentication** is needed to perform Admin actions.*

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Remove Cart|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|Cart Error|None|
|402|[Payment Required](https://tools.ietf.org/html/rfc7231#section-6.5.2)|Item Error|None|

#### Request Schema
```json
{
  "item_id": 7
}
```

#### Response Schema
###### 200  
```json
{
  "message": "Item Add/Removed successfully"
}
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```

====================
=

## Confirmation

### Registration Email Confirmation
**method:** `GET`\
**URL:** `/api/v1/confirmation`

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Registration Successfully Confirm|string|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|General Error|None|

#### Request Schema
```json
{
  "email": "shoppa@shoppa.pro",
  "confirmation_id": "sadfumaihfAFcAFCQrc0q398urSADASDQ$@2314213"
}
```

#### Response Schema
###### 200  
```json
{
  "message": "Registration Successfully Confirm"
}
```

###### 401
```json
{
"message": "Error occurred.",
"details": "details"
}
```
---

### Change Password Email Confirmation
**method:** `GET`\
**URL:** `/api/v1/change-password`

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successfully Change Password Email Confirmation|string|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|General Error|None|

#### Request Schema
```json
{
  "email": "shoppa@shoppa.pro",
  "confirmation_id": "sadfumaihfAFcAFCQrc0q398urSADASDQ$@2314213"
}
```

#### Response Schema
###### 200  
```json
{
  "message": "Registration Successfully Confirm"
}
```

###### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
----

### Subscriber Email Confirmation
**method:** `GET`\
**URL:** `/api/v1/subscriber`

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Registration Successfully Confirm|string|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|User Error|None|
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|General Error|None|

#### Request Schema
```json
{
  "email": "shoppa@shoppa.pro",
  "confirmation_id": "sadfumaihfAFcAFCQrc0q398urSADASDQ$@2314213"
}
```

#### Response Schema
###### 200  
```json
{
  "message": "Registration Successfully Confirm"
}
```

###### 401
```json
{
"message": "Error occurred.",
"details": "details"
}
```

====================
=

## Item

### Show Single Item
**method:** `GET`\
**URL:** `/api/v1/item`

***Authentication** is needed to perform User actions.*

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Show Item|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|

#### Request Schema
```json
{
  "id": 7
}
```

#### Response Schema
###### 200  
```json
{
  "item": {
    "id": 1,
    "title": "JetSky SEAWOO blue",
    "manufacturer": "SEAWOO",
    "on_sale": false,
    "on_stock": true,
    "sold": false,
    "engine_hs_power": 300,
    "original_price": 300,
    "discount": 12,
    "file_path": "C:\\\\temp\\photo.png",
    "new_price": 258,
    "user_id": 258,
    "created_at": "10/10/2022",
    "last_modified": "10/10/2022"
  }
}
```

###### 400
```json
{
"message": "Error occurred.",
"details": "details"
}
```
----

### List of Items Manufacture
**method:** `GET`\
**URL:** `/api/v1/items-manufacture`

***Authentication** is needed to perform User actions.*

#### Responses
|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Show Item|None|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|General Error|None|

#### Request Schema
```json
{
  "manufacturer": "DEAWOO"
}
```

#### Response Schema
###### 200  
```json
{
  "items": [
    {
      "id": 1,
      "title": "JetSky SEAWOO blue",
      "manufacturer": "SEAWOO",
      "on_sale": false,
      "on_stock": true,
      "sold": false,
      "engine_hs_power": 300,
      "original_price": 300,
      "discount": 12,
      "file_path": "C:\\\\temp\\photo.png",
      "new_price": 258,
      "user_id": 258,
      "created_at": "10/10/2022",
      "last_modified": "10/10/2022"
    }
  ]
}
```

###### 400
```json
{
"message": "Error occurred.",
"details": "details"
}
```
----
