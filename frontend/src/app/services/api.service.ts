import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  // Vendor endpoints
  getVendors(): Observable<any> {
    return this.http.get(`${this.apiUrl}/vendors/`);
  }

  getVendor(id: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/vendors/${id}/`);
  }

  createVendor(vendor: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/vendors/`, vendor);
  }

  updateVendor(id: string, vendor: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/vendors/${id}/`, vendor);
  }

  deleteVendor(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/vendors/${id}/`);
  }

  // RFP endpoints
  getRFPs(): Observable<any> {
    return this.http.get(`${this.apiUrl}/rfps/`);
  }

  getRFP(id: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/rfps/${id}/`);
  }

  createRFP(rfp: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/rfps/`, rfp);
  }

  updateRFP(id: string, rfp: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/rfps/${id}/`, rfp);
  }

  deleteRFP(id: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/rfps/${id}/`);
  }

  createRFPFromNaturalLanguage(description: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/rfps/create_from_natural_language/`, { description });
  }

  sendRFPToVendors(rfpId: string, vendorIds: string[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/rfps/${rfpId}/send_to_vendors/`, { vendor_ids: vendorIds });
  }

  awardRFP(rfpId: string, vendorId: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/rfps/${rfpId}/award/`, { vendor_id: vendorId });
  }

  closeRFP(rfpId: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/rfps/${rfpId}/close/`, {});
  }

  // Proposal endpoints
  getProposals(rfpId: string = ''): Observable<any> {
    if (rfpId) {
      return this.http.get(`${this.apiUrl}/proposals/?rfp_id=${rfpId}`);
    }
    return this.http.get(`${this.apiUrl}/proposals/`);
  }

  getProposal(id: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/proposals/${id}/`);
  }

  parseProposal(id: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/proposals/${id}/parse/`, {});
  }

  compareProposals(rfpId: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/proposals/compare_and_evaluate/`, { rfp_id: rfpId });
  }

  // Email endpoints
  checkProposalEmails(): Observable<any> {
    return this.http.post(`${this.apiUrl}/email/check-proposals/`, {});
  }

  sendRFP(rfpId: string, vendorId: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/email/send-rfp/`, { rfp_id: rfpId, vendor_id: vendorId });
  }

  // AI endpoints
  parseNaturalLanguage(description: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/ai/parse-natural-language/`, { description });
  }

  parseProposalContent(content: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/ai/parse-proposal/`, { proposal_content: content });
  }

  evaluateProposals(rfpRequirements: any, proposals: any[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/ai/evaluate-proposals/`, { 
      rfp_requirements: rfpRequirements, 
      proposals 
    });
  }
}
