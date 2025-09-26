# 📄 Stage 3 – Technical Documentation: (Unibot)

---

## 📝 Task 0: Define User Stories and Mockups

### User Stories (MoSCoW)

**Must Have**
- As a **student**, I want to **search for FAQs by keyword**, so that **I can quickly find answers**.  
- As a **student**, I want to **know deadlines of activities/services**, so that **I don’t miss important dates**.  
- As a **student**, I want to **get information about campus facilities (library, cafeteria, gym)**, so that **I can plan my visits**.  
- As an **admin**, I want to **add or update FAQs**, so that **the chatbot always has accurate information**.  

**Should Have**
- As a **student**, I want to **ask the chatbot general questions about university events and announcements**, so that **I stay informed and engaged**.  
- As a **student**, I want to **access the chatbot from web**, so that **I can use it wherever I am**.  

**Could Have**
- As a **student**, I want to **rate chatbot answers**, so that **future responses can improve**.  
- As a **student**, I want to **save frequently asked questions**, so that **I can access them quickly later**.  

**Won’t Have (MVP)**
- As a **student**, I want to **interact with the chatbot using voice commands**, so that **I can have a hands-free experience**.  
- As a **student**, I want the chatbot to **access my grades and personal academic data**, so that **I can get personalized academic insights**.  
- As a **student**, I want the chatbot to **speak in multiple languages**, so that **I can interact in my preferred language**.  

### Mockups

- **Chatbot Interface:**  
  <img width="1600" height="1000" alt="image" src="https://github.com/user-attachments/assets/c0584a73-f01b-44b6-9266-f2f4011ee4dd" />

- **Admin Dashboard:**  
  <img width="1600" height="1126" alt="image" src="https://github.com/user-attachments/assets/e8e39f0e-4483-4685-8356-a15cf4ceeaaf" />

---

## 📝 Task 1: System Architecture

**High-Level Components**
- **Frontend:** React web interface.  
- **Backend:** Python + Django Framework (DRF).  
- **Database:** MongoDB.  
- **Search Engine (if applicable):** Rasa / Vector Store.  
- **External API (if applicable):** Optional (University Calendar in future, OpenAI).  

**Data Flow:** Student → Frontend → Backend (API) → DB/Search → Response → Student  

```mermaid
flowchart LR
    student["Student (Web)"] --> fe["Frontend - React"]
    fe -->|REST| be["Backend - Django (DRF)"]
    be -->|CRUD & Queries| db[("MongoDB")]
    be -->|Search/Rank| vs["Rasa / Vector Store - optional"]
    be -->|Events/AI optional| ext["External APIs - Calendar, OpenAI"]
    be --> fe
    fe --> student

```

---

## 📝 Task 2: Components, Classes, and Database Design

### 2.1 Back-End Components / Services

**AuthService**
- `login(email, password) → token`
- `generate_token(user)`
- `verify_token(token)`

**FaqService**
- `list_faqs(query, category_id)`
- `get_faq(id)`
- `create_faq(data, user)`
- `update_faq(id, data, user)`
- `delete_faq(id)`

**EventService**
- `list_events(from, to)`
- `create_event(data)`
- `update_event(id, data)`
- `delete_event(id)`

**SearchService**
- `search(query, top_k)`
- `index_faq(faq)` (used if vector store/Rasa added later)

**FeedbackService**
- `submit_feedback(faq_id, helpful, comment, user)`
- `list_feedback(faq_id)`

**FavoriteService (optional)**
- `toggle_favorite(user_id, faq_id)`
- `list_favorites(user_id)`

---

### 2.2 Database Design (Document-Oriented – MongoDB)

