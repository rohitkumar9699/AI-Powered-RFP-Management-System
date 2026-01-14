# AI-Powered RFP Management System - Frontend

## Overview
The frontend is built with Angular (standalone components) and Bootstrap 5, providing a modern, responsive user interface for managing RFPs (Request for Proposals), vendors, and proposals.

## Features

### Dashboard
- **Statistics Cards**: Display total vendors, active RFPs, total proposals, and average proposal score
- **Recent RFPs**: Shows the 5 most recent RFPs with status badges
- **Top Vendors**: Displays the top 5 vendors by activity

### Vendors Management
- **View Vendors**: List all vendors with their details (name, email, contact person, city, country, status)
- **Add Vendor**: Create new vendors with a form
- **Delete Vendor**: Remove vendors from the system
- **Edit Vendor**: Placeholder for future functionality

### RFPs Management  
- **View RFPs**: Display all RFPs with title, budget, deadline, vendor count, and status
- **Create RFP**: Placeholder for RFP creation form
- **Edit/Delete RFPs**: Action buttons for management

### Proposals Management
- **View Proposals**: List all proposals with vendor name, RFP ID, price, score, status, and delivery time
- **Score Badges**: Color-coded performance indicators
  - Green (90+), Blue (80-89), Yellow (70-79), Red (<70)
- **Average Score**: Shows overall proposal quality metrics
- **View Details**: Quick view of proposal details

## Technology Stack
- **Framework**: Angular 18+ (Standalone Components)
- **UI Framework**: Bootstrap 5.3
- **HTTP Client**: HttpClientModule
- **Styling**: SCSS
- **Language**: TypeScript

## Project Structure
```
frontend/
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   ├── dashboard.component.ts/html/scss
│   │   │   ├── vendors.component.ts/html/scss
│   │   │   ├── rfps.component.ts/html/scss
│   │   │   └── proposals.component.ts/html/scss
│   │   ├── services/
│   │   │   └── api.service.ts
│   │   ├── app.component.ts/html/scss
│   │   └── app.component.spec.ts
│   ├── index.html
│   ├── main.ts
│   └── styles.scss
├── angular.json
├── tsconfig.json
├── package.json
└── README.md
```

## Running the Application

### Development Server
```bash
cd frontend
npm install
npm start
```
The application will be available at `http://localhost:4200`

### Production Build
```bash
npm run build
```
Output will be in the `dist/` directory

## API Integration

### API Service
The `ApiService` in `src/app/services/api.service.ts` handles all HTTP requests to the backend API.

**Base URL**: `https://bookish-telegram-9rr4qpgpr9rcx7r-8000.app.github.dev/api`

### Available Endpoints
- **Vendors**: `/vendors/` (GET, POST, PUT, DELETE)
- **RFPs**: `/rfps/` (GET, POST, PUT, DELETE)
- **Proposals**: `/proposals/` (GET, POST)
- **AI Functions**: `/ai/` endpoints for natural language processing and proposal evaluation
- **Email**: `/email/` endpoints for email integration

## Component Architecture

All components are **standalone**, meaning they:
- Don't require NgModule declarations
- Import their own dependencies directly
- Can be used independently

### Shared Features
- CommonModule for *ngIf, *ngFor, pipes
- FormsModule for two-way binding [(ngModel)]
- Bootstrap utility classes for styling

## Styling

Components use:
- **Global styles**: `styles.scss` (Bootstrap utilities, global CSS)
- **Component styles**: Individual `*.component.scss` files for scoped styling
- **Bootstrap Classes**: Responsive grid, cards, badges, buttons

## Features Planned
- [ ] RFP creation from natural language
- [ ] Advanced proposal evaluation with AI
- [ ] Email integration for RFP distribution
- [ ] Proposal comparison views
- [ ] Export reports
- [ ] User authentication
- [ ] Real-time notifications

## Browser Support
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Notes
- The application expects the backend API to be running at the configured URL
- CORS is configured on the backend to accept requests from localhost:4200
- All API responses are expected in the format: `{ count, next, previous, results: [] }`
