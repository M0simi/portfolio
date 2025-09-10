# 📄 Stage 2 – Project Charter: University Chatbot for Students

---

## 1. Project Objectives

**Purpose:**  
The purpose of this project is to develop a chatbot that helps university students get instant and accurate answers to common questions related to university services, deadlines, campus activities, and facilities. This chatbot aims to improve the student experience by providing 24/7 access to university-related information, making it easier and quicker to find the answers students need.

**Objectives (SMART):**  
1- **Improve Student Access to Information**: Provide instant answers to frequently asked questions about campus facilities, academic services, and important deadlines.

2- **Enhance the Student Experience**: Facilitate easy access to a variety of university information without the need for students to navigate multiple sources or wait for staff responses.

3- **Reduce Support Overhead for University Staff**: Minimize repetitive inquiries handled by university staff regarding general and common topics, allowing them to focus on more complex tasks.

---

## 2. Stakeholders and Team Roles

**Internal Stakeholders:**  
- **Team Members:**  
  - Saleh Alharbi – Project Manager (PM)  
  - Meshari Alosimi – Developer & Documentation
  - Abdulaziz Almutairi – Backend Developer  
  - Abdulaziz Alzahrani – Frontend Developer  

- **Tutors/Instructors:** Provide feedback and evaluation.  

**External Stakeholders:**  
- University students (end-users)  
- University administration (support and potential integration partner)
- External AI Services Providers (if applicable): Might offer APIs or technologies used to power the chatbot’s AI functionality.

**Roles & Responsibilities:**  
- **Project Manager (PM):** Oversees planning, ensures progress, manages risks.  
- **Frontend Developer:** Builds chatbot interface and user experience.  
- **Backend Developer:** Develops server-side logic, database integration, and APIs.  
- **Developer & Documentation:** Supports development tasks and maintains clear documentation.  

---

## 3. Scope

**In-Scope:**  
- Providing answers to common university-related questions (e.g., campus facilities, deadlines, events). 
- Real-time data regarding university services, facilities (e.g., library, cafeteria), and key events. 
- Web or mobile-friendly interface for students.
- Development of an intuitive user interface that allows students to interact with the chatbot.
- 24/7 availability.  

**Out-of-Scope:**  
- The MVP will not integrate with university systems for personalized student data like grades, course registrations, etc.  
- Advanced features like predictive analytics or voice assistants (future phases).
- No advanced NLP capabilities (e.g., understanding complex questions or casual conversations).  
- Full-scale integration with every university system.
- The chatbot will be available primarily through a web interface, not as a mobile app in this MVP version.
- Multi-Language Support: The MVP will not include multi-language support for international students (will be added later if needed).  

---

## 4. Risks

| **Risk**                                                                 | **Category**       | **Description**                                                                                       | **Mitigation Strategy**                                                                                   |
|--------------------------------------------------------------------------|--------------------|--------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| Lack of experience with chatbot development tools or NLP libraries       | Technical          | Team members may be unfamiliar with platforms like Dialogflow, Rasa, or NLP models like GPT.           | Allocate time for team training sessions and tutorials during the initial sprint. Assign learning tasks.   |
| Integration difficulty with university systems or databases              | Technical          | Challenges in connecting with external systems to retrieve real-time data.                             | Focus the MVP on public data; plan integration for later stages. Build a mock API to simulate real data.   |
| Delay in meeting deadlines                                               | Timeline           | Potential delays due to scope creep, unforeseen technical issues, or team availability.                | Use agile methodology with short sprints, set realistic timelines, and conduct weekly progress reviews.    |
| Poor team communication or collaboration                                 | Team Dynamics      | Miscommunication may lead to duplicated efforts or incomplete tasks.                                   | Set clear communication guidelines, hold weekly sync meetings, and use Slack + Notion for task tracking.   |
| Insufficient or unclear data for chatbot training                        | Technical          | Limited or low-quality FAQ data may affect chatbot accuracy and performance.                           | Start with scraped/available FAQ data, and validate it with students or university sources when possible.  |
| Low student adoption or interest in using the chatbot                    | User Adoption      | Students may not be aware of the chatbot or may not find it useful.                                    | Create an onboarding strategy (e.g., demo videos, posters), and gather user feedback for continuous improvement. |
| Difficulty in maintaining chatbot accuracy as information changes        | Maintenance        | University services and deadlines often change, requiring regular content updates.                     | Design a simple content management backend or allow admin users to update key information manually.        |
| Privacy and data protection concerns                                     | Legal / Technical  | Risk of violating privacy policies when handling student-related queries.                              | Ensure the chatbot doesn’t process sensitive personal data. Follow local laws (e.g., GDPR/FERPA) in design.|
| Over-reliance on one or two key team members                             | Team Dynamics      | Bottlenecks if certain roles become unavailable or overwhelmed.                                        | Cross-train members, document progress thoroughly, and foster knowledge sharing within the team.          |


---

## 5. High-Level Plan

**Project Stages & Timeline:**  

- **Stage 1:** Idea Development & Team Formation ✅  
- **Stage 2:** Project Charter Development (Current, Week 3–4)  
- **Stage 3:** Technical Documentation (Week 5–6)  
- **Stage 4:** MVP Development (Week 7–10)  
- **Stage 5:** Project Closure & Final Presentation (Week 11–12)  

**Key Milestones:**  
- Week 4: Finalize Project Charter  
- Week 6: Complete Technical Documentation  
- Week 10: Deliver MVP for testing  
- Week 12: Final Presentation & Closure  

---

## 🗂️ 4. Develop a High-Level Plan

### Project Timeline & Milestones

Below is the high-level plan outlining the major phases of the project and their associated milestones.

| **Stage**                       | **Weeks**         | **Description**                                                                 | **Key Deliverables / Milestones**                                              |
|--------------------------------|---------------------|----------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| **Stage 1: Idea Development**  | Week 1–2         | Brainstorming, idea evaluation, and MVP selection.                              | ✅ Stage 1 Report (Team Formation & Idea Justification)                         |
| **Stage 2: Project Charter**   | Week 3–4      | Define project scope, goals, success criteria, and risk assessment.             | 📄 Project Charter Document                                                     |
| **Stage 3: Technical Documentation** | Week 5–6 | Create Software Requirements Specification (SRS), use cases, and architecture.  | 📘 SRS Document, System Architecture Diagrams, Use Case Diagrams                |
| **Stage 4: MVP Development**   | Week 7–10     | Build the chatbot MVP with core functionalities and perform testing.            | 💻 Working MVP, GitHub Code Repository, Internal Testing Report                 |
| **Stage 5: Project Closure**   | Week 11–12    | Final presentation, documentation handover, and team reflection.                | 🎓 Final Report, Presentation Slides, Demo Video, Lessons Learned               |

---

### Summary Timeline

