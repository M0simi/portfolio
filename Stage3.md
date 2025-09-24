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
- As a **student**, I want to **ask the chatbot general questions about university events and announcemtns**, so that **I stay informed and engaged**.
- As a **student**, I want to **access the chatbot from web**, so that **I can use it wherever I am**

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
- **Backend:** Python + Django Framework.  
- **Database:** MongoDB.  
- **Search Engine (if applicable):** Rasa.  
- **External API (if applicable):** Optional (University Calendar in future, OpenAI).

**Data Flow**
Student → Frontend → Backend (API) → Database/Search → Response → Student  

```mermaid
flowchart LR
    student[Student Web] --> frontend[Frontend - React]
    frontend -->|REST calls| backend[Backend - Python - Django]
    backend -->|CRUD/Queries| db[(MongoDB)]
    backend -->|Search / Rank| vector[(Vector Store - optional)]
    backend -->|Optional Events| external[External API - University Calendar, OpenAI]
    backend --> frontend
    frontend --> student
```

---

## 📝 Task 2: Components, Classes, and Database Design

### 2.1 Back-End Components / Services

AuthService

login(email, password) → token

generate_token(user)

verify_token(token)

FaqService

list_faqs(query, category_id)

get_faq(id)

create_faq(data, user)

update_faq(id, data, user)

delete_faq(id)

EventService

list_events(from, to)

create_event(data)

update_event(id, data)

delete_event(id)

SearchService

search(query, top_k)

index_faq(faq) (تُستخدم إذا اعتمدنا vector store/Rasa لاحقًا)

FeedbackService

submit_feedback(faq_id, helpful, comment, user)

list_feedback(faq_id)

FavoriteService (Optional for “save FAQs”)

toggle_favorite(user_id, faq_id)

list_favorites(user_id)


2.2 Database Design (Document-Oriented – MongoDB)

Collection: users
```
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

Mandatory: email, password_hash, role

Optional: name

Collection: categories
```
{
  "_id": "UUID",
  "name": "string"
}
```

Mandatory: name

Collection: faqs
```
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

Mandatory: question, answer, category_id

Optional: updated_by

Collection: events
```
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

Mandatory: title, start_date

Optional: end_date, location, description

Collection: feedback
```
{
  "_id": "UUID",
  "faq_id": "UUID -> faqs._id",
  "user_id": "UUID -> users._id",
  "helpful": true,
  "comment": "string",
  "created_at": "ISODate"
}
```

Mandatory: faq_id, user_id, helpful

Optional: comment

Collection: favorites
```
{
  "_id": "UUID",
  "user_id": "UUID -> users._id",
  "faq_id": "UUID -> faqs._id",
  "created_at": "ISODate"
}
```

Mandatory: user_id, faq_id

Constraint: unique pair (user_id, faq_id)

---

## 📝 Task 3: Sequence Diagrams

```mermaid
sequenceDiagram
    autonumber
    participant Student
    participant Admin
    participant Frontend as Frontend (Web/Admin UI)
    participant Backend as Backend API (Flask)
    participant DB as PostgreSQL

    %% --- Use Case 1: Student asks FAQ ---
    Student->>Frontend: Type question
    Frontend->>Backend: GET /api/faqs?query=...
    Backend->>DB: Search FAQs (text/embeddings)
    DB-->>Backend: Matching rows
    Backend-->>Frontend: 200 OK (JSON answer)
    Frontend-->>Student: Render answer in chat

    %% --- Divider ---
    Note over Student,DB: --- Admin updates FAQ ---

    %% --- Use Case 2: Admin updates FAQ ---
    Admin->>Frontend: Edit FAQ (question/answer)
    Frontend->>Backend: PUT /api/faqs/:id (JWT)
    Backend->>DB: UPDATE faqs SET ...
    DB-->>Backend: Update OK
    Backend-->>Frontend: 200 OK (updated record)
    Frontend-->>Admin: Show success + refreshed table

    %% --- Divider ---
    Note over Student,DB: --- Student views events ---

    %% --- Use Case 3: Student views events ---
    Student->>Frontend: Click "Deadlines" quick reply
    Frontend->>Backend: GET /api/events?from=&to=
    Backend->>DB: SELECT events WHERE date range
    DB-->>Backend: Matching events
    Backend-->>Frontend: 200 OK (JSON events)
    Frontend-->>Student: Show list of deadlines
