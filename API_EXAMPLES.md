# API Examples & Recipes

## Complete Workflow Example

### 1. Create Vendor

```bash
curl -X POST http://localhost:8000/api/vendors/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Corp",
    "email": "contact@acme.com",
    "contact_person": "Bob Wilson",
    "phone": "555-1234",
    "city": "Seattle",
    "country": "USA",
    "active": true
  }'
```

Response:
```json
{
  "id": "507f1f77bcf86cd799439011",
  "name": "Acme Corp",
  "email": "contact@acme.com",
  "contact_person": "Bob Wilson",
  "phone": "555-1234",
  "active": true,
  "created_at": "2024-01-13T10:30:00Z"
}
```

### 2. Create RFP from Natural Language

```bash
curl -X POST http://localhost:8000/api/rfps/create_from_natural_language/ \
  -H "Content-Type: application/json" \
  -d '{
    "description": "We need to procure 50 office chairs and 25 desks for our new facility. Budget is $25,000. Delivery needed within 2 weeks. Colors should be ergonomic black or gray. We need 1-year warranty and 30-day payment terms."
  }'
```

Response:
```json
{
  "id": "507f1f77bcf86cd799439012",
  "title": "Office Furniture Procurement",
  "description": "We need to procure 50 office chairs...",
  "requirements": {
    "items": [
      {
        "name": "Office Chairs",
        "quantity": 50,
        "specifications": "Ergonomic, black or gray"
      },
      {
        "name": "Desks",
        "quantity": 25,
        "specifications": "Standard office desks"
      }
    ],
    "delivery_timeline": "within 2 weeks",
    "payment_terms": "30-day payment terms",
    "warranty": "1-year warranty",
    "budget": 25000
  },
  "budget": 25000,
  "deadline": "2024-01-27T10:30:00Z",
  "status": "DRAFT",
  "selected_vendors": [],
  "natural_language_input": "..."
}
```

### 3. Send RFP to Vendors

```bash
curl -X POST http://localhost:8000/api/rfps/507f1f77bcf86cd799439012/send_to_vendors/ \
  -H "Content-Type: application/json" \
  -d '{
    "vendor_ids": [
      "507f1f77bcf86cd799439011",
      "507f1f77bcf86cd799439013"
    ]
  }'
```

Response:
```json
{
  "message": "RFP sent to vendors",
  "rfp": {
    "id": "507f1f77bcf86cd799439012",
    "status": "SENT",
    "selected_vendors": ["507f1f77bcf86cd799439011", "507f1f77bcf86cd799439013"]
  }
}
```

### 4. Receive Vendor Proposals

Vendor receives email and replies with:
```
Subject: RE: Request for Proposal: Office Furniture Procurement

Dear Procurement Team,

Thank you for the RFP. We are pleased to submit our proposal:

OFFICE CHAIRS:
- Unit Price: $180 per chair
- Total: $9,000 (50 chairs)
- Delivery: 10 days
- Warranty: 2 years

DESKS:
- Unit Price: $320 per desk
- Total: $8,000 (25 desks)
- Delivery: 10 days
- Warranty: 18 months

Total Price: $17,000
Payment Terms: Net 45
Colors Available: Black, Gray, White
Special: Free shipping and installation

Best regards,
Acme Corp Sales Team
```

### 5. Import Proposals from Email

```bash
curl -X POST http://localhost:8000/api/email/check-proposals/ \
  -H "Content-Type: application/json" \
  -d '{}'
```

Response:
```json
{
  "message": "Checked 2 emails",
  "proposals_received": [
    {
      "id": "507f1f77bcf86cd799439014",
      "vendor": "Acme Corp",
      "rfp_id": "507f1f77bcf86cd799439012",
      "subject": "RE: Request for Proposal: Office Furniture Procurement"
    }
  ]
}
```

### 6. Retrieve Proposals

```bash
curl "http://localhost:8000/api/proposals/?rfp_id=507f1f77bcf86cd799439012"
```

Response:
```json
[
  {
    "id": "507f1f77bcf86cd799439014",
    "rfp_id": "507f1f77bcf86cd799439012",
    "vendor_id": "507f1f77bcf86cd799439011",
    "vendor_name": "Acme Corp",
    "proposal_content": "Dear Procurement Team...",
    "parsed_data": {},
    "status": "RECEIVED"
  }
]
```

### 7. Parse Proposal with AI

```bash
curl -X POST http://localhost:8000/api/proposals/507f1f77bcf86cd799439014/parse/ \
  -H "Content-Type: application/json" \
  -d '{}'
```

Response:
```json
{
  "id": "507f1f77bcf86cd799439014",
  "vendor_name": "Acme Corp",
  "price": 17000,
  "delivery_time": "10 days",
  "warranty": "2 years for chairs, 18 months for desks",
  "payment_terms": "Net 45",
  "parsed_data": {
    "items": [
      {
        "name": "Office Chairs",
        "unit_price": 180,
        "total": 9000,
        "quantity": 50
      },
      {
        "name": "Desks",
        "unit_price": 320,
        "total": 8000,
        "quantity": 25
      }
    ],
    "additional_services": "Free shipping and installation"
  },
  "status": "PARSED"
}
```

