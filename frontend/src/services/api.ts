import axios from 'axios';

// Create an axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:5001/api', // Updated Flask backend URL to port 5001
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to add the auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Auth API calls
export const authAPI = {
  login: (username: string, password: string) =>
    api.post('/auth/login', { username, password }),
  
  register: (username: string, email: string, password: string) =>
    api.post('/auth/register', { username, email, password }),
  
  getCurrentUser: () => api.get('/auth/me'),
};

// Todo API calls
export const todoAPI = {
  getAllTodos: () => api.get('/todos/'),
  
  getTodo: (id: number) => api.get(`/todos/${id}`),
  
  createTodo: (todo: { title: string; description?: string; due_date?: string }) =>
    api.post('/todos/', todo),
  
  updateTodo: (id: number, updates: { 
    title?: string; 
    description?: string; 
    completed?: boolean;
    due_date?: string | null;
  }) => api.put(`/todos/${id}`, updates),
  
  deleteTodo: (id: number) => api.delete(`/todos/${id}`),
};

export default api;
