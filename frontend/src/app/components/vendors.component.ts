import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-vendors',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './vendors.component.html',
  styleUrls: ['./vendors.component.scss']
})
export class VendorsComponent implements OnInit {
  vendors: any[] = [];
  showForm = false;
  isLoading = false;
  
  newVendor = {
    name: '',
    email: '',
    contact_person: '',
    phone: '',
    city: '',
    country: '',
    website: '',
    notes: ''
  };

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadVendors();
  }

  loadVendors() {
    this.isLoading = true;
    this.apiService.getVendors().subscribe({
      next: (response: any) => {
        this.vendors = response.results || [];
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Error loading vendors:', err);
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

  addVendor() {
    if (!this.newVendor.name || !this.newVendor.email) {
      alert('Please fill in required fields');
      return;
    }

    this.isLoading = true;
    this.apiService.createVendor(this.newVendor).subscribe({
      next: (response: any) => {
        this.vendors.unshift(response);
        this.resetForm();
        this.showForm = false;
        this.isLoading = false;
        alert('Vendor created successfully!');
      },
      error: (err) => {
        console.error('Error creating vendor:', err);
        this.isLoading = false;
        alert('Error creating vendor');
      }
    });
  }

  editVendor(vendor: any) {
    alert('Edit functionality coming soon!');
  }

  deleteVendor(id: number) {
    if (confirm('Are you sure you want to delete this vendor?')) {
      this.apiService.deleteVendor(String(id)).subscribe({
        next: () => {
          this.vendors = this.vendors.filter(v => v.id !== id);
          alert('Vendor deleted successfully!');
        },
        error: (err) => {
          console.error('Error deleting vendor:', err);
          alert('Error deleting vendor');
        }
      });
    }
  }

  resetForm() {
    this.newVendor = {
      name: '',
      email: '',
      contact_person: '',
      phone: '',
      city: '',
      country: '',
      website: '',
      notes: ''
    };
  }
}
