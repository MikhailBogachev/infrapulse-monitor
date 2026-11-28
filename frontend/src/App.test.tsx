import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { cleanup, render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router';
import { afterEach, expect, test, vi } from 'vitest';

import { App } from './App';

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

test.each([
  [200, { status: 'live' }, 'API is live'],
  [503, { status: 'not_ready' }, 'API is unavailable'],
  [200, { status: 'unknown' }, 'API is unavailable'],
])('renders the health response for status %i', async (code, payload, label) => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(Response.json(payload, { status: code })));
  render(
    <QueryClientProvider client={new QueryClient()}>
      <MemoryRouter><App /></MemoryRouter>
    </QueryClientProvider>,
  );
  expect(screen.getByRole('heading', { name: 'InfraPulse' })).toBeTruthy();
  expect(await screen.findByText(label)).toBeTruthy();
});
