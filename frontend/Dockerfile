FROM node:22.11.0-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install --include=optional
# npm can skip platform-specific optional packages when the lockfile was
# generated on Windows. Alpine needs Rolldown's musl binding explicitly.
RUN npm install --no-save --include=optional @rolldown/binding-linux-x64-musl@1.2.11
COPY . .
RUN npm run build
FROM nginx:1.27.2-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD ["wget", "-qO-", "http://127.0.0.1/"]
