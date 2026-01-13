# Quick Start Guide

## 5-Minute Setup

### Prerequisites
- Python 3.9+, Node.js 18+, MongoDB
- OpenAI API key from https://platform.openai.com/api-keys
- Gmail or other email with SMTP/IMAP enabled

### 1. Backend Setup (2 min)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env with your credentials:
# - OPENAI_API_KEY=sk-your-key
# - EMAIL_HOST_USER=your-email@gmail.com
# - EMAIL_HOST_PASSWORD=your-app-password

python manage.py migrate
python manage.py runserver
```
✓ Backend running on http://localhost:8000

### 2. Frontend Setup (2 min)

```bash
cd frontend
npm install
npm start
```
✓ Frontend running on http://localhost:4200

### 3. Add Sample Vendors (1 min)

```bash
cd backend
python manage.py seed_vendors
```

## Try It Now

### Create an RFP
1. Open http://localhost:4200
2. Go to "RFPs" → "Create New"
3. Describe: "I need 20 laptops with 16GB RAM and 10 monitors for $30,000 total"
4. Click "Create" → Watch AI structure it!

### Send to Vendors
1. Select vendors from the list
2. Click "Send RFPs"
3. Check sample vendors' emails receive the RFP

### Receive & Evaluate Proposals
1. In backend terminal:
   ```bash
   python manage.py shell
   from rfp_management.apps.email_service.services import EmailService
   EmailService().receive_proposal_emails()
   ```
2. Go to RFP → "Proposals" → See AI evaluation and scores

## Troubleshooting

| Issue | Solution |
|-------|----------|
| OPENAI_API_KEY error | Check `.env` file is in `/backend` folder |
| CORS error | Ensure backend on 8000, frontend on 4200 |
| MongoDB error | Run `mongod` in another terminal |
| Email not sending | Use Gmail App Password (not regular password) |

## Next Steps

- [ ] Read [README.md](../README.md) for full documentation
- [ ] Explore API endpoints in [API Documentation](../README.md#api-documentation)
- [ ] Check out workflow examples in [Workflow Example](../README.md#workflow-example)
