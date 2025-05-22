# Project Architecture and API Overview

This document outlines the architectural decisions, design rationale, and API specifications for the Event Management Backend system.

---

## Table of Contents

1. [Auth Router (FastAPI API Endpoints)](#1-auth-router-fastapi-api-endpoints)  
2. [Collaboration Router (Permissions Management for Events)](#2-collaboration-router-permissions-management-for-events)  
3. [Event Router (CRUD and Batch Operations)](#3-event-router-crud-and-batch-operations)  
4. [Event Version Router (Version History, Rollback, Changelog, Diff)](#4-event-version-router-version-history-rollback-changelog-diff)   
5. [UserRepository (DB Layer for User and Token Blacklist)](#5-userrepository-db-layer-for-user-and-token-blacklist)  
6. [EventVersionRepository (Event Versioning Persistence Layer)](#6-eventversionrepository-event-versioning-persistence-layer)  
7. [EventRepository (Main Event Persistence Layer with Versioning)](#7-eventrepository-main-event-persistence-layer-with-versioning)  
8. [CollaborationRepository (DB Layer for Permissions Management)](#8-collaborationrepository-db-layer-for-permissions-management)  
9. [Summary](#9-summary)  

---

## 1. Auth Router (FastAPI API Endpoints)

**Purpose**  
Handles authentication-related HTTP API endpoints: user registration, login, token refresh, and logout.

**Architectural Decisions**  
- **Token-based authentication:** Issues JWT access and refresh tokens for secure stateless auth.  
- **Dependency Injection:** Uses FastAPI's `Depends` for injecting DB session and form data.  
- **Service Layer:** Delegates business logic to `AuthService` to separate concerns.  
- **Explicit error handling:** Uses `HTTPException` with appropriate HTTP status codes for failures.  
- **Security:** Validates authorization header format on logout.

**Endpoints**  
- `POST /api/auth/register` — Registers new users, returns user info + tokens.  
- `POST /api/auth/login` — Authenticates users, returns tokens and user details.  
- `POST /api/auth/refresh` — Refreshes access token using refresh token.  
- `POST /api/auth/logout` — Invalidates access tokens on logout.

---

## 2. Collaboration Router (Permissions Management for Events)

**Purpose**  
Manages sharing and permissions for events, allowing users to share events with roles and update or remove permissions.

**Architectural Decisions**  
- **RESTful design:** Clear resource paths like `/events/{event_id}/permissions`.  
- **Service abstraction:** Delegates business logic to `CollaborationService`.  
- **Try-except wrapping:** Catches exceptions and returns HTTP 500 on internal errors.  
- **Logging:** Internal logging of exceptions for debugging without exposing details to clients.  
- **Response Models:** Uses Pydantic models for validation and documentation.

**Endpoints**  
- `POST /api/events/{event_id}/share` — Share event with a user by role.  
- `GET /api/events/{event_id}/permissions` — List all permissions on an event.  
- `PUT /api/events/{event_id}/permissions/{user_id}` — Update user role.  
- `DELETE /api/events/{event_id}/permissions/{user_id}` — Remove user's permission.

---

## 3. Event Router (CRUD and Batch Operations)

**Purpose**  
Handles creation, retrieval, updating, listing, batch creation, and deletion of events, scoped by authenticated user.

**Architectural Decisions**  
- **RESTful CRUD:** Implements standard POST, GET, PUT, DELETE endpoints with clear resource paths.  
- **Batch Support:** Provides batch creation endpoint to create multiple events efficiently.  
- **Dependency Injection:** Uses FastAPI `Depends` for DB session and current user authentication.  
- **Service Layer:** Delegates business logic to `EventService` for separation of concerns.  
- **Robust Error Handling:** Wraps all operations in try-except blocks, raising appropriate `HTTPException` with 500 status for unexpected errors.  
- **Response Models:** Uses Pydantic schemas (`EventOut`, `EventBase`, `EventUpdate`, `EventCreateBatch`) for validation and OpenAPI documentation.

**Endpoints**  
- `POST /api/events/` — Create a new event. Returns the event along with its versions.  
- `GET /api/events/` — List all events for the authenticated user.  
- `GET /api/events/{event_id}` — Get a single event by ID, scoped to the user.  
- `PUT /api/events/{event_id}` — Update an existing event by ID.  
- `POST /api/events/batch` — Create multiple events in a batch operation.  
- `DELETE /api/events/{event_id}` — Delete an event by ID.

**Error Handling**  
- All endpoints return HTTP 500 with generic failure messages on unexpected errors to avoid leaking sensitive info.  
- `HTTPException` is raised for known error cases (e.g., not found) inside the service layer.

---

## 4. Event Version Router (Version History, Rollback, Changelog, Diff)

**Purpose**  
Manages event versioning features: retrieving specific versions, rolling back to prior versions, viewing changelogs, and computing diffs between versions.

**Architectural Decisions**  
- **Version History Support:** Maintains historical versions with version IDs accessible via dedicated endpoints.  
- **Rollback Functionality:** Allows reverting an event to any previous version, ensuring auditability and data integrity.  
- **Changelog Retrieval:** Provides list of all versions for an event to enable timeline viewing.  
- **Diff Computation:** Computes differences between two versions to help users see what changed.  
- **Dependency Injection:** Uses FastAPI `Depends` for DB session management.  
- **Service Layer:** `EventVersionService` encapsulates all versioning logic, keeping routers clean and focused on HTTP aspects.  
- **Error Handling:**  
  - Raises HTTP 404 for not found versions or invalid diff requests.  
  - Wraps unexpected exceptions in HTTP 500 with descriptive error messages.

**Endpoints**  
- `GET /api/events/{id}/history/{versionId}` — Retrieve a specific event version by version ID.  
- `POST /api/events/{id}/rollback/{versionId}` — Rollback the event to a specific version. Returns the updated event.  
- `GET /api/events/{event_id}/changelog` — Retrieve the changelog (list of all versions) for an event.  
- `GET /api/events/{event_id}/diff/{v1_id}/{v2_id}` — Compute and retrieve differences between two event versions.

**Response Models**  
- `EventVersionOut` — Details of a single event version.  
- `EventOut` — Current event data returned after rollback.  
- `ChangelogOut` — List of versions for changelog display.  
- `DiffOut` — Differences between two versions.

---


## 5. UserRepository (DB Layer for User and Token Blacklist)

**Purpose**  
Handles all database interactions related to users and token blacklisting for authentication.

**Architectural Decisions**  
- **Explicit transaction management:** Uses try-except with rollback to ensure data integrity.  
- **Password hashing:** Abstracted in security utilities for secure password storage.  
- **Token blacklist management:** Stores tokens to invalidate them during logout/revocation.  
- **Return types:** Returns SQLAlchemy models or None when entries are missing.

**Key Methods**  
- `get_user_by_email(email)`  
- `get_user_by_username(username)`  
- `create_user(user)`  
- `add_blacklisted_token(token, expires_at)`  
- `is_token_blacklisted(token)`

---

## 6. EventVersionRepository (Event Versioning Persistence Layer)

**Purpose**  
Manages event version data persistence to enable version history and rollback.

**Architectural Decisions**  
- **Versioning support:** Each event version stored as separate record with version number.  
- **Optional returns:** Use of `Optional` to denote missing data possibility.  
- **Ordered retrieval:** Versions ordered by `version_number` for proper history display.  
- **Error handling:** Wraps DB exceptions and raises HTTP errors.

**Key Methods**  
- `get_by_id(event_id, version_id)`  
- `list_versions(event_id)`  
- `create(event_id, version_number, data)`  
- `get_versions_by_event(event_id)`

---

## 7. EventRepository (Main Event Persistence Layer with Versioning)

**Purpose**  
CRUD operations for events with integrated version history support.

**Architectural Decisions**  
- **Version creation:** New version created on event creation and update.  
- **Use of flush:** Uses `.flush()` instead of `.commit()` to allow flexible transaction control.  
- **JSON serialization:** Uses `pydantic_encoder` for serializing Pydantic models into JSON for versions.  
- **Optional returns:** Methods return event or None based on existence.  
- **Try-except:** Handles exceptions especially in version creation.

**Key Methods**  
- `create(owner_id, data)`  
- `get(event_id)`  
- `list_by_user(user_id)`  
- `update(event_id, data)`  
- `create_batch(events_data, owner_id)`  
- `delete(event_id)`  
- `create_event_version(event_id, version_number, data, created_by)`

---

## 8. CollaborationRepository (DB Layer for Permissions Management)

**Purpose**  
Manages event permission entities and user roles in the database.

**Architectural Decisions**  
- **Clear separation:** Permissions isolated in own repository for clarity.  
- **Try-except with rollback:** Maintains data integrity on failure.  
- **Use of Optional:** Reflects possible missing permission entries.  
- **Flush instead of commit:** Enables flexible transaction management.

**Key Methods**  
- `get_by_event_and_user(event_id, user_id)`  
- `create_role(event_id, user_id, role)`  
- `list_by_event(event_id)`  
- `update_role(event_id, user_id, role)`  
- `delete_permission(event_id, user_id)`

---

## 9. Summary

- **Layered Architecture:** Controllers (Routers) → Services → Repositories → Database Models.  
- **Robust Error Handling:** All DB mutations protected with rollback and clear HTTP errors.  
- **Transaction Control:** Use of `.flush()` allows transactional flexibility across layers.  
- **Security:** Password hashing and token blacklisting implemented securely in user repository.  
- **Versioning:** Event repository tightly integrated with version history for audit and rollback.  
- **Clean API Design:** RESTful, predictable endpoints following best practices.  
- **Type Safety:** Extensive use of Pydantic models and type hints ensures correctness.

---
