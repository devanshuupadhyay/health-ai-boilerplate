# Health AI Boilerplate

<div align="center">
    <a href="https://devanshuupadhyay.netlify.app/projects/health-ai-boilerplate">
        <h1>Launch FHIR / AI Demo</h1>
    </a>
</div>

## Overview

This project provides a comprehensive starting point (boilerplate) for building modern, AI-enhanced healthcare applications. It combines a Nuxt 3 frontend, a FastAPI backend, and a separate AI microservice, all containerized with Docker and equipped with a local observability stack. The goal is to accelerate development by providing a robust foundation with essential features already integrated.

This boilerplate demonstrates how to manage patient data (using FHIR-like structures), handle clinical notes, integrate an AI model for summarization, implement full-text search, and monitor the application's health and performance.

---

## Features

- **Full-Stack Framework:** Vue 3/Nuxt 3 frontend and Python/FastAPI backend.
- **AI Integration:** Dedicated FastAPI service for AI tasks (e.g., clinical note summarization using Hugging Face Transformers).
- **Database:** PostgreSQL managed via SQLAlchemy ORM and Alembic migrations.
- **Background Tasks:** Celery with Redis for handling asynchronous operations like AI processing.
- **Authentication:** Token-based authentication (JWT) using FastAPI's security utilities.
- **Search:** Full-text search integration using Meilisearch.
- **FHIR-Inspired Data Model:** Uses Pydantic schemas mimicking FHIR resources for patient data.
- **Observability Stack (Local):**
  - **Logging:** Loki for log aggregation.
  - **Metrics:** Prometheus for metrics collection.
  - **Visualization:** Grafana for dashboards (logs & metrics).
  - **Log Shipping:** Promtail for collecting logs from Docker containers.
- **Containerization:** Docker and Docker Compose for easy setup and consistent environments.
- **Frontend:**
  - **UI Components:** Headless UI and Heroicons.
  - **State Management:** Pinia.
  - **Styling:** Tailwind CSS with Dark Mode support.
  - **Form Validation:** VeeValidate with Zod.
  - **Testing:** Cypress for E2E testing.
- **CI/CD:** Basic GitHub Actions workflow for building and linting.
- **Developer Experience:** Includes pre-commit hooks (Black, Flake8) and VS Code settings.

---

## Tech Stack

