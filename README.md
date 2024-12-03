# Project Architecture

The application is designed to be modular, maintainable, and database-agnostic. It primarily uses **FastAPI**, **Pydantic**, and **SQLAlchemy** and manages dependencies using **Poetry**.

## **Folder Structure**

Below is the high-level folder structure:

```
📦
├─ app
│  ├─ api
│  │  ├─ dto
│  │  │  └─ example_dto.py
│  │  ├─ v1
│  │  │  ├─ controller
│  │  │  │  └─ example_controller.py
│  │  │  └─ v1_router.py
│  ├─ common
│  │  ├─ error
│  │  │  └─ response_exception.py
│  │  └─ app_logger.py
│  ├─ configuration
│  │  ├─ global_exception_handler.py
│  │  └─ swagger_config.py
│  ├─ domain
│  │  ├─ entity
│  │  │  └─ example_entity.py
│  │  ├─ repository
│  │  │  └─ example_repo.py
│  │  ├─ service
│  │  │  └─ example_service.py
│  │  └─ unit_of_work
│  │     ├─ transaction.py
│  │     └─ transaction_manager.py
│  ├─ infrastructure
│  │  ├─ repository
│  │  │  └─ example_repo.py
│  │  ├─ table
│  │  │  └─ example_table.py
│  │  └─ unit_of_work
│  │     └─ transaction.py
│  └─ main.py
│  └─ app_container.py
├─ migration
│  ├─ versions
│  │  └─ initial_migration.py
│  ├─ README
│  ├─ env.py
│  └─ script.py.mako
├─ test
│  ├─ domain
│  │  ├─ service
│  │  │  └─ test_example_service.py
├─ .vscode
│  └─ settings.json
├─ .gitignore
├─ README.md
├─ alembic.ini
├─ docker-compose.yml
├─ mypy.ini
├─ pyproject.toml

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