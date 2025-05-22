from pathlib import Path

# Define the shell script content
curl_script = """
#!/bin/bash

# AUTH ROUTES

# Register
curl -X POST http://localhost:8000/api/auth/register \\
-H "Content-Type: application/json" \\
-d '{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword"
}'

# Login
curl -X POST http://localhost:8000/api/auth/login \\
-H "Content-Type: application/x-www-form-urlencoded" \\
-d "username=john@example.com&password=securepassword"

# Refresh token
curl -X POST http://localhost:8000/api/auth/refresh \\
-H "Authorization: Bearer <refresh_token>"

# Logout
curl -X POST http://localhost:8000/api/auth/logout \\
-H "Authorization: Bearer <access_token>"

# COLLABORATION ROUTES

# Share event
curl -X POST http://localhost:8000/api/events/<event_id>/share \\
-H "Authorization: Bearer <access_token>" \\
-H "Content-Type: application/json" \\
-d '{
  "user_id": "user_uuid_here",
  "role": "editor"
}'

# List permissions
curl -X GET http://localhost:8000/api/events/<event_id>/permissions \\
-H "Authorization: Bearer <access_token>"

# Update permission
curl -X PUT http://localhost:8000/api/events/<event_id>/permissions/<user_id> \\
-H "Authorization: Bearer <access_token>" \\
-H "Content-Type: application/json" \\
-d '{"role": "viewer"}'

# Delete permission
curl -X DELETE http://localhost:8000/api/events/<event_id>/permissions/<user_id> \\
-H "Authorization: Bearer <access_token>"

# EVENT ROUTES

# Create event
curl -X POST http://localhost:8000/api/events/ \\
-H "Authorization: Bearer <access_token>" \\
-H "Content-Type: application/json" \\
-d '{
  "title": "Team Meeting",
  "description": "Sprint planning",
  "start_time": "2025-05-25T10:00:00",
  "end_time": "2025-05-25T11:00:00"
}'

# List events
curl -X GET http://localhost:8000/api/events/ \\
-H "Authorization: Bearer <access_token>"

# Get single event
curl -X GET http://localhost:8000/api/events/<event_id> \\
-H "Authorization: Bearer <access_token>"

# Update event
curl -X PUT http://localhost:8000/api/events/<event_id> \\
-H "Authorization: Bearer <access_token>" \\
-H "Content-Type: application/json" \\
-d '{
  "title": "Updated Team Meeting",
  "description": "Sprint retrospective"
}'

# Batch create events
curl -X POST http://localhost:8000/api/events/batch \\
-H "Authorization: Bearer <access_token>" \\
-H "Content-Type: application/json" \\
-d '[
  {
    "title": "Event 1",
    "description": "Details",
    "start_time": "2025-05-26T10:00:00",
    "end_time": "2025-05-26T11:00:00"
  },
  {
    "title": "Event 2",
    "description": "More details",
    "start_time": "2025-05-27T14:00:00",
    "end_time": "2025-05-27T15:00:00"
  }
]'

# Delete event
curl -X DELETE http://localhost:8000/api/events/<event_id> \\
-H "Authorization: Bearer <access_token>"

# EVENT VERSION ROUTES

# Get specific version
curl -X GET http://localhost:8000/api/events/<event_id>/history/<version_id> \\
-H "Authorization: Bearer <access_token>"

# Rollback to version
curl -X POST http://localhost:8000/api/events/<event_id>/rollback/<version_id> \\
-H "Authorization: Bearer <access_token>"

# Get changelog
curl -X GET http://localhost:8000/api/events/<event_id>/changelog \\
-H "Authorization: Bearer <access_token>"

# Get diff between versions
curl -X GET http://localhost:8000/api/events/<event_id>/diff/<v1_id>/<v2_id> \\
-H "Authorization: Bearer <access_token>"
"""


