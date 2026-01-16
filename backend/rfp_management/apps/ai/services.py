"""AI Services - Integration with Ollama for NLP tasks"""
import os
import json
from datetime import datetime, timedelta
import ollama
import re


class AIService:
    """Service for AI-powered tasks using Ollama"""

    def __init__(self):
        """Initialize Ollama client"""
        self.model = os.getenv('OLLAMA_MODEL', 'tinyllama')

    def parse_natural_language_to_rfp(self, natural_language_input: str) -> dict:
        """
        Parse natural language input into structured RFP data.
        
        Args:
            natural_language_input: User's description of procurement needs
            
        Returns:
            dict: Structured RFP with title, requirements, budget, deadline
        """
        prompt = f"""
You are an expert procurement manager. Convert the following natural language procurement need into a structured RFP format.

User Input:
{natural_language_input}

Please extract and structure the following information:
1. Title: A concise title for the RFP
2. Requirements: A detailed breakdown of what's needed (items, quantities, specifications)
3. Budget: Total budget allocated (if mentioned)
4. Deadline: Delivery/completion deadline (if mentioned)
5. Payment Terms: Payment terms specified
6. Warranty/Support: Any warranty or support requirements

Return ONLY a valid JSON object with this exact structure:
{{
    "title": "RFP Title",
    "requirements": {{
        "items": [
            {{"name": "laptop", "quantity": 50, "specifications": "16GB RAM"}}
        ],
        "delivery_timeline": "30 days",
        "payment_terms": "net 30",
        "warranty": "1 year"
    }},
    "budget": 100000,
    "deadline": "2026-02-15"
}}

Do not add extra fields or explanations. Just the JSON.
"""

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert RFP analyst. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = response['message']['content'].strip()
            
            # Remove any prefix like "JSON Response:" 
            if '{' in response_text:
                start_idx = response_text.find('{')
                response_text = response_text[start_idx:]
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                rfp_data = json.loads(json_match.group())
            else:
                rfp_data = json.loads(response_text)
            
            # Ensure deadline is in correct format
            if rfp_data.get('deadline') and rfp_data['deadline'] != 'null':
                try:
                    deadline_obj = datetime.strptime(rfp_data['deadline'], '%Y-%m-%d')
                    rfp_data['deadline'] = deadline_obj.isoformat()
                except:
                    rfp_data['deadline'] = (datetime.now() + timedelta(days=30)).isoformat()
            else:
                rfp_data['deadline'] = (datetime.now() + timedelta(days=30)).isoformat()

            return rfp_data

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse AI response as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Error parsing natural language to RFP: {str(e)}")

    def parse_proposal(self, proposal_content: str) -> dict:
        """
        Parse vendor proposal email/content into structured data.
        
        Args:
            proposal_content: Raw email body or proposal text
            
        Returns:
            dict: Structured proposal data with price, delivery, warranty, etc.
        """
        prompt = f"""
You are an expert at parsing vendor proposals. Extract key information from the following vendor proposal:

Proposal Content:
{proposal_content}

Extract the following information if available:
1. Price/Cost (exact number, or estimated range)
2. Delivery Time (days, weeks, or specific date)
3. Warranty Period
4. Payment Terms
5. Key Features/Specifications Offered
6. Any special conditions or notes

Return ONLY a valid JSON object with this structure:
{{
    "price": null or number,
    "price_currency": "USD" or detected currency,
    "delivery_time": "string describing timeline",
    "warranty": "warranty details",
    "payment_terms": "payment terms",
    "specifications": {{"key": "value", ...}},
    "special_conditions": "any special notes"
}}
"""

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert proposal parser. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = response['message']['content'].strip()
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                proposal_data = json.loads(json_match.group())
            else:
                proposal_data = json.loads(response_text)

            return proposal_data

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse proposal as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Error parsing proposal: {str(e)}")

    def evaluate_proposals(self, rfp_requirements: dict, proposals: list) -> dict:
        """
        Evaluate multiple proposals against RFP requirements and provide recommendations.
        
        Args:
            rfp_requirements: The original RFP requirements
            proposals: List of parsed proposals from vendors
            
        Returns:
            dict: Evaluation with scores, summary, and recommendation
        """
        proposals_json = json.dumps(proposals, indent=2, default=str)
        requirements_json = json.dumps(rfp_requirements, indent=2, default=str)

        prompt = f"""
You are an expert procurement evaluator. Compare the following vendor proposals against the RFP requirements.

RFP Requirements:
{requirements_json}

Vendor Proposals:
{proposals_json}

For each proposal, provide:
1. Compliance Score (0-100): How well does it meet requirements?
2. Price Competitiveness Score (0-100): How competitive is the pricing?
3. Risk Assessment: Any risks or concerns?
4. Overall Score (0-100): Combined evaluation

Then provide:
5. Summary: Brief overview of all proposals
6. Recommendation: Which vendor to award, and why?

Return ONLY a valid JSON object with this structure:
{{
    "evaluations": {{
        "vendor_name_1": {{
            "compliance_score": number,
            "price_competitiveness": number,
            "risk_assessment": "string",
            "score": number,
            "notes": "string"
        }},
        ...
    }},
    "summary": "Overall summary of proposals",
    "recommendation": "Recommended vendor and rationale"
}}
"""

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert procurement evaluator. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = response['message']['content'].strip()
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                evaluation_data = json.loads(json_match.group())
            else:
                evaluation_data = json.loads(response_text)

            return evaluation_data

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse evaluation as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Error evaluating proposals: {str(e)}")

    def generate_rfp_email_body(self, rfp_title: str, rfp_requirements: dict) -> str:
        """
        Generate a professional RFP email body from structured RFP data.
        
        Args:
            rfp_title: Title of the RFP
            rfp_requirements: Structured requirements dict
            
        Returns:
            str: Formatted email body
        """
        requirements_json = json.dumps(rfp_requirements, indent=2, default=str)

        prompt = f"""
Generate a professional, clear, and concise RFP email to be sent to vendors.

RFP Title: {rfp_title}

Requirements:
{requirements_json}

The email should:
1. Briefly introduce the procurement need
2. List key requirements clearly
3. Include budget and timeline if available
4. Request specific information in the response
5. Include contact information placeholder
6. Be professional and clear

Return ONLY the email body text, no subject line.
"""

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at writing professional RFP emails."},
                    {"role": "user", "content": prompt}
                ]
            )

            return response['message']['content'].strip()

        except Exception as e:
            raise Exception(f"Error generating RFP email: {str(e)}")
