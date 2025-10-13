# 📌 Sprint Plan – Chatbot for University Students

## 1. ✅ Break Down User Stories into Smaller Tasks

**User Story:**  
_As a student, I want to easily find university event dates._

**Tasks:**
- Design the chat interface (Chat UI)
- Build the events information database
- Develop the intelligent response model
- Connect the UI with backend system (API)
- Conduct user experience testing

---

## 2. 🟢 Prioritize Tasks Using MoSCoW

| Task                              | Priority     |
|-----------------------------------|--------------|
| Design chat interface             | Must Have    |
| Build events information database | Must Have    |
| Develop intelligent response model| Must Have    |
| Connect UI with backend (API)     | Should Have  |
| Conduct user experience testing   | Could Have   |

---

## 3. 🔄 Identify Dependencies and Assign Tasks

| Task                              | Depends On              | Assigned To            |
|-----------------------------------|--------------------------|-------------------------|
| Design chat interface             | -                        | Meshari Alosimi         |
| Build events information database | -                        | Abdulaziz Almutairi     |
| Develop response model            | Events database          | Abdulaziz Alzahrani     |
| Connect UI with backend (API)     | Chat UI + Response Model | Abdulaziz Almutairi     |
| Conduct user testing              | All previous tasks       | Saleh Alharbi           |

---

## 4. 🗓 Sprint Duration

- **Length:** 2 weeks  
- **Start Date:** October 15, 2025  
- **End Date:** October 29, 2025

---

## 5. 📋 Summary Table

| Task                              | Responsible             | Priority     | Deadline         |
|-----------------------------------|--------------------------|--------------|------------------|
| Design chat interface             | Meshari Alosimi          | Must Have    | Oct 18, 2025     |
| Build events information database | Abdulaziz Almutairi      | Must Have    | Oct 18, 2025     |
| Develop response model            | Abdulaziz Alzahrani      | Must Have    | Oct 21, 2025     |
| Connect UI with backend (API)     | Abdulaziz Almutairi      | Should Have  | Oct 25, 2025     |
| Conduct user testing              | Saleh Alharbi            | Could Have   | Oct 28, 2025     |

---
# 🚀 Sprint Execution

## 🎯 Purpose
To implement features and deliverables according to the sprint plan, ensuring high code quality, collaboration, and efficient delivery.

---

## 🛠️ Instructions

### 👨‍💻 Developers
- Focus on assigned sprint tasks.
- Follow agreed coding standards and best practices.
- Write clear, maintainable, and well-documented code.
- Collaborate using Git and implement feature branches (e.g., `feature/chat-ui`).
- Submit Pull Requests (PRs) with proper descriptions and references to task IDs.

### 🔁 SCM (Source Code Management)
- Ensure all developers are using the version control system (e.g., Git).
- Review and approve pull requests before merging into `dev` or `main` branches.
- Enforce branching strategy:
  - `main` – stable production-ready code.
  - `dev` – integration branch for all features in development.
  - `feature/*` – individual features under development.

### 🧪 QA (Quality Assurance)
- Test completed features and tasks as soon as they are marked "Ready for QA."
- Use tools like **Postman** for API testing and **manual/automated testing** for UI components.
- Log bugs and issues in the task tracking system (e.g., Trello, Jira).
- Verify bug fixes before closing tasks.

---

## 🧾 Example: Sprint for API Development

### 👨‍💻 Developers
- Implement API endpoints for:
  - Event information retrieval.
  - User authentication.
  - FAQ search.
- Write unit tests for core API functions.

### 🔁 SCM
- Code is committed under `feature/api-endpoints`.
- PRs are submitted and reviewed by another team member.
- Once approved, merged into `dev` branch.

### 🧪 QA
- Use **Postman** to test:
  - API response accuracy.
  - Status codes.
  - Error handling.
- Report any bugs to developers and retest after fixes.

---

## ✅ Expected Outcomes
- All sprint tasks are completed and tested.
- Code is merged into the main development branch.
- Bugs are identified and resolved early.
- Deliverables are ready for review and potential deployment.

