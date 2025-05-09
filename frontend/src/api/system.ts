import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export async function fetchLogStatus() {
  const res = await axios.get(`${API_URL}/log_status`);
  return res.data;
}

export async function fetchDbSize() {
  const res = await axios.get(`${API_URL}/db_size`);
  return res.data;
}

export async function fetchUpdateCheck() {
  const res = await axios.get(`${API_URL}/update_check`);
  return res.data;
}

export async function clearAppData() {
  const res = await axios.post(`${API_URL}/clear_appdata`);
  return res.data;
}
