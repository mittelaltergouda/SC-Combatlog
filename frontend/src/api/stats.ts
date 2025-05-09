import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export async function fetchStats(params: any) {
  const res = await axios.get(`${API_URL}/stats`, { params });
  return res.data;
}

export async function fetchLeaderboards(params: any) {
  const res = await axios.get(`${API_URL}/leaderboards`, { params });
  return res.data;
}

export async function fetchEvents(params: any) {
  const res = await axios.get(`${API_URL}/events`, { params });
  return res.data;
}
