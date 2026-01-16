# AI-Powered RFP Management System

A comprehensive web application for managing Request for Proposal (RFP) processes with AI-powered natural language processing, vendor management, proposal comparison, and intelligent recommendations.

## 📋 Problem Statement

Build an AI-powered RFP Management System that:

1. **Create RFPs from Natural Language** - Users can describe procurement needs in plain English, and AI extracts structured RFP with requirements, budget, and timeline
2. **Manage Vendors & Distribute RFPs** - Create and manage vendor database, send RFPs via email to selected vendors
3. **Receive & Parse Proposals** - Receive vendor responses via email, automatically parse them using AI to extract price, delivery time, warranty, payment terms
4. **Compare Proposals & Recommend** - Analyze all proposals against RFP requirements, score them, and provide AI-powered recommendation for best vendor

---

## 🏗️ System Architecture

### Technology Stack

**Backend:**
- Framework: Django 4.0+ with Django REST Framework
- Database: SQLite (development) or PostgreSQL (production)
- AI: Ollama with TinyLlama
- Email: Gmail SMTP (sending) and IMAP (receiving)
- Language: Python 3.8+

**Frontend:**
- Framework: Angular 17+
- UI: Bootstrap 5.3
- HTTP: Angular HttpClient
- State: Component-based with services
- Language: TypeScript 5.0+

### Project Structure

```
/backend/                          # Django backend
├── rfp_management/
│   ├── settings.py                # Django configuration
│   ├── urls.py                    # Main URL routing
│   ├── wsgi.py                    # WSGI application
│   └── apps/
│       ├── vendors/               # Vendor management
│       │   ├── models.py
│       │   ├── views.py
│       │   ├── serializers.py
│       │   └── urls.py
│       ├── rfps/                  # RFP management + natural language
│       │   ├── models.py
│       │   ├── views.py
│       │   ├── serializers.py
│       │   └── urls.py
│       ├── proposals/             # Proposal handling
│       │   ├── models.py
│       │   ├── views.py
│       │   ├── serializers.py
│       │   └── urls.py
│       ├── ai/                    # AI services
│       │   ├── services.py        # OpenAI integration
│       │   ├── views.py
│       │   └── urls.py
│       └── email_service/         # Email handling
│           ├── services.py        # SMTP/IMAP integration
│           ├── views.py
│           └── urls.py
├── manage.py
└── .env                           # Environment variables

/frontend/                         # Angular frontend
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   ├── dashboard.component.*        # KPI dashboard
│   │   │   ├── vendors.component.*          # Vendor CRUD
│   │   │   ├── rfps.component.*             # RFP management
│   │   │   └── proposals.component.*        # Proposal evaluation
│   │   ├── services/
│   │   │   └── api.service.ts               # API integration
│   │   ├── app.component.*
│   │   └── models/
│   ├── main.ts
│   └── index.html
├── package.json
├── angular.json
└── tsconfig.json
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ 
- Node.js 16+
- npm or yarn
- Git
- Ollama installed with tinyllama model
- Gmail account with app password

### Ollama Setup

1. **Install Ollama:**
   - Download and install Ollama from https://ollama.ai/

2. **Pull the TinyLlama model:**
   ```bash
   ollama pull tinyllama
   ```

3. **Verify installation:**
   ```bash
   ollama list
   ```
   You should see `tinyllama` in the list.

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your settings:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
   
   # Database
   # Using SQLite by default
   
   # Ollama
   OLLAMA_MODEL=tinyllama
   
   # Gmail
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-specific-password
   
   # IMAP
   IMAP_USERNAME=your-email@gmail.com
   IMAP_PASSWORD=your-app-specific-password
   ```

6. **Start Ollama server:**
   ```bash
   ollama serve
   ```
   Keep this running in a separate terminal.

7. **Start backend server:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
   Backend API available at: `http://localhost:8000/api`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm start
   ```
   Frontend available at: `http://localhost:4200`

---

## 🧪 Testing the System

### 1. Create RFP from Natural Language
- Go to RFPs tab → Click "✨ From Text"
- Enter: "I need to buy 50 laptops with 16GB RAM, budget $100k, delivery in 30 days"
- AI will create structured RFP

### 2. Send RFP to Vendors
- Select vendors from the list
- Click "Send to Vendors" 
- System generates professional email and sends via Gmail

### 3. Receive & Parse Proposals
- Vendors reply to the email
- Click "Check for Emails" in Proposals tab
- System automatically parses proposal content using AI

### 4. Compare & Evaluate
- Select RFP and click "Evaluate Proposals"
- AI compares all proposals and provides recommendation

---

## 🔧 Configuration

### Environment Variables

Create `.env` file in backend directory:

