import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  vendors: any[] = [];
  rfps: any[] = [];
  proposals: any[] = [];
  
  vendorCount = 0;
  rfpCount = 0;
  proposalCount = 0;
  averageScore = 0;
  
  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadDashboardData();
  }

  loadDashboardData() {
    // Load Vendors
    this.apiService.getVendors().subscribe({
      next: (response: any) => {
        this.vendors = response.results || [];
        this.vendorCount = response.count || 0;
      },
      error: (err) => console.error('Error loading vendors:', err)
    });

    // Load RFPs
    this.apiService.getRFPs().subscribe({
      next: (response: any) => {
        this.rfps = response.results || [];
        this.rfpCount = response.count || 0;
      },
      error: (err) => console.error('Error loading RFPs:', err)
    });

    // Load Proposals
    this.apiService.getProposals('').subscribe({
      next: (response: any) => {
        this.proposals = response.results || [];
        this.proposalCount = response.count || 0;
        
        // Calculate average score
        if (this.proposals.length > 0) {
          const totalScore = this.proposals.reduce((sum: number, p: any) => sum + (p.score || 0), 0);
          this.averageScore = totalScore / this.proposals.length;
        }
      },
      error: (err) => console.error('Error loading proposals:', err)
    });
  }
}
