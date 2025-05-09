import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export async function savePlayerName(playerName: string) {
  // Hier könnte ein echter API-Call stehen, z.B. POST /api/config/playername
  localStorage.setItem('playerName', playerName);
}

export async function saveScPath(scPath: string) {
  // Hier könnte ein echter API-Call stehen, z.B. POST /api/config/scpath
  localStorage.setItem('scPath', scPath);
}

export function loadPlayerName() {
  return localStorage.getItem('playerName') || '';
}

export function loadScPath() {
  return localStorage.getItem('scPath') || '';
}
