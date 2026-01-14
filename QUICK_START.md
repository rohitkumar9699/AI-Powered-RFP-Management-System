# Quick Start Guide - AI-Powered RFP Management System

## 🚀 Start in 5 Minutes

### Option 1: Run Frontend Only (Recommended for Testing)

```bash
# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm start

# Open browser to http://localhost:4200
```

The frontend will connect to the backend API at:
```
https://bookish-telegram-9rr4qpgpr9rcx7r-8000.app.github.dev/api
```

### Option 2: Run Both Frontend and Backend Locally

#### Terminal 1: Frontend
```bash
cd frontend
npm install
npm start
# Runs on http://localhost:4200
```

#### Terminal 2: Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
# Runs on http://localhost:8000
```

---

## 📱 What You Can Do

Once running, the application provides:

### Dashboard
- View statistics (vendor count, RFPs, proposals)
- See recent RFPs
- Check top vendors
- Monitor average proposal scores

### Vendors
- ✅ View all vendors
- ✅ Add new vendors
- ✅ Delete vendors
- 🔄 Edit vendors (coming soon)

### RFPs
- ✅ View all RFPs
- ✅ See RFP details (budget, deadline, vendors)
- 🔄 Create RFP (coming soon)
- 🔄 Send to vendors (coming soon)

### Proposals
- ✅ View all vendor proposals
- ✅ See proposal scores and prices
- ✅ Track evaluation status
- ✅ View proposal details

---

## 🔧 System Requirements

### Frontend Only
- Node.js 16+ 
- npm or yarn
- Modern web browser
- Internet connection (to connect to backend API)

### Full Stack (Local)
- Node.js 16+
- Python 3.8+
- PostgreSQL database
- 2GB RAM
- Internet connection (for OpenAI API)

---

## 🎯 Key Features

### ✅ Implemented
- [x] Vendor management interface
- [x] RFP listing and display
- [x] Proposal viewing and scoring
- [x] Dashboard with KPIs
- [x] Responsive Bootstrap design
- [x] API integration
- [x] Real-time data loading

### 🔄 In Progress
- [ ] Natural language RFP creation
- [ ] AI-powered proposal parsing
- [ ] Email integration
- [ ] User authentication

### 🔮 Planned
- [ ] Advanced filtering
- [ ] Report generation
- [ ] Mobile app
- [ ] Dark mode
- [ ] Real-time notifications

---

## 📊 Sample Data

The system comes with sample data:
- **6 Vendors**: TechCorp, DataSystems, CloudFirst, DevOps Experts, SecureNet, Innovation Labs
- **5 RFPs**: Various infrastructure and software requirements
- **5 Proposals**: Responses from vendors with pricing and timeline

---

## 🔗 API Status

```bash
# Test API connection
curl https://bookish-telegram-9rr4qpgpr9rcx7r-8000.app.github.dev/api/vendors/

# Expected response:
{
  "count": 6,
  "next": null,
  "previous": null,
  "results": [...]
}
```

---

## 📂 Important Files

| File | Purpose |
|------|---------|
| `frontend/src/app/components/` | Main UI components |
| `frontend/src/app/services/api.service.ts` | API communication |
| `frontend/src/index.html` | Main HTML entry point |
| `frontend/angular.json` | Angular configuration |
| `frontend/package.json` | Dependencies and scripts |

---

## 🔍 Navigation

Once running, use the top navigation bar to switch between:
1. **Dashboard** - Overview and statistics
2. **RFPs** - Request for Proposals
3. **Vendors** - Vendor management
4. **Proposals** - Vendor responses

---

## ⚠️ Common Issues

### Port 4200 Already in Use
```bash
# Kill the process using port 4200
# Windows: netstat -ano | findstr :4200
# Linux/Mac: lsof -i :4200

# Or use a different port
ng serve --port 4201
```

### API Connection Error
- Check that backend is running
- Verify API URL in `api.service.ts`
- Check browser console for CORS errors
- Ensure backend has CORS enabled

### npm Install Fails
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

---

## 🎓 Learning Path

1. **First**: Run the frontend (`npm start`)
2. **Second**: Explore the dashboard
3. **Third**: Click through vendors and RFPs
4. **Fourth**: Check the code in `src/app/components/`
5. **Fifth**: Read component comments for understanding

---

## 📞 Need Help?

1. Check `frontend/FRONTEND_README.md` for detailed frontend docs
2. Review component comments in code
3. Check API responses in browser Network tab
4. Look for error messages in browser Console

---

## 🎉 You're Ready!

Run `npm start` and start exploring the RFP Management System!

```bash
cd frontend && npm install && npm start
```

Open http://localhost:4200 in your browser and start managing RFPs! 🚀

---

**Last Updated**: January 14, 2026
**Status**: Ready to Run ✅
