# Project Architecture

The application is designed to be modular, maintainable, and database-agnostic. It primarily uses **FastAPI**, **Pydantic**, and **SQLAlchemy** and manages dependencies using **Poetry**.

## **Folder Structure**

Below is the high-level folder structure:

```
📦
├─ .gitignore
├─ .vscode
│  └─ settings.json
├─ README.md
├─ alembic.ini
├─ app
│  ├─ __init__.py
│  ├─ api
│  │  ├─ __init__.py
│  │  ├─ dto
│  │  │  ├─ __init__.py
│  │  │  ├─ change_shop_owner_request.py
│  │  │  ├─ create_account_dto.py
│  │  │  ├─ create_product_dto.py
│  │  │  ├─ create_shop_request.py
│  │  │  ├─ login_dto.py
│  │  │  ├─ login_user_dto.py
│  │  │  ├─ product_dto.py
│  │  │  ├─ product_list_dto.py
│  │  │  ├─ shop_dto.py
│  │  │  ├─ shop_list_dto.py
│  │  │  ├─ update_product_dto.py
│  │  │  ├─ update_shop_request.py
│  │  │  └─ user_list_dto.py
│  │  └─ v1
│  │     ├─ __init__.py
│  │     ├─ controller
│  │     │  ├─ __init__.py
│  │     │  ├─ product_controller.py
│  │     │  ├─ shop_controller.py
│  │     │  └─ user_controller.py
│  │     └─ v1_router.py
│  ├─ app_container.py
│  ├─ common
│  │  ├─ __init__.py
│  │  ├─ app_logger.py
│  │  ├─ error
│  │  │  ├─ __init__.py
│  │  │  └─ response_exception.py
│  │  ├─ model
│  │  │  ├─ __init__.py
│  │  │  ├─ app_config.py
│  │  │  ├─ error_response.py
│  │  │  └─ user_info.py
│  │  └─ util
│  │     ├─ __init__.py
│  │     ├─ dto_util.py
│  │     ├─ jwt_util.py
│  │     └─ request_util.py
│  ├─ configuration
│  │  ├─ __init__.py
│  │  ├─ global_exception_handler.py
│  │  ├─ jwt_middleware.py
│  │  └─ swagger_config.py
│  ├─ domain
│  │  ├─ __init__.py
│  │  ├─ entity
│  │  │  ├─ __init__.py
│  │  │  ├─ login_user.py
│  │  │  ├─ product.py
│  │  │  ├─ shop.py
│  │  │  ├─ user.py
│  │  │  └─ user_detail.py
│  │  ├─ repository
│  │  │  ├─ product_repo.py
│  │  │  ├─ shop_repo.py
│  │  │  └─ user_repo.py
│  │  ├─ service
│  │  │  ├─ __init__.py
│  │  │  ├─ product_service.py
│  │  │  ├─ shop_service.py
│  │  │  └─ user_service.py
│  │  └─ unit_of_work
│  │     ├─ transaction.py
│  │     └─ transaction_manager.py
│  ├─ infrastructure
│  │  ├─ __init__.py
│  │  ├─ repository
│  │  │  ├─ __init__.py
│  │  │  ├─ product_repo.py
│  │  │  ├─ shop_repo.py
│  │  │  └─ user_repo.py
│  │  ├─ table
│  │  │  ├─ __init__.py
│  │  │  ├─ base.py
│  │  │  ├─ order_item_table.py
│  │  │  ├─ order_table.py
│  │  │  ├─ product_table.py
│  │  │  ├─ shop_table.py
│  │  │  └─ user_table.py
│  │  └─ unit_of_work
│  │     ├─ __init__.py
│  │     ├─ transaction.py
│  │     └─ transaction_manager.py
│  └─ main.py
├─ docker-compose.yml
├─ migration
│  ├─ README
│  ├─ env.py
│  ├─ script.py.mako
│  └─ versions
│     └─ e48a12275147_initial_migration.py
├─ mypy.ini
├─ pyproject.toml
└─ test
   ├─ __init__.py
   └─ domain
      └─ service
         └─ user_service.py

```

### **Key Layers**

The application is divided into three main layers, along with supporting layers like configuration and common utilities:

### **1. Domain Layer**

- **Description:**

The **domain layer** is the core of the application where business logic resides. This layer is **independent**, meaning it does not depend on the API or infrastructure layers, making it reusable and testable.

