# Flask + MongoDB Backend – Local Setup with Docker

## Run Locally Using Docker

### .env

```env
MONGO_URI=mongodb://mongo:27017/usersdb
SECRET_KEY=your-secret-key
```

### 1. Start the Containers

In the root directory (where `docker-compose.yml` is located), run:

```bash
docker-compose up --build -d
```

This will:

-   Build the Flask app image
-   Start MongoDB and Flask containers in the background
-   Wait for MongoDB to be healthy before launching Flask

### 2. Check if Containers Are Running

```bash
docker-compose ps
```

You should see something like:

```
NAME                     SERVICE     STATUS
flask-crud-flask-app-1   flask-app   running
flask-crud-mongo-1       mongo       running (healthy)
```

### 3. Access the API

The backend is now live at:

```
http://localhost:5000
```

---

## Test Endpoints with Postman

Use Postman to send requests to the API.

### 1. Create a User

**POST** `http://localhost:5000/users`

```json
{
    "name": "Alice",
    "email": "alice@example.com",
    "password": "secret123"
}
```

### 2. Get All Users

**GET** `http://localhost:5000/users`

### 3. Get a User by ID

**GET** `http://localhost:5000/users/U240405000001`

Replace with actual `user_id` returned from the create response.

### 4. Update a User

**PUT** `http://localhost:5000/users/U240405000001`

```json
{
    "name": "Alice Updated",
    "email": "alice@newdomain.com",
    "password": "newpass123"
}
```

### 5. Delete a User

**DELETE** `http://localhost:5000/users/U240405000001`

---

## Stop the Server

To stop and remove the containers:

```bash
docker-compose down
```
