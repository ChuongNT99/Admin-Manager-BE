# Room Management API Documentation

This documentation provides details on how to use the Room Management API.

## Base URL
The base URL for all endpoints is `http://localhost:5000` when running locally.

## Get List of Rooms

### GET /rooms

Get a list of all meeting rooms.

#### Request

- Method: `GET`
- URL: `/rooms`

#### Response

- Status: 200 OK
- Content-Type: application/json

```json
{
  "rooms": [
    {
      "room_id": 1,
      "room_name": "Room A",
      "status": "Available"
    },
    {
      "room_id": 2,
      "room_name": "Room B",
      "status": "Occupied"
    }
    // ... other rooms
  ]
}

Create a Room
POST /rooms
Create a new meeting room.

Request
Method: POST
URL: /rooms
Content-Type: application/json
Body:
{
  "room_name": "New Room",
  "status": "Available"
}
Response
Status: 201 Created
Content-Type: application/json
{
  "message": "Room created successfully"
}

# Room Management API Documentation

This documentation provides details on how to use the Room Management API.

## Base URL
The base URL for all endpoints is `http://localhost:5000` when running locally.

## Get List of Rooms

### GET /rooms

Get a list of all meeting rooms.

#### Request

- Method: `GET`
- URL: `/rooms`

#### Response

- Status: 200 OK
- Content-Type: application/json

```json
{
  "rooms": [
    {
      "room_id": 1,
      "room_name": "Room A",
      "status": "Available"
    },
    {
      "room_id": 2,
      "room_name": "Room B",
      "status": "Occupied"
    }
    // ... other rooms
  ]
}
Create a Room
POST /rooms
Create a new meeting room.

Request
Method: POST
URL: /rooms
Content-Type: application/json
Body:
json
{
  "room_name": "New Room",
  "status": "Available"
}
Response
Status: 201 Created
Content-Type: application/json
json
{
  "message": "Room created successfully"
}

Update a Room
PUT /rooms/:room_id
Update an existing meeting room by its ID.

Request
Method: PUT
URL: /rooms/:room_id
Content-Type: application/json
Body:
{
  "room_name": "Updated Room",
  "status": "Occupied"
}
Response
Status: 200 OK
Content-Type: application/json
{
  "message": "Room updated successfully"
}

Delete a Room
DELETE /rooms/:room_id
Delete a meeting room by its ID.

Request
Method: DELETE
URL: /rooms/:room_id
Response
Status: 200 OK
Content-Type: application/json

{
  "message": "Room deleted successfully"
}

Error Responses
If an error occurs, the API will respond with an error message and the appropriate HTTP status code.

Status: 400 Bad Request
Status: 404 Not Found

{
  "error": "Invalid request data"
}

{
  "error": "Room not found"
}

