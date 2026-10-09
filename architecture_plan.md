# AgriWater AI Architecture and Plan

## 1. Project Architecture

The project is built as a monorepo containing two main parts:

- **Frontend (`/frontend`)**: A React application built with Vite, TypeScript, and Tailwind CSS. It handles the user interface, client-side validation, and API communication.
- **Backend (`/backend`)**: A Python API built with FastAPI. It handles the business logic, database interactions, authentication, and machine learning model integration.
- **Database**: A MySQL relational database managed via SQLAlchemy ORM and Alembic migrations.

## 2. Folder Structure

```
Crop_Prediction_Mahaweli_C_Zone/
├── backend/
│   ├── app/
│   │   ├── api/routes/       # API endpoints (auth, evaporation, crops, etc.)
│   │   ├── core/             # Configuration, security, and dependencies
│   │   ├── ml/               # Machine Learning integration (mock & sklearn providers)
│   │   ├── models/           # SQLAlchemy database models
│   │   ├── schemas/          # Pydantic validation schemas
│   │   ├── services/         # Business logic services
│   │   ├── db.py             # Database connection setup
│   │   └── main.py           # FastAPI application entry point
│   ├── tests/                # Pytest integration and unit tests
│   ├── requirements.txt      # Python dependencies
│   └── alembic/              # Database migrations (to be created)
├── frontend/
│   ├── public/               # Static assets
│   ├── src/
│   │   ├── assets/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Page components (Landing, Dashboard, Predictor)
│   │   ├── services/         # API client and hooks
│   │   ├── App.tsx           # Main application component
│   │   └── main.tsx          # React DOM entry point
│   ├── package.json          # Node dependencies
│   ├── vite.config.ts        # Vite configuration
│   └── tailwind.config.js    # Tailwind configuration
└── README.md                 # Project documentation
```

## 3. Implementation Status and Plan

### Phase 1: Setup and Foundation (In Progress)
- [x] Create monorepo structure
- [x] Set up FastAPI and React scaffolds
- [x] Configure environment variables
- [x] Implement health checks
- [x] Create initial MySQL database and Alembic migrations

### Phase 2: Authentication and Layouts
- [x] Implement JWT authentication (Backend)
- [x] Setup Role-based access control (Backend)
- [x] Setup React Router and protected routes (Frontend)
- [x] Create basic layouts (Public, Specialist, Admin)

### Phase 3: Evaporation ML Integration
- [x] Implement the provider interface and Mock provider (Backend)
- [x] Complete provider selection and API endpoints (Backend)
- [x] Build Evaporation prediction form and UI (Frontend)

### Phase 4 & 5: Core Features and Dashboards
- [x] Crop catalogue and calendar
- [x] Water calculator
- [x] Scenario simulator
- [x] Dashboards for Specialists and Admins

### Phase 6: Polish and Testing
- [x] Comprehensive testing (Backend and Frontend)
- [x] UI/UX refinements
- [x] Final documentation
