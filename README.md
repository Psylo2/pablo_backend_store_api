# Shop API
### Documentation

## Authentication
**HTTP:** *Bearer*\
**HTTP Authorization Scheme:** *bearer*\
**Bearer format:** *JWT*

## Admin
*Authentication is needed to perform Admin actions.*

### Users List
`GET /api/v1/users`

#### Responses

|Status|Meaning|Description| Schema        |
|---|---|---|---------------|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|List of User objects| List of users |
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|User Error| Error message |
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|General Error| Error message |


#### Response Schema

##### 200 
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
##### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
-------------------------------------
### Blocked Users List
`GET /api/v1/users/blocked`

#### Responses

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|List of User objects| List of users |
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|User Error| Error message |
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|General Error| Error message |

#### Response Schema

##### 200 
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

##### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
----------------


### Allowed Users List

`GET /api/v1/users/allowed`

#### Responses

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|List of User objects| List of users |
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|User Error| Error message |
|401|[Unauthorized](https://tools.ietf.org/html/rfc7235#section-3.1)|General Error| Error message |

#### Response Schema

##### 200 
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

##### 40X
```json
{
"message": "Error occurred.",
"details": "details"
}
```
----------------
