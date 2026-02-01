export interface User {
  id: string | number;
  username: string;
  real_name: string;
  phone: string;
  email?: string;
  role: 'admin' | 'staff' | 'family';
  status: 'active' | 'inactive' | 'pending';
  gender?: 'male' | 'female';
  avatar?: string;
  created_at: string; // Date string from backend
  updated_at: string; // Date string from backend
  // Compatibility fields for old code
  createdAt?: string;
  updatedAt?: string;
}

export interface UserProfile {
  realName: string;
  phone: string;
  email?: string;
  avatar?: string;
  // Family specific
  relationship?: string;
  patientId?: string;
  balance?: number;
  // Staff specific
  position?: string;
  department?: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthResponse {
  token: string;
  user: User;
  profile: UserProfile;
}
