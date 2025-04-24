# DevOps Training

This repository is dedicated to tracking my journey through DevOps training at Calsoft. It serves as a collection of topics, insights, and hands-on projects as I progress through various phases of learning.

---

## 📜 Contents

1. [Part 1: Foundations of DevOps and Cloud Computing - Week 1-2](#part-1-foundations-of-devops-and-cloud-computing---week-1-2)
   - [What is DevOps?](#what-is-devops)
     - [🌟 Introduction to DevOps and Its Impact](#-introduction-to-devops-and-its-impact)
     - [🎨 Emma’s Story – Real-world Analogy](#-emmas-story--real-world-analogy)
     - [🧱 Software Development Lifecycle (SDLC)](#-software-development-lifecycle-sdlc)
     - [🔄 Software Development Models](#-software-development-models)
     - [⚠️ Challenges with Agile SDLC – Developer vs. Operations](#%EF%B8%8F-challenges-with-agile-sdlc--developer-vs-operations)
     - [🚧 Wall Between Dev and Ops](#-wall-between-dev-and-ops)
     - [🚀 Introduction to DevOps](#-introduction-to-devops)
     - [🔧 DevOps in Action – Breaking the Wall](#-devops-in-action--breaking-the-wall)
     - [🛠️ DevOps Lifecycle – Fully Automated Flow](#%EF%B8%8F-devops-lifecycle--fully-automated-flow)
   - [DevOps Principles, Practices, and Culture](#devops-principles-practices-and-culture)
     - [🧭 DevOps Principles](#-devops-principles)
     - [🛠️ DevOps Practices](#%EF%B8%8F-devops-practices)
     - [🌱 DevOps Culture](#-devops-culture)
   - [Assignment: Setup Helloworld Simple Jenkins CI-CD on Local Setup](Helloworld_Jenkins_CI_CD_local_setup.md)

---

## Part 1: Foundations of DevOps and Cloud Computing - Week 1-2

### What is DevOps?

#### 🌟 Introduction to DevOps and Its Impact

**Key Idea:**  
DevOps transforms the speed and efficiency of software delivery, turning tasks that took **hours or days** into ones completed in **minutes**.

**Explanation:**  
Traditionally, software development and deployment involved **siloed teams**, lengthy processes, and significant delays. DevOps introduces a **culture and set of practices** that unite development and operations, allowing companies to deliver updates faster and more reliably. This agility allows businesses to **focus more on their products and services**, which is why it's being rapidly adopted across industries.

---

#### 🎨 Emma’s Story – Real-world Analogy

**Scenario:**  
Emma, an artist who owns a physical art gallery, wants to **expand online** through a mobile app.

**What She Needs:**
- A team of **developers** to build the app.
- **Testers** to ensure its quality.
- **Operations/admins** to host and maintain the app on servers.

**Explanation:**  
Emma's situation mirrors many modern businesses that wish to digitize their services. Since she doesn’t have a technical team, she partners with a software firm. Through her journey, we explore the **real-life application of DevOps principles** in a typical software development cycle.

---

#### 🧱 Software Development Lifecycle (SDLC)

**Phases of SDLC:**

1. **Requirement Gathering & Analysis**  
   - Understanding what features the product should have.
   - How users will interact with it.
   - Research on market demand and competitive landscape.

2. **Planning**  
   - Estimating **cost**, **time**, and **resources** needed.
   - Identifying potential **risks**.

3. **Designing**  
   - Architects create technical blueprints and roadmaps for development.
   - These design documents guide developers in the coding phase.

4. **Development**  
   - Developers begin writing the actual software code.
   - This is often the most exciting and creative phase for devs.

5. **Testing**  
   - The software is thoroughly tested to catch bugs and issues.
   - It only moves forward once all defects are resolved.

6. **Deployment**  
   - The tested software is moved to the **production environment** where real users can interact with it.

7. **Maintenance**  
   - Keeping the app running smoothly.
   - Applying updates, fixing issues, and adapting to changes over time.

**Explanation:**  
This step-by-step process is structured and ensures quality. The operations team plays a critical role post-deployment, ensuring the software stays available and stable.

---

#### 🔄 Software Development Models

**1. Waterfall Model:**  
   - Each phase is done **sequentially**.
   - Once a phase is completed, you **can’t go back**.
   - Working software is seen **very late**, possibly months into development.
   - Not ideal if requirements are **uncertain or evolving**, like in Emma’s case.

**2. Agile Model:**  
   - Requirements are broken into **smaller tasks (sprints/iterations)**.
   - Iterations typically last **2 to 4 weeks**.
   - Each sprint delivers a **working prototype** or feature.
   - Stakeholders like Emma can give **frequent feedback**, helping shape the final product as it evolves.

**Explanation:**  
Agile offers **flexibility**. It’s best when clients are unsure about all features upfront, or when they may change ideas as the product takes shape.

---

#### ⚠️ Challenges with Agile SDLC – Developer vs. Operations

**Problem Emerges:**  
As development progresses using Agile, the **operations team (ops)** faces difficulties in keeping up:
- Code needs to be **frequently deployed** for testing.
- Testers sometimes **can’t access** the servers, or test cases fail.
- Deployment instructions may be **unclear** or miscommunicated.

**Explanation:**  
Agile demands **frequent updates**. The ops team is burdened by:
- Constant deployment requests.
- Managing server uptime.
- Fixing issues on short notice.

This leads to **missed deadlines**, frustration, and ultimately delays in product delivery — making Emma (the client) unhappy.

---

#### 🚧 Wall Between Dev and Ops

**The Great Divide:**  
- **Developers** throw their code "over the wall".
- **Operations** team has to figure out how to deploy it.
- Devs complain about **slow deployments**.
- Ops complains about **poor instructions and pressure**.

**Real-world Consequences:**  
- **Delays and bugs** in production.
- **Unhappy customers** and **lost business**.
- Development and operations are **misaligned**, even though they’re on the same project.

**Analogy:**  
Developers are **Agile** — quick and iterative.  
Operations are **ITIL (Waterfall)-driven** — structured and stability-focused.  
This clash causes friction.

---

#### 🚀 Introduction to DevOps

**Reggie’s Realization:**  
Reggie, the director, identifies the root cause:  
Dev and Ops aren’t **collaborating effectively**.

**Solution: DevOps**  
- A **DevOps consultant** is brought in to unify and streamline the process.
- The goal isn’t magic — it’s **collaboration, communication, and integration**.

---

#### 🔧 DevOps in Action – Breaking the Wall

**Training and Culture Shift:**  
- **Developers** are trained in operations concepts (e.g., server behavior, deployment pipelines).
- **Operations** are trained in Agile concepts (e.g., iterations, sprints).
- Every team is introduced to **automation tools and techniques**.

**Automation in DevOps:**  
All key tasks are automated:
- **Code building**
- **Testing (unit and integration)**
- **Infrastructure provisioning**
- **Software deployment**

Automation ensures:
- **No human errors**
- **Faster and repeatable** delivery process

**Explanation:**  
Instead of handing things over blindly, both teams:
- **Work together**
- Use **automated pipelines**
- Share knowledge and responsibility

---

#### 🛠️ DevOps Lifecycle – Fully Automated Flow

**Key Features:**
- **No manual intervention**
- **Quick iterations**
- Everything is **integrated and streamlined**
- Ensures **consistency**, **efficiency**, and **rapid delivery**

**Outcome:**  
- Any request Emma makes can now be fulfilled **quickly**.
- Customers are **satisfied** with timely updates and a stable experience.
- Emma's idea has **successfully scaled into a thriving online business**.

---

#### 🎉 Summary

**Before DevOps:**
- Siloed teams.
- Miscommunication.
- Delays in development and deployment.
- Frustrated stakeholders.

**After DevOps:**
- Seamless collaboration.
- Automated pipelines.
- Continuous delivery and integration.
- Happy customers and business growth.

---

### DevOps Principles, Practices, and Culture

#### 🧭 **DevOps Principles**

DevOps is not just a set of tools—**it’s a philosophy, a mindset, and a set of principles** that guide teams to deliver better software faster and more reliably.

1. **Collaboration and Communication**  
   DevOps breaks down silos between development and operations teams, fostering continuous collaboration and shared responsibilities.

2. **End-to-End Responsibility**  
   Teams own the software across its entire lifecycle, from development to maintenance.

3. **Continuous Improvement**  
   Focuses on small, frequent updates, retrospectives, and learning from failures.

4. **Automation First**  
   Automates repetitive tasks to save time and improve reliability.

5. **Customer-Centric Action**  
   Aligns technical efforts with customer satisfaction and business outcomes.

---

#### 🛠️ **DevOps Practices**

1. **Continuous Integration (CI)**  
   Frequent code merges with automated builds and tests to ensure quality.

2. **Continuous Delivery (CD)**  
   Prepares code for production with automated deployment to production-like environments.

3. **Infrastructure as Code (IaC)**  
   Manages infrastructure using code for consistency and repeatability.

4. **Automated Testing**  
   Includes unit, integration, and end-to-end tests integrated into CI/CD pipelines.

5. **Monitoring and Logging**  
   Real-time monitoring and insights for performance and reliability.

6. **Configuration Management**  
   Maintains consistency of software performance across environments.

7. **Version Control for Everything**  
   Applies version control to source code, infrastructure, configurations, and pipelines.

8. **Security as Code (DevSecOps)**  
   Integrates security practices into the development lifecycle.

---

#### 🌱 **DevOps Culture**

1. **Blameless Culture**  
   Focuses on learning from failures and improving systems rather than assigning blame.

2. **Shared Ownership**  
   Encourages empathy and shared responsibilities among all roles.

3. **Learning and Experimentation**  
   Promotes a growth mindset and experimentation as paths to innovation.

4. **Agility and Flexibility**  
   Thrives in environments where rapid changes and adaptability are critical.

5. **Feedback Loops**  
   Embeds constant feedback loops for continuous improvement.

6. **Tooling Supports Culture, Not Defines It**  
   Tools enable collaboration and efficiency but are not the foundation of DevOps.

---