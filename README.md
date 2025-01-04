# Little Lemon API 🍋


## Project Description

This project involves creating a fully functional API for the Little Lemon restaurant. The API will allow client application developers to build web and mobile applications that can interact with the restaurant's data. The API will support various user roles, including customers, managers, and delivery crew, each with different levels of access and permissions.

### Key Features

- **User Registration and Token Generation**: Users can register, log in, and obtain access tokens for authenticated API requests.
- **Menu Management**: Managers can add, update, and delete menu items. Customers and delivery crew can view menu items.
- **User Group Management**: Managers can assign users to the manager or delivery crew groups.
- **Cart Management**: Customers can add items to their cart, view their cart, and delete items from their cart.
- **Order Management**: Customers can place orders, view their orders, and managers can update order status and assign delivery crew.
- **Filtering, Pagination, and Sorting**: The API supports filtering, pagination, and sorting for menu items and orders.
- **Throttling**: The API implements throttling to limit the number of requests from authenticated and unauthenticated users.

## API Endpoints

### User Registration and Token Generation

- **POST /api/users**: Creates a new user.
- **GET /api/users/users/me/**: Displays the current user.
- **POST /token/login/**: Generates access tokens.

### Menu Items

- **GET /api/menu-items**: Lists all menu items (accessible by customers and delivery crew).
- **POST /api/menu-items**: Creates a new menu item (accessible by managers).
- **GET /api/menu-items/{menuItem}**: Lists a single menu item.
- **PUT, PATCH /api/menu-items/{menuItem}**: Updates a single menu item (accessible by managers).
- **DELETE /api/menu-items/{menuItem}**: Deletes a menu item (accessible by managers).

### User Group Management

- **GET /api/groups/manager/users**: Returns all managers.
- **POST /api/groups/manager/users**: Assigns a user to the manager group.
- **DELETE /api/groups/manager/users/{userId}**: Removes a user from the manager group.
- **GET /api/groups/delivery-crew/users**: Returns all delivery crew.
- **POST /api/groups/delivery-crew/users**: Assigns a user to the delivery crew group.
- **DELETE /api/groups/delivery-crew/users/{userId}**: Removes a user from the delivery crew group.

### Cart Management

- **GET /api/cart/menu-items**: Returns current items in the cart for the current user.
- **POST /api/cart/menu-items**: Adds a menu item to the cart.
- **DELETE /api/cart/menu-items**: Deletes all menu items in the cart for the current user.

### Order Management

- **GET /api/orders**: Returns all orders for the current user (customers) or all orders (managers).
- **POST /api/orders**: Creates a new order for the current user.
- **GET /api/orders/{orderId}**: Returns all items for a specific order.
- **PUT, PATCH /api/orders/{orderId}**: Updates an order (accessible by managers and delivery crew).
- **DELETE /api/orders/{orderId}**: Deletes an order (accessible by managers).



## Contact

For any queries, please contact: **mahdertesfaye11@gmail.com**
