export interface Vendor {
  id?: string;
  name: string;
  email: string;
  contact_person?: string;
  phone?: string;
  address?: string;
  city?: string;
  country?: string;
  website?: string;
  notes?: string;
  active: boolean;
}

export interface RFP {
  id?: string;
  title: string;
  description: string;
  requirements: any;
  budget?: number;
  deadline: string;
  status: 'DRAFT' | 'SENT' | 'CLOSED' | 'AWARDED';
  selected_vendors: string[];
  awarded_vendor?: string;
  natural_language_input: string;
}

export interface Proposal {
  id?: string;
  rfp_id: string;
  vendor_id: string;
  vendor_name: string;
  proposal_content: string;
  parsed_data: any;
  price?: number;
  delivery_time?: string;
  warranty?: string;
  payment_terms?: string;
  score?: number;
  evaluation?: any;
  status: 'RECEIVED' | 'PARSED' | 'EVALUATED';
}
