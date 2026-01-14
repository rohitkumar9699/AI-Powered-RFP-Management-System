import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-rfps',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './rfps.component.html',
  styleUrls: ['./rfps.component.scss']
})
export class RFpsComponent implements OnInit {
  rfps: any[] = [];

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.loadRFPs();
  }

  loadRFPs() {
    this.apiService.getRFPs().subscribe({
      next: (response: any) => {
        this.rfps = response.results || [];
      },
      error: (err) => console.error('Error loading RFPs:', err)
    });
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
