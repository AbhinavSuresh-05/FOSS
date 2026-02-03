import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// Authentication
export const login = async (username, password) => {
  const response = await axios.post(`${API_BASE_URL}/auth/token/`, {
    username,
    password,
  });
  return response.data;
};

export const logout = () => {
  localStorage.removeItem('authToken');
  localStorage.removeItem('username');
};

// Registration
export const register = async (username, password, password_confirm) => {
  const response = await axios.post(`${API_BASE_URL}/auth/register/`, {
    username,
    password,
    password_confirm,
  });
  return response.data;
};

// Equipment API
export const uploadCSV = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getDashboardStats = async () => {
  const response = await api.get('/dashboard/');
  return response.data;
};

export const getEquipmentList = async () => {
  const response = await api.get('/equipment/');
  return response.data;
};

export const downloadPDF = async () => {
  const response = await api.get('/report/pdf/', {
    responseType: 'blob',
  });
  return response.data;
};

export default api;
