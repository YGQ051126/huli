export interface Announcement {
  id: string | number;
  title: string;
  content: string;
  target_role: 'all' | 'family' | 'staff';
  status: 'published' | 'draft' | 'retracted';
  publish_time: string;
  expire_time?: string;
  created_by?: string | number;
  created_at: string;
  updated_at: string;
}

export interface AnnouncementQueryParams {
  status?: 'draft' | 'published' | 'retracted';
  target_role?: 'all' | 'family' | 'staff';
  page?: number;
  page_size?: number;
}