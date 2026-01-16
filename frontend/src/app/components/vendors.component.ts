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
  isEditMode = false;
  editingVendor: any = null;
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
      this.isEditMode = false;
      this.editingVendor = null;
    }
  }

  addVendor() {
    if (!this.newVendor.name || !this.newVendor.email) {
      this.showErrorModal('Please fill in required fields');
      return;
    }

    this.isLoading = true;
    this.apiService.createVendor(this.newVendor).subscribe({
      next: (response: any) => {
        this.vendors.unshift(response);
        this.resetForm();
        this.showForm = false;
        this.isLoading = false;
        this.showSuccessModal('Vendor created successfully!');
      },
      error: (err) => {
        console.error('Error creating vendor:', err);
        this.isLoading = false;
        this.showErrorModal('Error creating vendor');
      }
    });
  }

  submitForm() {
    if (this.isEditMode) {
      this.updateVendor();
    } else {
      this.addVendor();
    }
  }

  editVendor(vendor: any) {
    this.editingVendor = vendor;
    this.isEditMode = true;
    this.newVendor = {
      name: vendor.name,
      email: vendor.email,
      contact_person: vendor.contact_person || '',
      phone: vendor.phone || '',
      city: vendor.city || '',
      country: vendor.country || '',
      website: vendor.website || '',
      notes: vendor.notes || ''
    };
    this.showForm = true;
  }

  updateVendor() {
    if (!this.newVendor.name || !this.newVendor.email) {
      this.showErrorModal('Please fill in required fields');
      return;
    }

    this.isLoading = true;
    this.apiService.updateVendor(String(this.editingVendor.id), this.newVendor).subscribe({
      next: (response: any) => {
        const index = this.vendors.findIndex(v => v.id === this.editingVendor.id);
        if (index !== -1) {
          this.vendors[index] = response;
        }
        this.resetForm();
        this.showForm = false;
        this.isEditMode = false;
        this.editingVendor = null;
        this.isLoading = false;
        this.showSuccessModal('Vendor updated successfully!');
      },
      error: (err) => {
        console.error('Error updating vendor:', err);
        this.isLoading = false;
        this.showErrorModal('Error updating vendor');
      }
    });
  }

  deleteVendor(id: number) {
    this.showConfirmModal('Delete Vendor', 'Are you sure you want to delete this vendor? This action cannot be undone.', 'Delete', () => {
      this.apiService.deleteVendor(String(id)).subscribe({
        next: () => {
          this.vendors = this.vendors.filter(v => v.id !== id);
          this.showSuccessModal('Vendor deleted successfully!');
        },
        error: (err) => {
          console.error('Error deleting vendor:', err);
          this.showErrorModal('Error deleting vendor');
        }
      });
    });
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

  showConfirmModal(title: string, message: string, actionText: string, action: () => void) {
    const modal = document.createElement('div');
    modal.className = 'modal fade show';
    modal.style.display = 'block';
    modal.setAttribute('data-action', 'confirm');
    modal.innerHTML = `
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">${title}</h5>
            <button type="button" class="btn-close" onclick="this.closest('.modal').remove()"></button>
          </div>
          <div class="modal-body">
            <p>${message}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" onclick="this.closest('.modal').remove()">Cancel</button>
            <button type="button" class="btn btn-danger" id="confirmActionBtn">${actionText}</button>
          </div>
        </div>
      </div>
      <div class="modal-backdrop fade show"></div>
    `;
    document.body.appendChild(modal);
    
    // Store the action and attach event listener
    (modal as any)._action = action;
    const actionBtn = modal.querySelector('#confirmActionBtn') as HTMLButtonElement;
    actionBtn.addEventListener('click', () => {
      modal.remove();
      action();
    });
  }

  showSuccessModal(message: string) {
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
    setTimeout(() => modal.remove(), 3000);
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
