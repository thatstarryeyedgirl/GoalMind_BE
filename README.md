# GoalMind_BE

## Telex Goal Agent API

This is a simple Django REST API that connects to **Telex.im** as an intelligent goal assistant.  
The Goal Agent helps users break down their goals into small, achievable steps automatically.

## Project Overview

The **Telex Goal Agent** is built to work as a workflow for Telex.  
When a user sends a message like *“I want to learn Python”*,  
the agent will automatically:
1. Create a goal in the database
2. Generate 5 random steps to help the user achieve it
3. Return the goal and steps as a response

## Features

- Create goals with user IDs and messages  
- Auto-generate 5 random, personalized steps for each goal  
- Store goals and steps in a PostgreSQL database
- Return Telex-compatible workflow JSON for agent integration  
- Beginner-friendly Django REST setup using class-based views  

## Tech Stack

- **Backend:** `Django` + `Django REST Framework`
- **Database:** PostgreSQL
- **Language:** Python 3.12.10
- **API Type:** RESTful API  
- **Environment Management:** `.env`

## Endpoints
| Method | Endpoint | Description |
|--------|-----------|-------------|
| `GET` | `/a2a/agent/` | Returns Telex workflow JSON (agent info) |
| `POST` | `/a2a/goal/` | Creates a goal with steps for a user |


## Postman Documentation
The Telex Goal Agent API endpoints are fully documented in Postman to make testing and integration simple. The collection includes all routes for agent configuration and goal creation, along with sample requests and responses.

Each request is preconfigured with the correct HTTP method, headers, and example JSON data — allowing you to quickly test how each endpoint works. You can easily trigger the agent setup, send goal messages, and view the generated goal steps directly within Postman.
- **Postman Link:** `https://documenter.getpostman.com/view/48778720/2sB3Wqvg96`

