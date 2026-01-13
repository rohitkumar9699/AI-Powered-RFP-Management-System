# Development Guide

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Angular Frontend (4200)                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Components: RFP Creation, Vendor Management,        │   │
│  │ Proposal Comparison, Dashboard                      │   │
│  └──────────────────┬──────────────────────────────────┘   │
└─────────────────────┼───────────────────────────────────────┘
                      │ HTTP/REST
                      ▼
┌─────────────────────────────────────────────────────────────┐
│             Django REST API Backend (8000)                  │
│  ┌───────────┬──────────┬───────────┬─────────┬────────┐   │
│  │ Vendors   │  RFPs    │ Proposals │   AI    │ Email  │   │
│  │ App       │  App     │  App      │  App    │ App    │   │
│  └───────────┴──────────┴───────────┴─────────┴────────┘   │
│                      │                                      │
│  ┌──────────────────┴────────────────────┐                 │
│  │                                       │                 │
│  ▼                                       ▼                 │
│  OpenAI API (GPT-4)                   Email (SMTP/IMAP)  │
│  - RFP Parsing                        - Send RFPs        │
│  - Proposal Parsing                   - Receive Responses│
│  - Proposal Evaluation                                   │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
            ┌──────────────────┐
            │  MongoDB Atlas   │
            │  - Vendors       │
            │  - RFPs          │
            │  - Proposals     │
            └──────────────────┘
```

## Project Layout

```
backend/
├── rfp_management/              # Django project
│   ├── settings.py              # Configuration
│   ├── urls.py                  # URL routing
│   ├── wsgi.py                  # WSGI app
│   └── apps/
│       ├── vendors/             # Vendor CRUD
│       │   ├── models.py        # Vendor model
│       │   ├── views.py         # REST endpoints
│       │   ├── serializers.py   # Request/response
│       │   └── urls.py          # Routes
│       ├── rfps/                # RFP management
│       │   ├── models.py        # RFP model
│       │   ├── views.py         # RFP endpoints
│       │   └── ...
│       ├── proposals/           # Proposal handling
│       │   ├── models.py        # Proposal model
│       │   ├── views.py         # Comparison endpoints
│       │   └── ...
│       ├── ai/                  # AI service
│       │   ├── services.py      # OpenAI integration
│       │   ├── views.py         # AI endpoints
│       │   └── ...
│       └── email_service/       # Email handling
│           ├── services.py      # SMTP/IMAP logic
│           ├── views.py         # Email endpoints
│           └── ...
├── manage.py                    # Django CLI
└── requirements.txt             # Python dependencies

frontend/
├── src/
│   ├── app/
│   │   ├── app.component.ts     # Main component
│   │   ├── services/
│   │   │   └── api.service.ts   # HTTP client
│   │   ├── components/          # UI components
│   │   └── models/              # Interfaces
│   ├── main.ts                  # Bootstrap
│   └── styles.scss              # Global styles
├── package.json                 # Dependencies
└── angular.json                 # Config
```

## Key Concepts

### 1. RFP Lifecycle

```
DRAFT
  ↓ (User selects vendors)
SENT (RFP emailed to vendors)
  ↓ (Vendors reply)
CLOSED/AWARDED
  ↓ (RFP completed)
```

### 2. Proposal Status

```
RECEIVED (from email)
  ↓ (AI parsing)
PARSED (extracted data)
  ↓ (User initiates comparison)
EVALUATED (scored against RFP)
```

### 3. AI Integration Points

```
NLP Parsing:   Text → Structured JSON
Proposal:      Email → Extracted fields
Evaluation:    Multiple proposals → Scores + Recommendation
```

## Common Development Tasks

### Add a New Field to RFP

1. **Update Model** (backend/rfp_management/apps/rfps/models.py)
```python
class RFP(models.Model):
    new_field = models.CharField(max_length=255)  # Add here
```

2. **Update Serializer**
```python
class RFPSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [..., 'new_field']  # Add here
```

3. **Run Migration**
```bash
python manage.py makemigrations
python manage.py migrate
```

### Add a New API Endpoint

1. **Add View Method** (views.py)
```python
@action(detail=False, methods=['post'])
def my_action(self, request):
    return Response({'result': 'success'})
```

2. **URL Routing** (urls.py)
```python
# Automatically registered by router
```

### Call API from Frontend

```typescript
// api.service.ts
myAction(): Observable<any> {
  return this.http.post(`${this.apiUrl}/rfps/my_action/`, {});
}

// component.ts
this.apiService.myAction().subscribe(
  (result) => console.log(result),
  (error) => console.error(error)
);
```

## Testing

### Backend Unit Tests
```bash
python manage.py test rfp_management
python manage.py test rfp_management.apps.vendors
```

### Backend API Testing
```bash
# Using Postman or curl
curl http://localhost:8000/api/vendors/
```

### Frontend Testing
```bash
ng test
ng test --watch
```

## Debugging

### Backend
```bash
# Django shell
python manage.py shell
from rfp_management.apps.vendors.models import Vendor
Vendor.objects.all()

# Check logs
tail -f *.log
```

### Frontend
- Chrome DevTools (F12)
- Network tab for API calls
- Console for errors

### AI Integration
```python
# Test OpenAI directly
from rfp_management.apps.ai.services import AIService
ai = AIService()
result = ai.parse_natural_language("Your description")
print(result)
```

## Performance Tips

### Database
- Use `.select_related()` for foreign keys
- Use `.prefetch_related()` for many-to-many
- Add indexes for frequently queried fields

### API
- Use pagination for large lists
- Cache AI responses when appropriate
- Compress responses with gzip

### Frontend
- Lazy load components
- Use OnPush change detection
- Minimize API calls

## Security Considerations

### API
- Validate all inputs
- Rate limiting on endpoints
- CORS properly configured
- No sensitive data in logs

### Email
- Store passwords in environment variables
- Use app-specific passwords
- Validate sender emails

### Database
- Connection pooling
- Backup regularly
- Use SSL/TLS for connections

## Deployment Checklist

- [ ] Set DEBUG=False
- [ ] Update SECRET_KEY
- [ ] Configure allowed hosts
- [ ] Set up HTTPS
- [ ] Configure database backups
- [ ] Set up monitoring
- [ ] Configure logging
- [ ] Add authentication
- [ ] Enable rate limiting
- [ ] Test in staging

## Useful Commands

```bash
# Backend
python manage.py runserver 0.0.0.0:8000
python manage.py createsuperuser
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
python manage.py shell

# Frontend
ng serve
ng build
ng build --prod
ng test
ng lint
```

## Resources

- [Django Docs](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Angular Docs](https://angular.io/docs)
- [OpenAI API](https://platform.openai.com/docs)
- [MongoDB](https://docs.mongodb.com/)
