FROM node:22.22.2-bookworm-slim AS dependencies
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

FROM dependencies AS browser
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/playwright HOME=/tmp
RUN ./node_modules/.bin/playwright install --with-deps --only-shell chromium
COPY frontend/ ./
USER node
CMD ["node", "node_modules/@playwright/test/cli.js", "test", "--output", "/tmp/browser-results"]

FROM dependencies AS build
COPY frontend/ ./
RUN npm run build

FROM nginx:1.28.3-alpine AS runtime
COPY infra/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
