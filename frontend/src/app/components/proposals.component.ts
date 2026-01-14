import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-proposals',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './proposals.component.html',
  styleUrls: ['./proposals.component.scss']
})
export class ProposalsComponent implements OnInit {
  proposals: any[] = [];
  averageScore = 0;

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadProposals();
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
    alert(`Proposal from ${proposal.vendor_name} - Score: ${proposal.score}/100\n\nPrice: $${proposal.price}\nDelivery: ${proposal.delivery_time}`);
  }
}