```env
DEBUG=True
SECRET_KEY=your-django-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Ollama
OLLAMA_MODEL=tinyllama

# Email (Gmail)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
IMAP_USERNAME=your-email@gmail.com
IMAP_PASSWORD=your-app-password
```

### Gmail Setup

1. Enable 2FA on Gmail account
2. Generate App Password: https://support.google.com/accounts/answer/185833
3. Use app password in EMAIL_HOST_PASSWORD and IMAP_PASSWORD

---

## 📊 System Features

✅ **Natural Language RFP Creation** - AI parses procurement needs into structured RFPs  
✅ **Vendor Management** - CRUD operations for vendor database  
✅ **Email Integration** - Send RFPs and receive proposals via Gmail  
✅ **AI Proposal Parsing** - Automatically extract price, terms, specs from emails  
✅ **Intelligent Comparison** - Score and rank proposals against requirements  
✅ **Recommendation Engine** - AI suggests best vendor with rationale  

---

## 🚀 Deployment

For production deployment:

1. Use PostgreSQL instead of SQLite
2. Configure proper email service (SendGrid, AWS SES)
3. Set up Ollama server separately
4. Use Docker containers
5. Configure HTTPS and security settings

---

## 📱 Features & Workflows

### 1️⃣ Create RFPs from Natural Language

**User Flow:**
1. Click "✨ From Text" button in RFPs tab
2. Enter natural language description: "We need 100 laptops with 16GB RAM, $150k budget, 60-day delivery"
3. AI parses and extracts:
   - Title: "Laptop Procurement"
   - Requirements: Items, quantities, specifications
   - Budget: $150,000
   - Deadline: ~60 days from now
   - Payment terms, warranty expectations
4. RFP created with status: **DRAFT**

**Technical Flow:**
```
User Input → Frontend /rfps/create-from-natural-language/ → 
Ollama TinyLlama → AIService.parse_natural_language_to_rfp() → 
RFP Model created → Response back to Frontend
```

**API Endpoint:**
```
POST /api/rfps/create-from-natural-language/
Request: { "description": "natural language text" }
Response: { id, title, requirements, budget, deadline, status: "DRAFT", ... }
```

### 2️⃣ Manage Vendors & Send RFPs

**Vendor Management:**
- Create vendors with: name, email, contact person, phone, address, website
- View all vendors in grid format
- Update vendor information
- Delete vendors
- Toggle active/inactive status

**Send RFP to Vendors:**
1. Click "Send" button on any RFP
2. Vendor selection checkboxes appear
3. Select 1 or more vendors
4. Click "Send to Selected Vendors"
5. System sends professional RFP email via Gmail SMTP
6. RFP status changes to: **SENT**
7. "Send" button becomes disabled

**Technical Flow:**
```
Frontend selection → POST /api/rfps/{id}/send-to-vendors/ →
EmailService.send_rfp_to_vendor() → Gmail SMTP →
RFP status updated to "SENT" → Response with success message
```

**API Endpoints:**
```
GET    /api/vendors/                    List vendors
POST   /api/vendors/                    Create vendor
PUT    /api/vendors/{id}/               Update vendor
DELETE /api/vendors/{id}/               Delete vendor
POST   /api/rfps/{id}/send-to-vendors/  Send to vendors
```

### 3️⃣ Receive & Parse Proposals

**Email Reception:**
1. Vendors reply to RFP email with proposals
2. Click "📧 Check for Incoming Proposals" button
3. System connects to Gmail IMAP
4. Downloads emails from inbox
5. Matches vendors by email address
6. Creates Proposal records with status: **RECEIVED**

**Proposal Parsing:**
1. Received proposals appear in list with "Parse" button
2. Click "Parse" to extract proposal data with AI
3. OpenAI extracts:
   - Price/Cost
   - Delivery timeline
   - Warranty period
   - Payment terms
   - Specifications & capabilities
4. Status changes to: **PARSED**
5. Parsed data stored as JSON in database

**Technical Flow:**
```
Email reply → Check Emails → EmailService.receive_proposal_emails() →
IMAP Gmail download → Proposal created (RECEIVED) →
Click Parse → AIService.parse_proposal() → OpenAI extracts →
Status → PARSED, parsed_data stored
```

**API Endpoints:**
```
POST /api/email/check-proposals/       Check for incoming emails
POST /api/proposals/{id}/parse/        Parse proposal with AI
```

### 4️⃣ Compare Proposals & Get AI Recommendation

**Evaluation Process:**
1. Ensure you have 2+ proposals in **PARSED** status for same RFP
2. Go to Proposals tab
3. Select RFP from dropdown
4. Click "Compare & Evaluate"
5. AI analyzes all proposals against RFP requirements
6. System generates scores and recommendation

