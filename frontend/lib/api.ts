import axios from 'axios';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE,
});

export type Cluster = {
  id: number;
  topic: string;
  summary: string | null;
  momentum: number;
  created_at: string;
  updated_at: string;
  items: Item[];
};

export type Item = {
  id: number;
  title: string;
  content: string;
  url: string;
  author: string | null;
  published_at: string;
  score: number;
  source: Source;
};

export type Source = {
  id: number;
  name: string;
  type: string;
};

export const getClusters = () => api.get<Cluster[]>('/clusters/').then(res => res.data);
export const getCluster = (id: number) => api.get<Cluster>(`/clusters/${id}`).then(res => res.data);
export const generateBrief = (id: number) => api.post(`/clusters/${id}/brief`).then(res => res.data);
export const triggerIngest = () => api.post('/ingest/run').then(res => res.data);