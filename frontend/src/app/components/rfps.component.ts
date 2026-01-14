import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-rfps',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './rfps.component.html',
  styleUrls: ['./rfps.component.scss']
})
export class RFpsComponent implements OnInit {
  rfps: any[] = [];
  showForm = false;
  isLoading = false;
  selectedRFP: any = null;
  
  newRFP = {
    title: '',
    description: '',
    budget: 0,
    deadline: '',
    requirements: ''
  };

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadRFPs();
  }

  loadRFPs() {
    this.isLoading = true;
    this.apiService.getRFPs().subscribe({
      next: (response: any) => {
        this.rfps = response.results || [];
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Error loading RFPs:', err);
        this.isLoading = false;
      }
    });
  }

  toggleForm() {
    this.showForm = !this.showForm;
    if (!this.showForm) {
      this.resetForm();
    }
  }

  createRFP() {
    if (!this.newRFP.title || !this.newRFP.description) {
      alert('Please fill in required fields');
      return;
    }

    this.isLoading = true;
    this.apiService.createRFP(this.newRFP).subscribe({
      next: (response: any) => {
        this.rfps.unshift(response);
        this.resetForm();
        this.showForm = false;
        this.isLoading = false;
        alert('RFP created successfully!');
      },
      error: (err) => {
        console.error('Error creating RFP:', err);
        this.isLoading = false;
        alert('Error creating RFP: ' + (err.error?.detail || err.message));
      }
    });
  }

  viewRFP(rfp: any) {
    this.selectedRFP = rfp;
    alert(`RFP: ${rfp.title}\n\nBudget: $${rfp.budget}\nDeadline: ${new Date(rfp.deadline).toLocaleDateString()}\nStatus: ${rfp.status}\n\nDescription:\n${rfp.description}`);
  }

  editRFP(rfp: any) {
    this.newRFP = {
      title: rfp.title,
      description: rfp.description,
      budget: rfp.budget,
      deadline: rfp.deadline?.split('T')[0] || '',
      requirements: rfp.requirements || ''
    };
    this.selectedRFP = rfp;
    this.showForm = true;
    window.scrollTo(0, 0);
  }

  deleteRFP(rfp: any) {
    if (confirm(`Are you sure you want to delete "${rfp.title}"?`)) {
      this.isLoading = true;
      this.apiService.deleteRFP(String(rfp.id)).subscribe({
        next: () => {
          this.rfps = this.rfps.filter(r => r.id !== rfp.id);
          this.isLoading = false;
          alert('RFP deleted successfully!');
        },
        error: (err) => {
          console.error('Error deleting RFP:', err);
          this.isLoading = false;
          alert('Error deleting RFP');
        }
      });
    }
  }

  resetForm() {
    this.newRFP = {
      title: '',
      description: '',
      budget: 0,
      deadline: '',
      requirements: ''
    };
    this.selectedRFP = null;
  }

  getStatusBadge(status: string): string {
    switch (status) {
      case 'DRAFT':
        return 'bg-secondary';
      case 'SENT':
        return 'bg-warning text-dark';
      case 'CLOSED':
        return 'bg-danger';
      case 'AWARDED':
        return 'bg-success';
      default:
        return 'bg-primary';
    }
  }
}
