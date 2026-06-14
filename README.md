# 🤖 Smart AI Chatbot — Chikku

A full-stack AI-powered chatbot application built with FastAPI, Streamlit, and PostgreSQL. Meet **Chikku** — your smart, friendly AI assistant powered by **LLaMA 3.1** via Groq.

---

## 🌐 Live Demo

> **Frontend:** https://smart-chatbot-frontend-sp03.onrender.com

---

## 🏗️ Architecture

```
Render.com                  AWS EC2 (t3.micro)
┌─────────────────┐         ┌─────────────────────┐
│  frontend.py    │ ──────▶ │  backend.py          │
│  (Streamlit)    │  HTTP   │  (FastAPI)           │
└─────────────────┘         └─────────┬───────────┘
                                      │
                             ┌─────────▼───────────┐
                             │  AWS RDS             │
                             │  (PostgreSQL)        │
                             └─────────────────────┘
```
---

## ✨ Features

- 💬 Real-time AI chat powered by LLaMA 3.1 via Groq
- 🔐 User authentication (Register / Login) with JWT tokens
- 👤 Guest mode — chat without creating an account
- 💾 Persistent chat history stored in PostgreSQL
- 🔒 Secure password hashing with bcrypt
- 🎨 Custom CSS styling for a clean UI

---

## 🛠️ Tech Stack

| Layer    | Technology                               |
|---|---   |
| Frontend | Streamlit                                |
| Backend  | FastAPI                                  |
| Database | PostgreSQL (AWS RDS)                     |
| LLM      | LLaMA 3.1 Instant (via Groq)             |
| Auth     | JWT (python-jose)                        |
| Hosting  | Render.com (Frontend), AWS EC2 (Backend) |

---

## 📁 Project Structure

```
Smart_Chatbot/
├── frontend.py          
├── backend.py           
├── style.css            
├── requirements.txt     
├── requirements-frontend.txt
└── .gitignore
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description                     |
|---|---|---|
| POST | `/login`         | Login existing user       |
| POST | `/register`      | Register new user         |
| POST | `/guest`         | Create guest session      |
| POST | `/Chatbot`       | Chat (authenticated user) |
| POST | `/guest-chatbot` | Chat (guest user)         |

---

## ⚙️ Environment Variables

### Backend `.env`
```env
DB_HOST      =   "Hosted on AWS RDS"
DB_PORT      =   "PORT NUMBER"
DB_NAME      =   "Chatbot-DB"
DB_USER      =   "postgres"
DB_PASSWORD  =   "Not Public"
GROK API KEY =   "Not Public"
SECRET_KEY   =   "Not Public"
ALGORITHM    =   "HS256"
```

### Frontend `.env`
```env
BACKEND_URL = "Not Disclose"
```
