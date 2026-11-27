import { useQuery } from '@tanstack/react-query';
import { Activity } from 'lucide-react';
import { Route, Routes } from 'react-router';
import { z } from 'zod';

import { Card } from './components/ui/card';

const live = z.object({ status: z.literal('live') });

function Status() {
  const health = useQuery({
    queryKey: ['health', 'live'],
    queryFn: async ({ signal }) => {
      const response = await fetch('/health/live', { signal });
      if (!response.ok) throw new Error('API unavailable');
      return live.parse(await response.json());
    },
    retry: false,
  });

  return (
    <main className="mx-auto max-w-xl px-4 py-12">
      <Card aria-labelledby="page-title">
        <Activity aria-hidden="true" className="mb-4 text-accent" />
        <h1 id="page-title" className="text-2xl font-semibold">InfraPulse</h1>
        <p role="status" className="mt-3 text-muted-foreground">
          {health.isPending ? 'Checking API…' : health.isSuccess ? 'API is live' : 'API is unavailable'}
        </p>
      </Card>
    </main>
  );
}

export function App() {
  return (
    <Routes>
      <Route path="/" element={<Status />} />
      <Route path="*" element={<main className="p-6"><h1>Page not found</h1></main>} />
    </Routes>
  );
}
