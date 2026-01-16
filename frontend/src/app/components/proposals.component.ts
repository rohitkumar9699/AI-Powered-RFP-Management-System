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
  
  // Modal properties
  showViewModal = false;
  showConfirmModal = false;
  selectedProposal: any = null;
  confirmTitle = '';
  confirmMessage = '';
  confirmActionText = '';
  confirmType = '';
  pendingAction: () => void = () => {};

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
        this.showSuccessModal(`Checked emails. Found ${response.proposals_received?.length || 0} new proposals.`);
        this.loadProposals();
      },
      error: (err) => {
        this.checkingEmails = false;
        console.error('Error checking emails:', err);
        this.showErrorModal('Error checking emails: ' + (err.error?.error || err.message));
      }
    });
  }

  evaluateProposals() {
    if (!this.selectedRFPId) {
      this.showErrorModal('Please select an RFP to evaluate');
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
        this.showErrorModal('Error evaluating proposals: ' + (err.error?.error || err.message));
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
        this.showSuccessModal('Proposal parsed successfully!');
      },
      error: (err) => {
        this.isLoading = false;
        console.error('Error parsing proposal:', err);
        this.showErrorModal('Error parsing proposal: ' + (err.error?.error || err.message));
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
      case 'ACCEPTED':
        return 'bg-success';
      default:
        return 'bg-primary';
    }
  }

  viewProposal(proposal: any) {
    this.selectedProposal = proposal;
    this.showViewModal = true;
  }

  acceptProposal(proposal: any) {
    this.selectedProposal = proposal;
    this.confirmTitle = 'Accept Proposal';
    this.confirmMessage = `Are you sure you want to accept the proposal from ${proposal.vendor_name}?`;
    this.confirmActionText = 'Accept';
    this.confirmType = 'accept';
    this.pendingAction = () => this.executeAcceptProposal();
    this.showConfirmModal = true;
  }

  deleteProposal(proposal: any) {
    this.selectedProposal = proposal;
    this.confirmTitle = 'Delete Proposal';
    this.confirmMessage = `Are you sure you want to delete the proposal from ${proposal.vendor_name}? This action cannot be undone.`;
    this.confirmActionText = 'Delete';
    this.confirmType = 'delete';
    this.pendingAction = () => this.executeDeleteProposal();
    this.showConfirmModal = true;
  }

  executeAcceptProposal() {
    this.apiService.acceptProposal(this.selectedProposal.id).subscribe({
      next: (response: any) => {
        const index = this.proposals.findIndex(p => p.id === this.selectedProposal.id);
        if (index !== -1) {
          this.proposals[index] = response;
        }
        this.closeConfirmModal();
        this.showSuccessModal('Proposal accepted successfully! Acceptance email sent to vendor.');
      },
      error: (err) => {
        console.error('Error accepting proposal:', err);
        this.showErrorModal('Error accepting proposal: ' + (err.error?.error || err.message));
      }
    });
  }

  executeDeleteProposal() {
    this.apiService.deleteProposal(this.selectedProposal.id).subscribe({
      next: () => {
        this.proposals = this.proposals.filter(p => p.id !== this.selectedProposal.id);
        this.closeConfirmModal();
        this.showSuccessModal('Proposal deleted successfully!');
      },
      error: (err) => {
        console.error('Error deleting proposal:', err);
        this.showErrorModal('Error deleting proposal: ' + (err.error?.error || err.message));
      }
    });
  }

  executeConfirmedAction() {
    this.pendingAction();
  }

  closeViewModal() {
    this.showViewModal = false;
    this.selectedProposal = null;
  }

  closeConfirmModal() {
    this.showConfirmModal = false;
    this.confirmTitle = '';
    this.confirmMessage = '';
    this.confirmActionText = '';
    this.confirmType = '';
    this.pendingAction = () => {};
  }

  showSuccessModal(message: string) {
    // For now, we'll use a simple approach - you can enhance this with a proper modal component
    const modal = document.createElement('div');
    modal.className = 'modal fade show';
    modal.style.display = 'block';
    modal.innerHTML = `
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-success text-white">
            <h5 class="modal-title">Success</h5>
            <button type="button" class="btn-close btn-close-white" onclick="this.closest('.modal').remove()"></button>
          </div>
          <div class="modal-body">
            <p>${message}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-success" onclick="this.closest('.modal').remove()">OK</button>
          </div>
        </div>
      </div>
      <div class="modal-backdrop fade show"></div>
    `;
    document.body.appendChild(modal);
    setTimeout(() => modal.remove(), 3000); // Auto-remove after 3 seconds
  }

  showErrorModal(message: string) {
    const modal = document.createElement('div');
    modal.className = 'modal fade show';
    modal.style.display = 'block';
    modal.innerHTML = `
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-danger text-white">
            <h5 class="modal-title">Error</h5>
            <button type="button" class="btn-close btn-close-white" onclick="this.closest('.modal').remove()"></button>
          </div>
          <div class="modal-body">
            <p>${message}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-danger" onclick="this.closest('.modal').remove()">OK</button>
          </div>
        </div>
      </div>
      <div class="modal-backdrop fade show"></div>
    `;
    document.body.appendChild(modal);
  }
}
