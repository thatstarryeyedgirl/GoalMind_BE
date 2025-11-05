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
- Store goals and steps in a PostgreSQL or SQLite database  
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
| `GET` | `/api/agent/` | Returns Telex workflow JSON (agent info) |
| `POST` | `/api/goal/` | Creates a goal with steps for a user |


## Postman Documentation

- **Postman Link:** ``