**Results Display:**
- **Summary:** Executive summary of all proposals
- **🏆 Recommendation:** Which vendor wins and why
- **Detailed Scores:** For each vendor:
  - Overall Score (0-100)
  - Compliance Score (0-100)
  - Price Competitiveness (0-100)
  - Risk Assessment
- **Visual Progress Bars:** Easy comparison at a glance

**Scoring Algorithm:**
- Compliance Score: How well proposal meets RFP requirements
- Price Score: How competitive pricing is vs budget
- Overall Score: Combined weighted score
- Risk Assessment: Delivery risks, warranty gaps, payment term concerns

**Technical Flow:**
```
Select RFP → POST /api/proposals/compare-and-evaluate/ →
AIService.evaluate_proposals() → OpenAI multi-proposal comparison →
Scores + Risk Assessment + Recommendation → 
Results card with visual display
```

**API Endpoint:**
```
POST /api/proposals/compare-and-evaluate/
Request: { "rfp_id": "rfp_id" }
Response: {
  evaluations: {
    "vendor_name": {
      compliance_score: 90,
      price_competitiveness: 85,
      score: 88,
      risk_assessment: "..."
    }
  },
  summary: "...",
  recommendation: "Award to Vendor X because..."
}
```

---

## 📊 Database Models

### Vendor Model
```python
- name: CharField (255)
- email: EmailField
- contact_person: CharField
- phone: CharField
- address: TextField
- city: CharField
- country: CharField
- website: URLField
- notes: TextField
- active: Boolean (default=True)
- created_at: DateTime (auto)
- updated_at: DateTime (auto)
```

### RFP Model
```python
- title: CharField (255)
- description: TextField
- requirements: JSONField (structured)
- budget: DecimalField
- deadline: DateTime
- status: CharField (DRAFT, SENT, CLOSED, AWARDED)
- selected_vendors: JSONField (list of IDs)
- awarded_vendor: CharField
- natural_language_input: TextField
- created_at: DateTime (auto)
- updated_at: DateTime (auto)
```

### Proposal Model
```python
- rfp_id: CharField
- vendor_id: CharField
- vendor_name: CharField
- proposal_content: TextField (raw email text)
- parsed_data: JSONField (AI-extracted data)
- price: DecimalField
- delivery_time: CharField
- warranty: CharField
- payment_terms: CharField
- score: FloatField
- evaluation: JSONField
- status: CharField (RECEIVED, PARSED, EVALUATED)
- email_message_id: CharField
- received_at: DateTime (auto)
- updated_at: DateTime (auto)
```

---

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database
MONGODB_URI=mongodb://localhost:27017/rfp_management

# OpenAI
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo

# Email (Gmail SMTP)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# IMAP (Gmail for receiving)
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
IMAP_USERNAME=your-email@gmail.com
IMAP_PASSWORD=your-app-password

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:4200
```

### Gmail Setup

**To enable Gmail integration:**

1. **Enable 2-Factor Authentication** in Gmail account
2. **Generate App Password:**
   - Go to Google Account → Security
   - App passwords → Select Mail and Windows Device
   - Copy the 16-character password
   - Use this as `EMAIL_HOST_PASSWORD` and `IMAP_PASSWORD`

### CORS Configuration

Backend (`settings.py`) allows requests from:
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',
    'http://127.0.0.1:4200',
]
```

---

## 🧪 Testing Workflows

### Test 1: Natural Language RFP Creation
```
1. Start frontend: npm start (http://localhost:4200)
2. Go to "RFPs" tab
3. Click "✨ From Text" button
4. Enter: "We need 50 units of industrial equipment, budget $200,000, 90-day delivery, need 5-year warranty"
5. Click "Create RFP from Text"
6. ✅ Verify: RFP appears with extracted title, budget, deadline, requirements
7. ✅ Status shows: "DRAFT"
```

### Test 2: Vendor Management & RFP Distribution
```
1. Go to "Vendors" tab
2. Click "Add Vendor"
3. Enter vendor details (name, email, contact, phone)
4. Click "Create"
5. ✅ Vendor appears in list
6. Go to "RFPs" tab
7. Click "Send" on an RFP
8. Check vendor checkbox
9. Click "Send to Selected Vendors"
10. ✅ Verify: RFP status → "SENT"
11. ✅ Check vendor email: Should receive professional RFP email
```

### Test 3: Email Reception & Parsing
```
1. Have vendor reply to RFP email with proposal
2. Go to "Proposals" tab
3. Click "📧 Check for Incoming Proposals"
4. ✅ Proposal appears with status "RECEIVED"
5. Click "Parse" button
6. ✅ Verify: Status → "PARSED"
7. ✅ Verify: parsed_data shows price, delivery time, warranty, payment terms
```

