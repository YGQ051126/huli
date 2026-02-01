import api from './api';

// Service Types (Catalog)
export interface ServiceType {
  id: number;
  name: string;
  service_type: string;
  description: string;
  price: number;
  duration?: number;
}

// Service Order
export interface ServiceOrderItem {
  id: number;
  service_name: string;
  price: number;
}

export interface ServiceFeedbackImage {
  id: number;
  image: string;
  created_at: string;
}

export interface ServiceFeedback {
  id: number;
  staff_name: string;
  content: string;
  images: ServiceFeedbackImage[];
  created_at: string;
}

export interface ServiceReview {
  id: number;
  rating: number;
  comment: string;
  created_at: string;
}

export interface ServiceOrder {
  id: number;
  order_no: string;
  family_name: string;
  patient_name: string;
  total_amount: number;
  status: 'pending' | 'processing' | 'completed' | 'rated' | 'cancelled';
  paid_at: string;
  created_at: string;
  items: ServiceOrderItem[];
  feedback?: ServiceFeedback;
  review?: ServiceReview;
}

// APIs
export const getServiceTypes = () => {
  return api.get<ServiceType[]>('/service-types/');
};

export const getServiceOrders = () => {
  return api.get<any>('/service-orders/');
};

export const createServiceOrder = (data: { patient_id: number | string; service_ids: number[] }) => {
  return api.post<ServiceOrder>('/service-orders/create_order/', data);
};

export const processServiceOrder = (orderId: number) => {
  return api.post(`/service-orders/${orderId}/process/`);
};

export const submitServiceFeedback = (orderId: number, formData: FormData) => {
  return api.post(`/service-orders/${orderId}/submit_feedback/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const submitServiceReview = (orderId: number, data: { rating: number; comment: string }) => {
  return api.post(`/service-orders/${orderId}/submit_review/`, data);
};

export const getServiceStats = () => {
  return api.get<any[]>('/service-orders/stats/');
};

export const createServiceType = (data: Partial<ServiceType>) => {
  return api.post<ServiceType>('/service-types/', data);
};

export const updateServiceType = (id: number, data: Partial<ServiceType>) => {
  return api.put<ServiceType>(`/service-types/${id}/`, data);
};

export const deleteServiceType = (id: number) => {
  return api.delete(`/service-types/${id}/`);
};
