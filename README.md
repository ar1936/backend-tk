# 📚 SecureDoc Manager

A modern, secure, and scalable document management system built with FastAPI, designed to streamline document handling with robust access controls and efficient file management capabilities.

## 🚀 Key Features

### 🔒 Security & Access
- **JWT Authentication**: Secure user authentication with JSON Web Tokens
- **Role-Based Access Control**: Granular permissions (Admin, Editor, Viewer)
- **Password Protection**: Industry-standard bcrypt hashing
- **CORS Protection**: Configured for secure cross-origin requests

### 📄 Document Management
- **File Upload & Storage**: Support for multiple document formats
- **Metadata Management**: Title, description, and file type tracking
- **Version Control**: Track document changes and history
- **Efficient Retrieval**: Paginated document listing with filtering

### 🛠 Technical Highlights
- **RESTful API**: Clean, intuitive endpoints following REST principles
- **Asynchronous Processing**: Built with Python's async/await for performance
- **Containerized**: Ready for Docker deployment
- **Comprehensive Testing**: Unit, integration, and load testing
- **Automated Workflows**: CI/CD ready with GitHub Actions

## 🏗 Technology Stack

| Category       | Technology           |
|----------------|----------------------|
| **Backend**    | Python 3.8+, FastAPI |
| **Database**   | PostgreSQL 13+       |
| **ORM**        | SQLAlchemy 1.4+      |
| **Auth**       | OAuth2 with JWT      |
| **Container**  | Docker, Docker Compose|
| **Testing**    | pytest, Locust       |
| **Docs**       | OpenAPI, Swagger UI  |


## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 13+
- Docker (optional, for containerized deployment)
- pip (Python package manager)

### Quick Start with Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/secure-doc-manager.git
   cd secure-doc-manager/backend
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. Start services:
   ```bash
   docker-compose up --build -d
   ```

4. Access the API:
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc

### Manual Installation

1. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up PostgreSQL database and update `.env`

4. Run database migrations:
   ```bash
   alembic upgrade head
   ```

5. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## 📚 API Documentation

### Authentication
All endpoints (except `/api/auth/register` and `/api/auth/token`) require authentication via JWT token in the `Authorization` header:
```
Authorization: Bearer your_jwt_token_here
```

### Available Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/token` - Obtain access token
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - Invalidate token

#### Users (Admin Only)
- `GET /api/users/` - List all users
- `GET /api/users/{id}` - Get user by ID
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user

#### Documents
- `POST /api/documents/` - Upload document (Admin/Editor)
- `GET /api/documents/` - List documents
- `GET /api/documents/{id}` - Get document
- `PUT /api/documents/{id}` - Update document (Admin/Editor)
- `DELETE /api/documents/{id}` - Delete document (Admin)

## 🧪 Testing

### Unit & Integration Tests
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html
```

### Load Testing with Locust
```bash
# Start Locust web interface
locust -f tests/locustfile.py

# Or run in headless mode
locust -f tests/locustfile.py --headless --users 100 --spawn-rate 5 --run-time 1m
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with these variables:
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Authentication
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 hours

# CORS (comma-separated origins)
CORS_ORIGINS=http://localhost:3000,http://localhost:4200
```

## 🚀 Deployment

### Docker Production Setup
1. Update `docker-compose.prod.yml` with your production settings
2. Build and start:
   ```bash
   docker-compose -f docker-compose.prod.yml up --build -d
   ```

### Cloud Deployment
- **AWS**: Deploy using ECS/EKS with RDS
- **GCP**: Use Cloud Run with Cloud SQL
- **Azure**: Deploy to App Service with Azure Database for PostgreSQL

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

For support or questions, please open an issue in the repository or contact [your-email@example.com](mailto:your-email@example.com)

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- SQLAlchemy for powerful ORM capabilities
- PostgreSQL for reliable data storage
- All open-source contributors

---

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/token` - Login and get access token (form data)
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - Logout

#### Register
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123","full_name":"Test User", "role":"viewer"}'
```
#### Login
```bash
curl -X POST "http://localhost:8000/api/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"
```
#### Get Current User
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```
#### Logout
```bash
curl -X POST "http://localhost:8000/api/auth/logout" \
  -H "Authorization: Bearer $TOKEN"
```

---

### User Management (Admin only for some endpoints)
- `GET /api/users/` - List all users (Admin only)
- `GET /api/users/{user_id}` - Get user by ID (Admin only)
- `PUT /api/users/{user_id}` - Update user info (Admin only)
- `DELETE /api/users/{user_id}` - Delete user (Admin only)

