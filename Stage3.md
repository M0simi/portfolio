# 📄 Stage 3 – Technical Documentation: (Unibot)

---

## 📝 Task 0: Define User Stories and Mockups

### User Stories (MoSCoW)

**Must Have**
- As a **student**, I want to **search FAQs by keyword** to **find answers quickly**.  
- As a **student**, I want **deadlines of activities/services** so I **don’t miss dates**.  
- As a **student**, I want **info about facilities (library/cafeteria/gym)** to **plan visits**.  
- As an **admin**, I want to **add/update FAQs** so **content stays accurate**.

**Should Have**
- As a **student**, I want to **ask about events/announcements** to **stay informed**.  
- As a **student**, I want to **use the chatbot on the web** to **access it anywhere**.

**Could Have**
- As a **student**, I want to **rate answers** to **improve responses**.  
- As a **student**, I want to **save favorite FAQs** to **open them quickly later**.

**Won’t Have (MVP)**
- Voice commands.  
- Access to personal academic data (grades).  
- Multi-language support.

### Mockups
- **Chatbot UI:**  
  <img width="1600" height="1000" alt="chat-mock" src="https://github.com/user-attachments/assets/c0584a73-f01b-44b6-9266-f2f4011ee4dd" />
- **Admin Dashboard:**  
  <img width="1600" height="1126" alt="admin-mock" src="https://github.com/user-attachments/assets/e8e39f0e-4483-4685-8356-a15cf4ceeaaf" />

---

## 📝 Task 1: System Architecture

**Stack**
- **Frontend:** React (Web)  
- **Backend:** Python + Django REST Framework (DRF)  
- **Database:** MongoDB  
- **Search (optional):** Rasa / Vector Store  
- **External (future):** University Calendar, OpenAI  

**Data Flow:** Student → Frontend → Backend(API) → DB/Search → Response → Student

```mermaid
flowchart LR
  student[Student (Web)]
  fe[Frontend - React]
  be[Backend - Django (DRF)]
  db[(MongoDB)]
  vs[(Rasa / Vector Store - optional)]
  ext[(External APIs - Calendar, OpenAI)]

  student --> fe
  fe --> be
  be --> db
  be --> vs
  be --> ext
  be --> fe
  fe --> student
```

---

## 📝 Task 2: Components, Classes, and Database Design

### 2.1 Back-End Components / Services

**AuthService**
- `login(email, password) -> token`
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
- `index_faq(faq)` *(optional)*

**FeedbackService**
- `submit_feedback(faq_id, helpful, comment, user)`
- `list_feedback(faq_id)`

**FavoriteService (optional)**
- `toggle_favorite(user_id, faq_id)`
- `list_favorites(user_id)`

### 2.2 Database Design (MongoDB – Documents)

**users**
```json
{"_id":"UUID","name":"string","email":"string","password_hash":"string","role":"admin|student","created_at":"ISODate","updated_at":"ISODate"}
```

**categories**
```json
{"_id":"UUID","name":"string"}
```

**faqs**
```json
{"_id":"UUID","question":"text","answer":"text","category_id":"UUID","updated_by":"UUID","updated_at":"ISODate","created_at":"ISODate"}
```

**events**
```json
{"_id":"UUID","title":"string","start_date":"ISODate","end_date":"ISODate","location":"string","description":"string","created_at":"ISODate","updated_at":"ISODate"}
```

**feedback**
```json
{"_id":"UUID","faq_id":"UUID","user_id":"UUID","helpful":true,"comment":"string","created_at":"ISODate"}
```

**favorites**
```json
{"_id":"UUID","user_id":"UUID","faq_id":"UUID","created_at":"ISODate"}
```

---

## 📝 Task 3: Sequence Diagrams

### Use Case 1 — Student asks FAQ
```mermaid
sequenceDiagram
  autonumber
  participant Student
  participant FE as Frontend (React)
  participant BE as Backend (Django API)
  participant DB as MongoDB

  Student->>FE: Type question
  FE->>BE: GET /api/faqs?query=...
  BE->>DB: text search
  DB-->>BE: matching docs
  BE-->>FE: 200 OK (answers)
  FE-->>Student: Render answer
```

### Use Case 2 — Admin updates FAQ
```mermaid
sequenceDiagram
  autonumber
  participant Admin
  participant FE as Frontend (Admin UI)
  participant BE as Backend (Django API)
  participant DB as MongoDB

  Admin->>FE: Edit FAQ (question/answer)
  FE->>BE: PUT /api/faqs/:id (JWT)
  BE->>DB: updateOne({_id:id}, {$set:{question,answer,updated_by,updated_at}})
  DB-->>BE: ack
  BE-->>FE: 200 OK (updated)
  FE-->>Admin: Show success
```

### Use Case 3 — Student views events
```mermaid
sequenceDiagram
  autonumber
  participant Student
  participant FE as Frontend (React)
  participant BE as Backend (Django API)
  participant DB as MongoDB

  Student->>FE: Click "Deadlines"
  FE->>BE: GET /api/events?from=&to=
  BE->>DB: find({start_date:{$gte:from,$lte:to}})
  DB-->>BE: events[]
  BE-->>FE: 200 OK (events)
  FE-->>Student: Show list
```

---

## 📝 Task 4: API Specifications

### Internal APIs (Django + DRF)

| Endpoint            | Method | Input                                   | Output                                     | Role     |
|---------------------|--------|-----------------------------------------|--------------------------------------------|----------|
| `/api/auth/login`   | POST   | `{email, password}`                     | `{token, role}`                            | Admin    |
| `/api/faqs`         | GET    | `?query=keyword&category=_id`           | `[{_id, question, answer, category_id}]`   | Student  |
| `/api/faqs`         | POST   | `{question, answer, category_id}`       | `{_id, question, answer, category_id}`     | Admin    |
| `/api/faqs/:id`     | PUT    | `{question?, answer?}`                  | `{_id, question, answer, updated_at}`      | Admin    |
| `/api/events`       | GET    | `{from?, to?}`                          | `[{_id, title, start_date, end_date}]`     | Student  |
| `/api/feedback`     | POST   | `{faq_id, helpful, comment?}`           | `{_id, faq_id, helpful, comment}`          | Student  |
| `/api/favorites`    | POST   | `{faq_id}`                              | `{_id, user_id, faq_id}`                   | Student  |
| `/api/favorites`    | GET    | `Authorization: JWT`                    | `[{_id, faq_id, created_at}]`              | Student  |

### External APIs (Future)
- **University Calendar API** – deadlines/events.  
- **University Announcements API** – news/alerts.  
- **OpenAI API** – better answers/NLP.  
- **Rasa NLU (optional)** – intent/entity extraction.

---

## 📝 Task 5: SCM and QA Strategies

### Source Control (SCM)
- **Repository:** GitHub  
- **Branching:** `main` (prod), `dev` (integration), `feature/*` (per feature)  
- **Process:** Pull Requests → Code Review → Merge (protected branches)

### Quality Assurance (QA)
- **Backend:** Django Test Framework + `pytest` (unit & integration)  
- **Frontend:** React Testing Library  
- **API Testing:** Postman / DRF APIClient  
- **Linting:** `black` + `flake8` (+ `flake8-django`), `eslint` for JS  
- **CI/CD:** GitHub Actions – run tests & linters on each PR (with MongoDB service)

---

# 📌 Final Deliverable
This single document includes Tasks 0→5 for **Unibot**.
