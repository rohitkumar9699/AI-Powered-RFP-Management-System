import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-proposals',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './proposals.component.html',
  styleUrls: ['./proposals.component.scss']
})
export class ProposalsComponent implements OnInit {
  proposals: any[] = [];
  rfps: any[] = [];
  averageScore = 0;
  isLoading = false;
  selectedRFPId = '';
  evaluationResult: any = null;
  showEvaluation = false;
  checkingEmails = false;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadProposals();
    this.loadRFPs();
  }

  loadProposals() {
    this.apiService.getProposals('').subscribe({
      next: (response: any) => {
        this.proposals = response.results || [];
        
        // Calculate average score
        if (this.proposals.length > 0) {
          const totalScore = this.proposals.reduce((sum: number, p: any) => sum + (p.score || 0), 0);
          this.averageScore = totalScore / this.proposals.length;
        }
      },
      error: (err) => console.error('Error loading proposals:', err)
    });
  }

  loadRFPs() {
    this.apiService.getRFPs().subscribe({
      next: (response: any) => {
        this.rfps = response.results || [];
      },
      error: (err) => console.error('Error loading RFPs:', err)
    });
  }

  checkForEmails() {
    this.checkingEmails = true;
    this.apiService.checkProposalEmails().subscribe({
      next: (response: any) => {
        this.checkingEmails = false;
        alert(`Checked emails. Found ${response.proposals_received?.length || 0} new proposals.`);
        this.loadProposals();
      },
      error: (err) => {
        this.checkingEmails = false;
        console.error('Error checking emails:', err);
        alert('Error checking emails: ' + (err.error?.error || err.message));
      }
    });
  }

  evaluateProposals() {
    if (!this.selectedRFPId) {
      alert('Please select an RFP to evaluate');
      return;
    }

    this.isLoading = true;
    this.apiService.compareProposals(this.selectedRFPId).subscribe({
      next: (response: any) => {
        this.evaluationResult = response;
        this.showEvaluation = true;
        this.isLoading = false;
      },
      error: (err) => {
        this.isLoading = false;
        console.error('Error evaluating proposals:', err);
        alert('Error evaluating proposals: ' + (err.error?.error || err.message));
      }
    });
  }

  parseProposal(proposal: any) {
    this.isLoading = true;
    this.apiService.parseProposal(proposal.id).subscribe({
      next: (response: any) => {
        const index = this.proposals.findIndex(p => p.id === proposal.id);
        if (index !== -1) {
          this.proposals[index] = response;
        }
        this.isLoading = false;
        alert('Proposal parsed successfully!');
      },
      error: (err) => {
        this.isLoading = false;
        console.error('Error parsing proposal:', err);
        alert('Error parsing proposal: ' + (err.error?.error || err.message));
      }
    });
  }

  getScoreBadge(score: number): string {
    if (score >= 90) return 'bg-success';
    if (score >= 80) return 'bg-info';
    if (score >= 70) return 'bg-warning text-dark';
    return 'bg-danger';
  }

  getStatusBadge(status: string): string {
    switch (status) {
      case 'RECEIVED':
        return 'bg-secondary';
      case 'PARSED':
        return 'bg-warning text-dark';
      case 'EVALUATED':
        return 'bg-success';
      default:
        return 'bg-primary';
    }
  }

  viewProposal(proposal: any) {
    alert(`Proposal from ${proposal.vendor_name} - Score: ${proposal.score || 'N/A'}/100\n\nPrice: $${proposal.price}\nDelivery: ${proposal.delivery_time}\nWarranty: ${proposal.warranty || 'N/A'}`);
  }
}
