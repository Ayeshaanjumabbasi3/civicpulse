# ADR 0002: Frontend runtime configuration

The API URL is resolved from `public/config.js` and `window.__CONFIG__` rather than baked into the Vite bundle. The same image can therefore run in Compose and Kubernetes. `frontend/nginx.conf` proxies `/api/` to the backend service while the browser keeps using the frontend origin.
