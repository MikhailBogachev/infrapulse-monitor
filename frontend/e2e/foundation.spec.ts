import { expect, test } from '@playwright/test';

test('Nginx serves the SPA and preserves health and API responses', async ({ page, request }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'InfraPulse' })).toBeVisible();
  await expect(page.getByRole('status')).toHaveText('API is live');
  await page.goto('/unknown-route');
  await expect(page.getByRole('heading', { name: 'Page not found' })).toBeVisible();
  expect((await request.get('/api/v1/unknown')).status()).toBe(404);
  expect(await (await request.get('/health/ready')).json()).toEqual({ status: 'ready' });
});