- **Frontend:** Nuxt 3 (Vue 3), Tailwind CSS, Pinia, VeeValidate, Cypress, TypeScript
- **Backend:** FastAPI (Python 3.10), SQLAlchemy, Alembic, Celery, Pydantic, PostgreSQL
- **AI Service:** FastAPI (Python 3.10), Hugging Face Transformers, PyTorch
- **Database:** PostgreSQL
- **Cache/Broker:** Redis
- **Search:** Meilisearch
- **Containerization:** Docker, Docker Compose
- **Observability:** Prometheus, Grafana, Loki, Promtail
- **CI/CD:** GitHub Actions

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Docker & Docker Compose:** Essential for running the containerized services. [Download Docker](https://www.docker.com/products/docker-desktop/).
- **Node.js:** Required for the Nuxt 3 frontend. We recommend using the version specified in `.github/workflows/ci-cd.yml` (currently Node 20). [Download Node.js](https://nodejs.org/).
- **Python:** Required for the FastAPI backend and AI service (currently Python 3.10). [Download Python](https://www.python.org/).
- **Git:** For cloning the repository.
- **(Optional) VS Code Extensions:**
  - **Docker:** ([ms-azuretools.vscode-docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)) - Useful for managing containers directly within VS Code.
  - **Python:** ([ms-python.python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)) - For Python development and debugging within the backend/AI services.
  - **Volar:** ([Vue.volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar)) - Recommended for Vue/Nuxt development.
  - **Tailwind CSS IntelliSense:** ([bradlc.vscode-tailwindcss](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss)) - Provides autocompletion and linting for Tailwind classes.

---

## Getting Started

Follow these steps to get the Health AI Boilerplate running locally:

1.  **Clone the Repository:**

    ```bash
    git clone <your-repository-url>
    cd health-ai-boilerplate
    ```

2.  **Set Up Environment Variables:**

    - Copy the example environment file for the backend:
      ```bash
      cp backend/.env.example backend/.env
      ```
    - **Important:** Open `backend/.env` and fill in the required values:
      - `DATABASE_URL`: Defaults should work with the provided Docker Compose setup (`postgresql://postgres:postgres@db:5432/health_ai_db`).
      - `SECRET_KEY`: **Generate a strong, unique secret key** for JWT authentication. You can use `openssl rand -hex 32` or an online generator.
      - `SENTRY_DSN` (Optional): If you want to use Sentry for error tracking, add your DSN here.
      - Grafana Cloud variables (Optional): If you intend to ship logs/metrics to Grafana Cloud, fill in `LOKI_URL`, `LOKI_USERNAME`, `LOKI_API_KEY`, `PROM_REMOTE_WRITE_URL`, `PROM_USERNAME`, `PROM_API_KEY`. Otherwise, the local observability stack will be used.

3.  **Build and Run with Docker Compose:**

    - This command will build the images for the `backend`, `ai`, and other services, and start all containers defined in `docker-compose.yml`.

    ```bash
    docker compose up --build -d
    ```

    - **VS Code Tip:** If you have the Docker extension installed, you can manage your containers (start, stop, view logs) directly from the Docker view in the activity bar.

4.  **Install Frontend Dependencies:**

    - Navigate to the frontend directory and install the necessary Node.js packages.

    ```bash
    cd frontend
    npm install
    cd ..
    ```

    - _(Note: The `frontend/README.md` mentions `npm install`, `pnpm install`, `yarn install`, or `bun install` as options)_.

5.  **Run Database Migrations:**

    - Execute the Alembic migrations _inside_ the running backend container to set up the database schema.

    ```bash
    docker compose exec backend alembic upgrade head
    ```

6.  **Seed Initial Data (Optional but Recommended):**

    - Run the seed script _inside_ the backend container to populate the database with initial data (like a test user and patient).

    ```bash
    docker compose exec backend python seed.py
    ```

7.  **Run the Frontend Development Server:**
    - Start the Nuxt development server. It will connect to the backend API via the proxy configured in `nuxt.config.ts`.
    ```bash
    cd frontend
    npm run dev
    cd ..
    ```

**You should now be able to access the application!**

---

## Usage

- **Frontend Application:** Open your browser and navigate to [http://localhost:3000](http://localhost:3000).
  - **Login Credentials:** Use the seeded user: `test@example.com` / `password123`.
- **Backend API Docs (Swagger UI):** Accessible at [http://localhost:8008/docs](http://localhost:8008/docs).
- **AI Service Health Check:** Check status at [http://localhost:8001/health](http://localhost:8001/health).
- **Meilisearch (API):** Base URL at [http://localhost:7700](http://localhost:7700). Use the `MEILI_MASTER_KEY` from `docker-compose.yml` for testing.
- **Grafana (Local Observability):** Access dashboards at [http://localhost:3001](http://localhost:3001) (Login: `admin`/`admin`).
- **Prometheus:** Access metrics and targets at [http://localhost:9090](http://localhost:9090).
- **Loki:** Log query endpoint (usually accessed via Grafana) at [http://localhost:3100](http://localhost:3100).

---

## For Developers Using This Boilerplate

This boilerplate is designed to be a starting point. Here's how you can adapt and build upon it:

1.  **Customize the Frontend:**
    - Modify existing Vue components in `frontend/components/`.
    - Add new pages in `frontend/pages/`.
    - Adjust Tailwind CSS theme and styles in `frontend/tailwind.config.js` and `frontend/assets/css/main.css`.
    - Extend Pinia stores (`frontend/stores/`) for new state management needs.
2.  **Extend the Backend API:**
    - Define new Pydantic schemas in `backend/app/schemas/`.
    - Create new SQLAlchemy models in `backend/app/models/`. Remember to generate Alembic migrations (`docker compose exec backend alembic revision --autogenerate -m "Your migration message"`) and apply them (`docker compose exec backend alembic upgrade head`).
    - Implement new business logic in `backend/app/services/`.
    - Add new FastAPI routers and endpoints in `backend/app/api/v1/`.
3.  **Enhance the AI Service:**
    - Add new AI models or tasks in `ai/main.py`.
    - Update `ai/requirements.txt` with any new Python dependencies.
    - Adjust the `ai/Dockerfile` if necessary.
4.  **Modify Background Tasks:**
    - Add new Celery tasks in `backend/app/tasks/`. Remember to include them in `celery_worker.py`'s `autodiscover_tasks`.
5.  **Configure Observability:**
    - Adjust Prometheus scrape targets (`infra/observability/prometheus/prometheus.yml`).
    - Customize Grafana dashboards (`infra/observability/grafana/provisioning/dashboards/`) or build new ones via the UI.
    - Modify Promtail relabeling rules (`infra/observability/promtail/promtail-config.yml`) for log parsing and labeling.
6.  **Update Dependencies:** Regularly update dependencies in:
    - `frontend/package.json` (run `npm update` in `frontend/`)
    - `backend/requirements.txt` (run `pip install -r requirements.txt` inside the backend container or rebuild the image)
    - `ai/requirements.txt` (run `pip install -r requirements.txt` inside the AI container or rebuild the image)
7.  **Deployment:**
    - The included `docker-compose.yml` is primarily for local development. For production, consider:
      - Using managed database and Redis services.
      - Optimizing Docker images for size and security.
      - Implementing a robust deployment strategy (e.g., Kubernetes, serverless functions, managed container platforms).
      - Configuring production-level observability (e.g., Grafana Cloud, Datadog, Sentry).
      - Securing sensitive information (secrets management).
      - Generating production search keys for Meilisearch.

---

## Project Structure

The repository is organized into the following main directories:

- **`/ai`**: Contains the separate FastAPI service responsible for AI tasks (e.g., summarization). Includes its own `Dockerfile` and `requirements.txt`.
- **`/backend`**: Contains the main FastAPI application.
  - `alembic/`: Database migration scripts.
  - `app/`: Core application code.
    - `api/`: API endpoint definitions (routers, dependencies).
    - `core/`: Configuration, security, logging setup.
    - `db/`: Database session management.
    - `models/`: SQLAlchemy database models.
    - `schemas/`: Pydantic data validation schemas.
    - `services/`: Business logic layer.
    - `tasks/`: Celery background task definitions.
  - `celery_worker.py`: Celery application instance.
  - `main.py`: FastAPI application entry point.
  - `requirements.txt`: Python dependencies.
  - `Dockerfile`: Instructions for building the backend Docker image.
  - `seed.py`: Script to populate the database with initial data.
- **`/frontend`**: Contains the Nuxt 3 application.
  - `assets/`: Global styles and static assets.
  - `components/`: Reusable Vue components.
  - `composables/`: Vue composables (like `useDemoToaster`).
  - `cypress/`: Cypress E2E tests.
  - `layouts/`: Nuxt layout definitions.
  - `middleware/`: Nuxt route middleware (e.g., authentication).
  - `pages/`: Application pages and routing structure.
  - `plugins/`: Nuxt plugins (e.g., Meilisearch client setup).
  - `public/`: Static files served directly (like `favicon.ico`).
  - `stores/`: Pinia state management stores.
  - `types/`: TypeScript type definitions.
  - `nuxt.config.ts`: Nuxt application configuration.
  - `package.json`: Node.js dependencies and scripts.
- **`/infra`**: Contains infrastructure-related configurations.
  - `observability/`: Configuration files for the local observability stack (Grafana, Loki, Prometheus, Promtail).
- **`.github/workflows`**: Contains GitHub Actions workflow definitions (e.g., `ci-cd.yml`).
- **`docker-compose.yml`**: Defines the multi-container setup for local development.

---

## Observability

This boilerplate includes a pre-configured local observability stack using Docker Compose, allowing you to monitor application logs and metrics during development.

- **Prometheus:** Scrapes metrics from the backend service (via `prometheus-fastapi-instrumentator`). Access at [http://localhost:9090](http://localhost:9090).
- **Loki:** Aggregates logs from all Docker containers via Promtail.
- **Promtail:** Automatically discovers running containers and ships their logs to Loki.
- **Grafana:** Provides dashboards for visualizing logs (from Loki) and metrics (from Prometheus). Access at [http://localhost:3001](http://localhost:3001) (Login: `admin`/`admin`).
- **Sentry:** (Optional) If configured with a DSN in `backend/.env`, the backend will send error reports to Sentry.

**Note:** The Grafana Agent configuration (`infra/observability/agent/agent-config.river`) is provided as an alternative setup for shipping logs and metrics directly to Grafana Cloud (requires environment variables set in `.env`). The default `docker-compose.yml` uses the local stack (Prometheus, Loki, Promtail).

---

## Testing

- **Frontend E2E Tests:** End-to-end tests for the frontend are implemented using Cypress.
  - **Configuration:** `frontend/cypress.config.ts`.
  - **Tests:** Located in `frontend/cypress/e2e/` (e.g., `rpa-workflow.cy.ts`).
  - **Running Tests:**
    ```bash
    cd frontend
    npx cypress open # Opens the Cypress Test Runner UI
    # or
    npx cypress run # Runs tests headlessly in the terminal
    cd ..
    ```
    _(Ensure the full application stack is running via `docker compose up -d` and `npm run dev` in the frontend directory before running Cypress tests)._
- **Backend Tests:** (Placeholder) Currently, the CI pipeline includes a placeholder step for backend tests. You would typically add tests using a framework like `pytest`.