```

```mermaid
%%{init: {'theme': 'dark', 'sequence': {'showSequenceNumbers': true}}}%%
sequenceDiagram
  autonumber
  participant Student
  participant Admin
  participant Frontend as Frontend (React Web/Admin UI)
  participant Backend as Backend API (Django + DRF)
  participant DB as MongoDB

  %% ===================== Use Case 1: Student asks FAQ =====================
  rect rgba(180,180,180,0.15)
    Note over Student,DB: --- Student asks FAQ ---
    Student->>Frontend: Type question
    Frontend->>Backend: GET /api/faqs?query=...
    Backend->>DB: find({ $text: { $search: "<query>" } })
    DB-->>Backend: matching FAQ documents
    Backend-->>Frontend: 200 OK (JSON answers)
    Frontend-->>Student: Render answer in chat
  end

  %% ===================== Use Case 2: Admin updates FAQ =====================
  rect rgba(180,180,180,0.15)
    Note over Student,DB: --- Admin updates FAQ ---
    Admin->>Frontend: Edit FAQ (question/answer)
    Frontend->>Backend: PUT /api/faqs/:id (Authorization: Bearer JWT)
    Backend->>DB: updateOne({ _id: id }, { $set: { question, answer, updated_by, updated_at } })
    DB-->>Backend: { acknowledged: true, modifiedCount: 1 }
    Backend-->>Frontend: 200 OK { updated record }
    Frontend-->>Admin: Show success + refreshed table
  end

  %% ===================== Use Case 3: Student views events ==================
  rect rgba(180,180,180,0.15)
    Note over Student,DB: --- Student views events ---
    Student->>Frontend: Click "deadlines" quick reply
    Frontend->>Backend: GET /api/events?from=&to=
    Backend->>DB: find({ start_date: { $gte: from, $lte: to } })
    DB-->>Backend: matching event documents
    Backend-->>Frontend: 200 OK (JSON events)
    Frontend-->>Student: Show list of deadlines
  end
```

---

## 📝 Task 4: API Specifications

### Internal APIs

| Endpoint          | Method | Input                          | Output                          | Role   |
|-------------------|--------|--------------------------------|---------------------------------|--------|
| `/api/auth/login` | POST   | {email, password}             | {token, role}                   | Admin  |
| `/api/faqs`       | GET    | ?query=keyword&category=id    | [{id, question, answer}]        | Student|
| `/api/faqs`       | POST   | {question, answer, category_id}| {id, question, answer}          | Admin  |
| `/api/faqs/:id`   | PUT    | {question?, answer?}          | {id, question, answer}          | Admin  |
| `/api/events`     | GET    | {from?, to?}                  | [{id, title, start_date,...}]   | Student|
| `/api/feedback`   | POST   | {faq_id, helpful, comment?}   | {id, faq_id, helpful, comment}  | Student|

### External APIs (Future)
- University Calendar API.  
- University Announcements API.
- OpenAI API  

---

## 📝 Task 5: SCM and QA Strategies

### Source Control (SCM)
- **Repository:** GitHub.  
- **Branching Strategy:**  
  - `main` → production-ready.  
  - `dev` → integration branch.  
  - `feature/*` → per feature.  
- **Process:** Pull Requests → Code Review → Merge.  

### Quality Assurance (QA)
- **Backend:** pytest (unit + integration tests).  
- **Frontend:** React Testing Library.  
- **API Testing:** Postman.  
- **Linting:** black + flake8 (Python), ESLint (JS).  
- **CI/CD:** GitHub Actions to run tests/lint checks for each PR.  

---

# 📌 Final Deliverable: Stage 3 – Technical Documentation (Unibot)

This document consolidates all the outputs of Stage 3 for the **Unibot** project, including:

- **Task 0:** User Stories and Mockups  
- **Task 1:** System Architecture  
- **Task 2:** Components, Classes, and Database Design  
- **Task 3:** Sequence Diagrams  
- **Task 4:** API Specifications  
- **Task 5:** SCM and QA Strategies
  