### 8. Compare & Evaluate Proposals

```bash
curl -X POST http://localhost:8000/api/proposals/compare_and_evaluate/ \
  -H "Content-Type: application/json" \
  -d '{"rfp_id": "507f1f77bcf86cd799439012"}'
```

Response:
```json
{
  "summary": "We received 2 qualified proposals. Acme Corp offers the best value at $17,000 with faster delivery. FurniturePro offers more comprehensive warranty coverage.",
  "recommendation": "We recommend Acme Corp as they meet all requirements within budget, offer faster delivery (10 days vs 14 days), and provide competitive pricing with adequate warranty terms. Their free installation service adds additional value.",
  "proposals": [
    {
      "id": "507f1f77bcf86cd799439014",
      "vendor_name": "Acme Corp",
      "price": 17000,
      "delivery_time": "10 days",
      "warranty": "2 years",
      "score": 92,
      "evaluation": {
        "compliance_score": 95,
        "price_competitiveness": 94,
        "delivery_score": 90,
        "warranty_score": 85,
        "risk_assessment": "Low risk - established vendor",
        "notes": "Best overall value with free installation"
      },
      "status": "EVALUATED"
    },
    {
      "id": "507f1f77bcf86cd799439015",
      "vendor_name": "FurniturePro",
      "price": 19500,
      "delivery_time": "14 days",
      "warranty": "3 years",
      "score": 85,
      "evaluation": {
        "compliance_score": 92,
        "price_competitiveness": 75,
        "delivery_score": 80,
        "warranty_score": 95,
        "risk_assessment": "Low risk - good reputation",
        "notes": "Higher cost but better warranty coverage"
      },
      "status": "EVALUATED"
    }
  ]
}
```

### 9. Award RFP

```bash
curl -X POST http://localhost:8000/api/rfps/507f1f77bcf86cd799439012/award/ \
  -H "Content-Type: application/json" \
  -d '{"vendor_id": "507f1f77bcf86cd799439011"}'
```

Response:
```json
{
  "id": "507f1f77bcf86cd799439012",
  "title": "Office Furniture Procurement",
  "status": "AWARDED",
  "awarded_vendor": "507f1f77bcf86cd799439011"
}
```

### 10. Close RFP

```bash
curl -X POST http://localhost:8000/api/rfps/507f1f77bcf86cd799439012/close/ \
  -H "Content-Type: application/json" \
  -d '{}'
```

Response:
```json
{
  "id": "507f1f77bcf86cd799439012",
  "status": "CLOSED"
}
```

## Python Client Example

```python
import requests
import json

BASE_URL = "http://localhost:8000/api"

class RFPClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
    
    def create_vendor(self, name, email, contact_person=""):
        """Create a new vendor"""
        data = {
            "name": name,
            "email": email,
            "contact_person": contact_person,
            "active": True
        }
        response = requests.post(f"{self.base_url}/vendors/", json=data)
        return response.json()
    
    def create_rfp(self, description):
        """Create RFP from natural language"""
        data = {"description": description}
        response = requests.post(
            f"{self.base_url}/rfps/create_from_natural_language/",
            json=data
        )
        return response.json()
    
    def send_rfp_to_vendors(self, rfp_id, vendor_ids):
        """Send RFP to vendors"""
        data = {"vendor_ids": vendor_ids}
        response = requests.post(
            f"{self.base_url}/rfps/{rfp_id}/send_to_vendors/",
            json=data
        )
        return response.json()
    
    def check_emails(self):
        """Check for proposal emails"""
        response = requests.post(
            f"{self.base_url}/email/check-proposals/",
            json={}
        )
        return response.json()
    
    def compare_proposals(self, rfp_id):
        """Evaluate proposals"""
        data = {"rfp_id": rfp_id}
        response = requests.post(
            f"{self.base_url}/proposals/compare_and_evaluate/",
            json=data
        )
        return response.json()

# Usage
client = RFPClient()

# Create vendor
vendor = client.create_vendor("Tech Corp", "sales@techcorp.com")
print(vendor)

# Create RFP
rfp = client.create_rfp("Need 20 laptops with 16GB RAM, $30,000 budget")
print(rfp)
```

## Postman Collection

Import this into Postman as a collection:

```json
{
  "info": {
    "name": "RFP Management API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Vendors",
      "item": [
        {
          "name": "List Vendors",
          "request": {
            "method": "GET",
            "url": "{{base_url}}/vendors/"
          }
        },
        {
          "name": "Create Vendor",
          "request": {
            "method": "POST",
            "url": "{{base_url}}/vendors/",
            "body": {
              "mode": "raw",
              "raw": "{\"name\": \"New Vendor\", \"email\": \"sales@vendor.com\"}"
            }
          }
        }
      ]
    },
    {
      "name": "RFPs",
      "item": [
        {
          "name": "Create RFP from Text",
          "request": {
            "method": "POST",
            "url": "{{base_url}}/rfps/create_from_natural_language/",
            "body": {
              "mode": "raw",
              "raw": "{\"description\": \"Your procurement need here\"}"
            }
          }
        }
      ]
    }
  ]
}
```

Set the `base_url` variable to `http://localhost:8000/api`.