**Collection: users**
```json
{
  "_id": "UUID",
  "name": "string",
  "email": "string (unique)",
  "password_hash": "string",
  "role": "admin|student",
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

**Collection: categories**
```json
{
  "_id": "UUID",
  "name": "string"
}
```

**Collection: faqs**
```json
{
  "_id": "UUID",
  "question": "text",
  "answer": "text",
  "category_id": "UUID -> categories._id",
  "updated_by": "UUID -> users._id",
  "updated_at": "ISODate",
  "created_at": "ISODate"
}
```

**Collection: events**
```json
{
  "_id": "UUID",
  "title": "string",
  "start_date": "ISODate",
  "end_date": "ISODate",
  "location": "string",
  "description": "string",
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

**Collection: feedback**
```json
{
  "_id": "UUID",
  "faq_id": "UUID -> faqs._id",
  "user_id": "UUID -> users._id",
  "helpful": true,
  "comment": "string",
  "created_at": "ISODate"
}
```

**Collection: favorites**
```json
{
  "_id": "UUID",
  "user_id": "UUID -> users._id",
  "faq_id": "UUID -> faqs._id",
  "created_at": "ISODate"
}
```

---

## 📝 Task 3: Sequence Diagrams

### Student asks FAQ
```mermaid
sequenceDiagram
  autonumber
  participant Student
  participant Frontend as Frontend (React Web)
  participant Backend as Backend API (Django + DRF)
  participant DB as MongoDB

  Student->>Frontend: Type question
  Frontend->>Backend: GET /api/faqs?query=...
  Backend->>DB: find({ $text: { $search: "<query>" } })
  DB-->>Backend: Matching FAQ documents
  Backend-->>Frontend: 200 OK (JSON answers)
  Frontend-->>Student: Render answer in chat
```

### Admin updates FAQ
```mermaid
sequenceDiagram
  autonumber
  participant Admin
  participant Frontend as Frontend (React Admin UI)
  participant Backend as Backend API (Django + DRF)
  participant DB as MongoDB

  Admin->>Frontend: Edit FAQ
  Frontend->>Backend: PUT /api/faqs/:id (JWT)
  Backend->>DB: updateOne({ _id:id }, { $set:{ question, answer, updated_by, updated_at } })
  DB-->>Backend: { acknowledged:true, modifiedCount:1 }
  Backend-->>Frontend: 200 OK (updated record)
  Frontend-->>Admin: Show success + refresh
```

### Student views events
```mermaid
sequenceDiagram
  autonumber
  participant Student
  participant Frontend as Frontend (React Web)
  participant Backend as Backend API (Django + DRF)
  participant DB as MongoDB

  Student->>Frontend: Click "Deadlines"
  Frontend->>Backend: GET /api/events?from=&to=
  Backend->>DB: find({ date_range })
  DB-->>Backend: Matching events
  Backend-->>Frontend: 200 OK (JSON events)
  Frontend-->>Student: Show deadlines list
```

---

## 📝 Task 4: API Specifications

**Internal APIs**
| Endpoint | Method | Input | Output | Role |
|----------|--------|-------|--------|------|
| /api/auth/login | POST | {email, password} | {token, role} | Admin |
| /api/faqs | GET | ?query=keyword&category=id | [{id, question, answer}] | Student |
| /api/faqs | POST | {question, answer, category_id} | {id, question, answer} | Admin |
| /api/faqs/:id | PUT | {question?, answer?} | {id, question, answer} | Admin |
| /api/events | GET | {from?, to?} | [{id, title, start_date,...}] | Student |
| /api/feedback | POST | {faq_id, helpful, comment?} | {id, faq_id, helpful, comment} | Student |

**External APIs (Future)**
- University Calendar API  
- University Announcements API  
- OpenAI API  

---

## 📝 Task 5: SCM and QA Strategies

**Source Control (SCM)**
- Repository: GitHub  
- Branching Strategy:  
  - `main` → production-ready  
  - `dev` → integration branch  
  - `feature/*` → per feature  
- Process: Pull Requests → Code Review → Merge  

**Quality Assurance (QA)**
- Backend: pytest (unit + integration tests)  
- Frontend: React Testing Library  
- API Testing: Postman  
- Linting: black + flake8 (Python), ESLint (JS)  
- CI/CD: GitHub Actions to run tests/lint checks for each PR  

---

# 📌 Final Deliverable: Stage 3 – Technical Documentation (Unibot)

This document consolidates all the outputs of Stage 3 for the **Unibot** project, including:

- **Task 0:** User Stories and Mockups  
- **Task 1:** System Architecture  
- **Task 2:** Components, Classes, and Database Design  
- **Task 3:** Sequence Diagrams  
- **Task 4:** API Specifications  
- **Task 5:** SCM and QA Strategies
