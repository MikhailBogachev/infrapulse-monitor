import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  timeout: 15_000,
  use: { baseURL: process.env.INFRAPULSE_BASE_URL ?? 'http://127.0.0.1:8080' },
});