### Test 4: Proposal Comparison
```
1. Get 2-3 proposals in "PARSED" status for same RFP
2. Go to "Proposals" tab
3. Select RFP from dropdown
4. Click "Compare & Evaluate"
5. ✅ Evaluation card appears
6. ✅ Summary paragraph visible
7. ✅ 🏆 Recommendation shows with rationale
8. ✅ All vendors listed with scores:
   - Compliance (0-100)
   - Price Competitiveness (0-100)
   - Overall Score (0-100)
   - Risk Assessment
9. ✅ Visual progress bars showing comparison
```

---

## 📡 API Reference

### Base URL
```
http://localhost:8000/api
```

### RFP Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/rfps/create-from-natural-language/` | Create RFP from text |
| GET | `/rfps/` | List all RFPs |
| POST | `/rfps/` | Create RFP manually |
| GET | `/rfps/{id}/` | Get RFP details |
| PUT | `/rfps/{id}/` | Update RFP |
| DELETE | `/rfps/{id}/` | Delete RFP |
| POST | `/rfps/{id}/send-to-vendors/` | Send to vendors |
| POST | `/rfps/{id}/award/` | Award to vendor |

### Vendor Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/vendors/` | List all vendors |
| POST | `/vendors/` | Create vendor |
| GET | `/vendors/{id}/` | Get vendor details |
| PUT | `/vendors/{id}/` | Update vendor |
| DELETE | `/vendors/{id}/` | Delete vendor |
| GET | `/vendors/active/` | List active vendors |
| POST | `/vendors/{id}/toggle-active/` | Toggle active status |

### Proposal Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/proposals/` | List all proposals |
| GET | `/proposals/{id}/` | Get proposal details |
| POST | `/proposals/{id}/parse/` | Parse with AI |
| POST | `/proposals/compare-and-evaluate/` | Compare proposals |

### Email Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/email/check-proposals/` | Check for new emails |

---

## 🐛 Troubleshooting

### Issue: "Cannot GET /api/vendors"
**Solution:** Ensure backend is running on port 8000
```bash
cd backend
python manage.py runserver 0.0.0.0:8000
```

### Issue: CORS errors in frontend
**Solution:** Check CORS configuration in `backend/settings.py`
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',
    'http://127.0.0.1:4200',
]
```

### Issue: OpenAI API errors
**Solution:** Verify OPENAI_API_KEY and OPENAI_MODEL in `.env`
```
OPENAI_API_KEY=sk-your-full-key
OPENAI_MODEL=gpt-4-turbo
```

### Issue: Emails not being received
**Solution:** Verify IMAP settings and app password in `.env`
```
IMAP_USERNAME=your-email@gmail.com
IMAP_PASSWORD=16-character-app-password
```

### Issue: Cannot parse proposal content
**Solution:** Ensure OpenAI API is configured and has sufficient quota

---

## 🔐 Security Notes

1. **Never commit .env file** - Use `.env.example` as template
2. **API Keys:** Store securely in environment variables
3. **Gmail Password:** Use app-specific password, not account password
4. **CORS:** Configure only for trusted origins in production
5. **HTTPS:** Always use HTTPS in production
6. **Input Validation:** All endpoints validate input data

---

## 📈 Performance Considerations

- **Frontend Bundle:** ~260 KB (compressed: ~70 KB)
- **API Response Time:** <500ms typical
- **OpenAI Processing:** 2-5 seconds per request
- **Email Checking:** 5-10 seconds (depends on inbox size)

---

## 🚀 Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in .env
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` for your domain
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure HTTPS
- [ ] Set up proper email credentials
- [ ] Configure monitoring and logging
- [ ] Use production OpenAI API key
- [ ] Set up regular backups

### Deploy to Production

```bash
# Backend
pip install -r requirements.txt
python manage.py migrate --settings=rfp_management.settings_production
gunicorn rfp_management.wsgi

# Frontend
npm run build
Deploy dist/ folder to web server
```

---

## 📝 Notes

- All timestamps are in UTC
- RFP statuses: DRAFT → SENT → CLOSED/AWARDED
- Proposal statuses: RECEIVED → PARSED → EVALUATED
- AI uses GPT-4-turbo for all natural language processing
- Email checking is manual (click button) - can be automated with background tasks

---

## 🤝 Support

For issues or questions:
1. Check backend logs: `python manage.py runserver`
2. Check frontend console: Browser DevTools (F12)
3. Verify all environment variables in `.env`
4. Test API directly: `curl http://localhost:8000/api/vendors/`
5. Check database: `python manage.py shell`

---

**Last Updated:** January 14, 2026  
**Status:** Production Ready  
**Version:** 1.0.0