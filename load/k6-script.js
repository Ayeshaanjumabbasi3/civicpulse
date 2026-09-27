import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = { vus: 20, duration: '2m' };

export default function () {
  const response = http.get(`${__ENV.BASE_URL || 'http://civicpulse.local'}/api/stats`);
  check(response, { 'stats is healthy': (r) => r.status === 200 });
  sleep(0.1);
}