- **Key Components:**
    - **Entities:** Define domain-specific models (e.g., `User`, `Product`, `Shop`) in `domain/entity`.
    - **Repositories (Abstract):** Define repository interfaces that outline methods like `save_user` or `get_user_by_id` without implementation.
    - **Services:** Business logic is implemented in service classes (e.g., `UserService`, `ProductService`), where each method handles specific operations. These methods use unit-of-work patterns to manage database transactions.
    - **Unit of Work (Abstract):** Manages transactions and ensures consistency across repository operations. This abstraction ensures the domain layer remains database-agnostic.
- **Example Workflow:**
    
    ```python
    
    async def create_account(self, username: str, password: str) -> User:
        async with self.transaction_manager.get_transaction() as transaction:
            if await self.user_repo.is_username_exists(transaction, username):
                raise BadRequestException("Username already exists")
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user = await self.user_repo.create_user(transaction, username, hashed_password)
            await transaction.commit()
            return user
    
    ```
    

**Why Abstract Layers?**

By using abstract repositories and unit-of-work patterns, the application can switch databases or persistence layers without modifying the domain logic.

---

### **2. API Layer**

- **Description:**
    
    The **API layer** exposes application functionality via RESTful endpoints. It serves as the entry point for handling user requests.
    
- **Key Components:**
    - **DTOs (Data Transfer Objects):** Define request and response models using Pydantic for validation and serialization.
    - **Controllers:** Define API endpoints and handle request/response flows. They:
        1. Validate input using DTOs.
        2. Convert input to domain entities.
        3. Pass the data to the service layer for processing.
        4. Convert service outputs into DTOs for API responses.
- **Flow Example:**
    1. A request hits an API endpoint in a controller (e.g., `create_product`).
    2. Input is validated using a Pydantic schema.
    3. Data is passed to a domain service (e.g., `ProductService`).
    4. Service processes the request and returns the result.
    5. The result is converted back to a DTO and returned as a response.

---

### **3. Infrastructure Layer**

- **Description:**
    
    The **infrastructure layer** implements the abstract repositories and handles database-specific logic.
    
- **Key Components:**
    - **Repositories (Concrete):** Implement repository interfaces defined in the domain layer. These repositories interact with the database using SQLAlchemy.
    - **Tables:** Define ORM models for database tables (e.g., `UserTable`, `ProductTable`).
    - **Unit of Work:** Implements transaction management to ensure consistency in database operations.
- **Key Workflow:**
Repositories and unit-of-work methods accept and return **domain entities**, ensuring domain independence. For example:
    
    ```python
    
    async def save_user(self, transaction, user_entity: User):
        user_table = UserTable(**user_entity.dict())
        transaction.session.add(user_table)
        await transaction.session.flush()
    
    ```
    

---

### **4. Common Layer**

- **Purpose:**Contains shared utilities and components used across layers.
- **Components:**
    - **Logger:** Centralized logging setup.
    - **Utilities:** Helper classes for DTO conversions, JWT handling, request processing, etc.
    - **Shared Models:** Reusable Pydantic models for standardizing error responses or configuration.

---

### **5. Configuration Layer**

- **Purpose:**Manages application-wide settings and configurations.
- **Components:**
    - **Global Error Handling:** Catches exceptions raised in the service layer (e.g., `BadRequestException`) and returns standardized JSON error responses.
    - **JWT Middleware:** Verifies JWT tokens for secure API endpoints.
    - **Swagger Config:** Auto-generates API documentation using FastAPI’s built-in Swagger UI.

---

### **6. Dependency Injection**

- **Purpose:**Dependency injection is managed via the `app_container.py` file, ensuring clean object-oriented programming and reducing coupling between components.

---

### **7. Test Layer**

- **Purpose:**Contains unit and integration tests for controllers, services, and repositories.
- **Key Approach:**
    - Use mock dependencies for unit tests.
    - Follow strict dependency injection to simplify testing of individual components.

---

### **Key Principles**

1. **Domain Independence:** The domain layer is isolated and does not depend on any other layer.
2. **Database Agnosticism:** Abstract repositories and unit-of-work patterns ensure that switching the database requires changes only in the infrastructure layer.
3. **Clear Separation of Concerns:**
    - API layer handles validation and routing.
    - Domain layer implements business logic.
    - Infrastructure layer manages database operations.