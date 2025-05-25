# API Documentation

## Table of Contents
1. [Authentication](#authentication)
   - [Register User](#register-user)
   - [Login](#login)
   - [Get Current User](#get-current-user)
   - [Logout](#logout)
2. [Users](#users)
   - [List Users](#list-users)
   - [Get User by ID](#get-user-by-id)
   - [Update User](#update-user)
   - [Delete User](#delete-user)
3. [Documents](#documents)
   - [Upload Document](#upload-document)
   - [List Documents](#list-documents)
   - [Get Document](#get-document)
   - [Update Document](#update-document)
   - [Delete Document](#delete-document)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting)
6. [Pagination](#pagination)

## Base URL
All API endpoints are relative to the base URL:
```
http://localhost:8000
```

## Authentication

### Register User
Register a new user account.

**Endpoint**: `POST /api/auth/register`

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe",
  "role": "viewer"
}
```

**Roles**: `admin`, `editor`, `viewer`

**Response**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "viewer",
  "is_active": true,
  "created_at": "2023-05-25T12:00:00Z"
}
```

### Login
Authenticate and receive an access token.

**Endpoint**: `POST /api/auth/token`

**Form Data**:
- `username`: User's email
- `password`: User's password

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get Current User
Get the currently authenticated user's details.

**Endpoint**: `GET /api/auth/me`

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "viewer",
  "is_active": true
}
```

### Logout
Invalidate the current access token.

**Endpoint**: `POST /api/auth/logout`

**Headers**:
```
Authorization: Bearer <access_token>
```

**Response**:
```json
{
  "message": "Successfully logged out"
}
```

## Users

### List Users
Get a paginated list of all users (Admin only).

**Endpoint**: `GET /api/users/`

**Query Parameters**:
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 10, max: 100)

**Response**:
```json
{
  "items": [
    {
      "id": 1,
      "email": "admin@example.com",
      "full_name": "Admin User",
      "role": "admin",
      "is_active": true
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 10
}
```

### Get User by ID
Get a specific user by ID (Admin only).

**Endpoint**: `GET /api/users/{user_id}`

**Response**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "viewer",
  "is_active": true,
  "created_at": "2023-05-25T12:00:00Z"
}
```

### Update User
Update a user's information (Admin only).

**Endpoint**: `PUT /api/users/{user_id}`

**Request Body**:
```json
{
  "full_name": "Updated Name",
  "role": "editor"
}
```

### Delete User
Delete a user (Admin only).

**Endpoint**: `DELETE /api/users/{user_id}`

**Response**:
```json
{
  "message": "User deleted successfully"
}
```

## Documents

### Upload Document
Upload a new document (Admin/Editor only).

**Endpoint**: `POST /api/documents/`

**Form Data**:
- `file`: The file to upload
- `title`: Document title
- `description`: Document description
- `file_type`: File type (e.g., pdf, docx)

**Response**:
```json
{
  "id": 1,
  "title": "Example Document",
  "description": "This is an example document",
  "file_type": "pdf",
  "file_path": "/uploads/documents/example.pdf",
  "owner_id": 1,
  "created_at": "2023-05-25T12:00:00Z"
}
```

### List Documents
Get a paginated list of documents.

**Endpoint**: `GET /api/documents/`

**Query Parameters**:
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 10, max: 100)

### Get Document
Get document details by ID.

**Endpoint**: `GET /api/documents/{document_id}`

### Update Document
Update document metadata or file (Admin/Editor only).

**Endpoint**: `PUT /api/documents/{document_id}`

### Delete Document
Delete a document (Admin only).

**Endpoint**: `DELETE /api/documents/{document_id}`

## Error Handling

### Common Error Responses

**400 Bad Request**
```json
{
  "detail": "Invalid request data"
}
```

**401 Unauthorized**
```json
{
  "detail": "Could not validate credentials"
}
```

**403 Forbidden**
```json
{
  "detail": "Not enough permissions"
}
```

**404 Not Found**
```json
{
  "detail": "Resource not found"
}
```

**422 Validation Error**
```json
{
  "detail": [
    {
      "loc": ["string", 0],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Rate Limiting
- 100 requests per minute per IP for unauthenticated endpoints
- 1000 requests per minute per user for authenticated endpoints

## Pagination
All list endpoints support pagination using `skip` and `limit` query parameters.

**Example**:
```
GET /api/documents/?skip=10&limit=5
```
