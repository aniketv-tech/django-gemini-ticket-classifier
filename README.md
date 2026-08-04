# AI-Powered Customer Support Ticket Classifier 🚀

An intelligent, automated support ticket classification and resolution engine built with **Django REST Framework** and **Google Gemini API**. It ingests incoming customer inquiries, automatically analyzes their intent, categorizes them, sets priority levels, and generates personalized auto-replies in real time.

---

## ✨ Features

* **Automated Ticket Triage:** Instantly classifies tickets into categories (*Billing*, *Technical Support*, *Feature Request*, *General Inquiry*).
* **Smart Priority Assignment:** Assigns priority tags (*High*, *Medium*, *Low*) based on ticket urgency.
* **Context-Aware Auto-Replies:** Drafts personalized responses tailored specifically to customer details using **Gemini 2.5 Flash**.
* **Fault-Tolerant Fallback:** Includes a built-in offline keyword-matching engine that takes over if API keys are missing, network connectivity drops, or rate limits are reached—guaranteeing 100% server uptime (`HTTP 201 Created`).
* **REST API Interface:** Clean API endpoint provided by Django REST Framework (DRF).

---

## 🛠️ Tech Stack

* **Language:** Python
* **Web Framework:** Django, Django REST Framework (DRF)
* **Database:** SQLite
* **AI Model:** Google Gemini 2.5 Flash (`gemini-2.5-flash`)
* **SDK / Tools:** `google-genai`, `python-dotenv`, Git, GitHub

---

## 🏗️ System Architecture


[ User / Client ]
       │
       ▼ (POST /api/tickets/)
[ Django REST Framework ]
       │
       ▼
[ AI Agent Engine (agent.py) ]
       ├── Calls Gemini 2.5 Flash API (Structured JSON Output)
       └── 🛡️ Fallback Engine (Triggered on API failure/offline)
       │
       ▼
[ SQLite Database & HTTP 201 Response ]

---

