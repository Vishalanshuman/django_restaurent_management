
# Restaurant Management System

This project is a Django REST API for managing restaurant operations, including user registration, food item management, order creation, and recommendations.

## Features

- **User Registration and Authentication**: Allows users to register and log in using JWT tokens.
- **Food Item Management**: Admin can create, update, and delete food items.
- **Order Management**: Customers can place orders, and admins can manage all orders.
- **Recommendations**: Provides food recommendations based on the user's previous orders.
- **Pagination and Filtering**: Support for paginated and filtered views for food items and orders.
- **Swagger Documentation**: The API is documented using Swagger (drf-yasg).
  
## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Vishalanshuman/django_restorent_management.git
   ```

2. Navigate into the project directory:

   ```bash
   cd django_restorent_management
   ```

3. Set up a virtual environment:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scriptsctivate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

5. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Run database migrations:

   ```bash
   python manage.py migrate
   ```

7. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

8. Start the Django development server:

   ```bash
   python manage.py runserver
   ```

## API Endpoints

- **POST `/api/register/`**: Register a new user.
- **POST `/api/login/`**: Obtain JWT tokens for login.
- **GET `/api/food-items/`**: List all food items (with pagination and filtering).
- **POST `/api/food-items/`**: Create a new food item (admin only).
- **GET `/api/orders/`**: List orders (for authenticated users and admins).
- **POST `/api/orders/`**: Create a new order.
- **PUT `/api/orders/{order_id}/`**: Update an order (admin only).
- **PATCH `/api/orders/{order_id}/status/`**: Admin can update the status of an order.

## Authentication

- JWT authentication is used for login.
- Access token is obtained by logging in through the `/api/login/` endpoint.
- Include the `Authorization: Bearer <access_token>` header in subsequent API requests.

## Project Structure

```
django_restorent_management/
│
├── django_restorent_management/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── restaurant/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── ...
│
├── manage.py
└── requirements.txt
```

## Testing

- To run tests:

  ```bash
  pytest
  ```
