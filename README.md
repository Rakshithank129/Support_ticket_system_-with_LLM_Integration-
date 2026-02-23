Support Ticket System
A support ticket management system with AI-powered auto-classification. Built with Django, React, PostgreSQL, and Docker.

Start everything:
docker-compose up --build  #it will start the entire application stack

services with URL:
Frontend         http://localhost:3000
Backend API      http://localhost:8000/api/

API Endpoints:

Method        Endpoint                 Description
POST          /api/tickets/            Create a new ticket
GET           /api/tickets/            List all tickets
PATCH         /api/tickets/<id>/       Update a ticket (change status)
GET           /api/tickets/stats/      Get aggregated statistics
POST          /api/tickets/classify/   Get AI-suggested category + priority

Filtering & Search:

GET /api/tickets/?search=login issue
GET /api/tickets/?category=technical&priority=high
GET /api/tickets/?status=open

Example for Creating a Ticket:
POST : /api/tickets/
json{
  "title": "",
  "description": "",
  "category": "",
  "priority": ""
}


Valid values need to be used:

category: billing | technical | account | general
priority: low | medium | high | critical
status: open | in_progress | resolved | closed (defaults to open)

💡How AI Classification Works
Before submitting a ticket, call the classify endpoint with just the description:

POST /api/tickets/classify/

{
  "description": "I keep getting an error when trying to login since yesterday."
}

Response:
{
  "suggested_category": "account",
  "suggested_priority": "high"
}

The frontend calls this automatically when the user finishes typing the description. The suggested values pre-fill the dropdowns and the user can accept or override them before submitting.

If the LLM is unavailable, both values return as null and the form still works normally.

LLM Choice
Model used: OpenAI
Chosen for its low latency (important for real-time suggestions), cost efficiency, and reliable structured JSON output at temperature=0.