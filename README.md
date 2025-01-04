# Little Lemon API 🍋

Welcome to the Little Lemon API project! This Django-based API provides a robust backend system for managing restaurant operations, including menu items, orders, user roles, and more. The API is designed to support the development of web and mobile applications for the Little Lemon restaurant.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Usage](#usage)
4. [API Endpoints](#api-endpoints)
5. [Authentication & Authorization](#authentication--authorization)
6. [Throttling](#throttling)


---

## Project Overview

The Little Lemon API provides endpoints to:
- Manage menu items
- Handle user roles (Manager, Delivery Crew, Customers)
- Process customer orders
- Assign delivery crew to orders
- Filter, sort, and paginate results

It adheres to RESTful principles and is built using **Django** and **Django REST Framework (DRF)**.

---

## Features
- **User Authentication:** Token-based authentication using Djoser.
- **Role Management:** Distinct access for Managers, Delivery Crew, and Customers.
- **Error Handling:** Appropriate HTTP status codes and error messages for all operations.
- **Filtering, Sorting, and Pagination:** Enhanced search capabilities for menu items and orders.
- **Throttling:** Rate limits for authenticated and unauthenticated users.



## Usage

Use an API client like **Postman** or **cURL** to interact with the API. Alternatively, integrate it with a frontend application.

---

## API Endpoints

### User Authentication
- `POST /api/users`: Create a new user.
- `POST /token/login`: Generate an access token.
- `GET /api/users/me`: View current user details.

### Menu Management
- **Customers & Delivery Crew:**
  - `GET /api/menu-items`: View all menu items.
  - `GET /api/menu-items/{menuItem}`: View details of a specific menu item.
- **Managers:**
  - `POST /api/menu-items`: Add a menu item.
  - `PUT /api/menu-items/{menuItem}`, `PATCH /api/menu-items/{menuItem}`: Update a menu item.
  - `DELETE /api/menu-items/{menuItem}`: Delete a menu item.

### Order Management
- **Customers:**
  - `GET /api/orders`: View customer’s orders.
  - `POST /api/orders`: Place an order.
- **Managers:**
  - `GET /api/orders`: View all orders.
  - `DELETE /api/orders/{orderId}`: Delete an order.
- **Delivery Crew:**
  - `GET /api/orders`: View assigned orders.
  - `PATCH /api/orders/{orderId}`: Update order delivery status.

---

## Authentication & Authorization

This project uses **Djoser** for authentication. Only authorized users can access certain endpoints:
- **Manager Role:** Full control over menu items and order assignments.
- **Delivery Crew Role:** Access and update assigned orders.
- **Customer Role:** Access menu items and place orders.

---

## Throttling

The API applies rate limits to prevent abuse:


---


## Contact

For any queries, please contact: **mahdertesfaye11@gmail.com**