#### List Users
```bash
curl -X GET "http://localhost:8000/api/users/" \
  -H "Authorization: Bearer $TOKEN"
```
#### Get User by ID
```bash
curl -X GET "http://localhost:8000/api/users/3" \
  -H "Authorization: Bearer $TOKEN"
```
#### Update User
```bash
curl -X PUT "http://localhost:8000/api/users/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"full_name": "Updated Name", "role": "editor"}'
```
#### Delete User
```bash
curl -X DELETE "http://localhost:8000/api/users/1" \
  -H "Authorization: Bearer $TOKEN"
```

---

### Document Management
- `POST /api/documents/` - Upload a new document (Admin/Editor only)
- `GET /api/documents/` - List all documents
- `GET /api/documents/{document_id}` - Get a specific document
- `PUT /api/documents/{document_id}` - Update document metadata (Admin/Editor only)
- `DELETE /api/documents/{document_id}` - Delete a document (Admin only)

#### Upload Document
```bash
curl -X POST "http://localhost:8000/api/documents/" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test.pdf" \
  -F "title=Test Document" \
  -F "description=This is a test document" \
  -F "file_type=pdf"
```
#### List Documents
```bash
curl -X GET "http://localhost:8000/api/documents/" \
  -H "Authorization: Bearer $TOKEN"
```
#### Get Document
```bash
curl -X GET "http://localhost:8000/api/documents/1" \
  -H "Authorization: Bearer $TOKEN"
```
#### Update Document (metadata only)
```bash
curl -X PUT "http://localhost:8000/api/documents/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Document", "description": "Updated description", "file_type": "pdf"}'
```
#### Update Document (with file)
```bash
curl -X PUT "http://localhost:8000/api/documents/1" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@updated.pdf" \
  -F "title=Updated Document" \
  -F "description=Updated description" \
  -F "file_type=pdf"
```
#### Delete Document
```bash
curl -X DELETE "http://localhost:8000/api/documents/1" \
  -H "Authorization: Bearer $TOKEN"
```

---

### Ingestion
- `GET /api/ingestion/` - List all ingestion logs (Admin/Editor only)
- `POST /api/ingestion/trigger` - Trigger document ingestion (Admin/Editor only)
- `GET /api/ingestion/status` - Get ingestion status (Admin/Editor only)

#### List Ingestion Logs
```bash
curl -X GET "http://localhost:8000/api/ingestion/" \
  -H "Authorization: Bearer $TOKEN"
```
#### Trigger Ingestion
```bash
curl -X POST "http://localhost:8000/api/ingestion/trigger" \
  -H "Authorization: Bearer $TOKEN"
```
#### Get Ingestion Status
```bash
curl -X GET "http://localhost:8000/api/ingestion/status" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Environment Setup

### .env Example
Create a `.env` file in the project root:
```env
POSTGRES_SERVER=db
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
CORS_ALLOWED_ORIGINS=http://localhost:4200,http://127.0.0.1:4200
```

---

## Running with Docker

1. **Build and start all services:**
```bash
docker-compose up --build -d
```
2. **Stop all services:**
```bash
docker-compose down
```
3. **View logs:**
```bash
docker-compose logs -f
```
4. **Access the API:**
- FastAPI docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Manual Local Setup (without Docker)

1. **Install dependencies:**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
2. **Start PostgreSQL** and create the database/tables (see `init.sql` for schema).
3. **Set up your `.env` file** as above.
4. **Run the app:**
```bash
uvicorn app.main:app --reload
```

---

## Testing

1. **Run all tests:**
```bash
./run_tests.sh all
```
2. **Run a specific test file:**
```bash
pytest tests/test_documents.py
```
3. **Generate a coverage report:**
```bash
pytest --cov=app --cov-report=html
```
4. **View coverage report:**
Open `htmlcov/index.html` in your browser.

---

## Load Testing

1. **Start the app:**
```bash
docker-compose up -d
```
2. **Run load tests:**
```bash
./run_load_tests.sh
```
3. **Open Locust UI:**
[http://localhost:8089](http://localhost:8089)

---

## Database Schema

- `users` - User accounts
- `documents` - Document metadata and file info
- `ingestion_logs` - Ingestion process logs

See `init.sql` for full schema.

---

## Security
- Passwords hashed with bcrypt
- JWT authentication
- Role-based access control
- CORS configuration

---

## Error Handling
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

