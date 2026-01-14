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
  vendors: any[] = [];
  showForm = false;
  showNLForm = false;
  showSendForm = false;
  isLoading = false;
  selectedRFP: any = null;
  selectedVendors: Set<string> = new Set();
  
  newRFP = {
    title: '',
    description: '',
    budget: 0,
    deadline: '',
    requirements: ''
  };

  naturalLanguageInput = '';

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadRFPs();
    this.loadVendors();
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

  loadVendors() {
    this.apiService.getVendors().subscribe({
      next: (response: any) => {
        this.vendors = response.results || [];
      },
      error: (err) => {
        console.error('Error loading vendors:', err);
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

  createFromNaturalLanguage() {
    if (!this.naturalLanguageInput.trim()) {
      alert('Please enter a description of your procurement need');
      return;
    }

    this.isLoading = true;

    this.apiService.createRFPFromNaturalLanguage(this.naturalLanguageInput).subscribe({
      next: (response: any) => {
        this.rfps.unshift(response);
        this.naturalLanguageInput = '';
        this.showNLForm = false;
        this.isLoading = false;
        alert('RFP created from natural language successfully!');
      },
      error: (err) => {
        console.error('Error creating RFP:', err);
        this.isLoading = false;
        alert('Error creating RFP: ' + (err.error?.error || err.message));
      }
    });
  }

  toggleNLForm() {
    this.showNLForm = !this.showNLForm;
    if (!this.showNLForm) {
      this.naturalLanguageInput = '';
    }
  }

  toggleSendForm(rfp: any) {
    if (this.showSendForm && this.selectedRFP?.id === rfp.id) {
      this.showSendForm = false;
      this.selectedRFP = null;
      this.selectedVendors.clear();
    } else {
      this.showSendForm = true;
      this.selectedRFP = rfp;
      this.selectedVendors.clear();
    }
  }

  toggleVendor(vendorId: string) {
    if (this.selectedVendors.has(vendorId)) {
      this.selectedVendors.delete(vendorId);
    } else {
      this.selectedVendors.add(vendorId);
    }
  }

  sendToVendors() {
    if (this.selectedVendors.size === 0) {
      alert('Please select at least one vendor');
      return;
    }

    this.isLoading = true;
    const vendorIds = Array.from(this.selectedVendors);

    this.apiService.sendRFPToVendors(String(this.selectedRFP.id), vendorIds).subscribe({
      next: (response: any) => {
        // Update RFP in list
        const index = this.rfps.findIndex(r => r.id === this.selectedRFP.id);
        if (index !== -1) {
          this.rfps[index] = response.rfp || response;
        }
        
        this.isLoading = false;
        this.showSendForm = false;
        this.selectedVendors.clear();
        this.selectedRFP = null;
        alert('RFP sent to vendors successfully!');
      },
      error: (err) => {
        console.error('Error sending RFP:', err);
        this.isLoading = false;
        alert('Error sending RFP: ' + (err.error?.error || err.message));
      }
    });
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
