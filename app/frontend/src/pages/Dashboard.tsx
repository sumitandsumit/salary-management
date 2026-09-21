import { useEffect, useState } from 'react';
import { Card, Grid, SimpleGrid, Table, Text, Title } from '@mantine/core';
import {
  Bar,
  BarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { fetchSummary } from '../lib/api';
import type { AnalyticsSummary } from '../lib/types';

function entries(record: Record<string, string>) {
  return Object.entries(record).map(([k, v]) => ({ k, v }));
}

function KpiCard({ label, value, delay }: { label: string; value: string; delay: number }) {
  return (
    <Card withBorder className="card-lift animate-fade-in-up" style={{ animationDelay: `${delay}ms`, animationFillMode: 'both', padding: '1rem' }}>
      <Text size="sm" c="dimmed">{label}</Text>
      <Text size="xl" fw={700} mt={4}>{value}</Text>
    </Card>
  );
}

export function Dashboard() {
  const [data, setData] = useState<AnalyticsSummary | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchSummary().then(setData).catch((e: Error) => setError(e.message));
  }, []);

  if (error) return <Text c="red">Failed to load analytics: {error}</Text>;
  if (!data)
    return (
      <div style={{ padding: 32 }}>
        <div className="shimmer" style={{ height: 32, width: 240, marginBottom: 16 }} />
        <SimpleGrid cols={{ base: 1, sm: 3 }}>
          {[0, 1, 2].map((i) => (
            <div key={i} className="shimmer" style={{ height: 96 }} />
          ))}
        </SimpleGrid>
      </div>
    );

  return (
    <div className="page-shell">
      <Title order={3} className="page-title">
        How we pay people
      </Title>
      <Text size="sm" c="dimmed" className="page-subtitle">
        Payroll overview — amounts normalized to USD using the current FX rate.
      </Text>

      <SimpleGrid cols={{ base: 1, sm: 3 }} className="kpi-grid">
        {[
          { label: 'Headcount (active)', value: String(data.headcount) },
          { label: 'Total payroll (USD)', value: `$${Number(data.total_usd).toLocaleString()}` },
          { label: 'FX rate date', value: data.rate_date ?? '—' },
        ].map((kpi, i) => (
          <KpiCard key={kpi.label} {...kpi} delay={400 + i * 120} />
        ))}
      </SimpleGrid>

      <Grid>
        <Grid.Col span={{ base: 12, md: 6 }}>
          <Card withBorder className="card-lift animate-fade-in" style={{ animationDelay: '600ms', animationFillMode: 'both', padding: '1rem' }}>
            <Text fw={600} mb="xs">Distribution (USD)</Text>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={data.distribution}>
                <XAxis dataKey="label" />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="count" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Grid.Col>
        <Grid.Col span={{ base: 12, md: 6 }}>
          <Card withBorder className="card-lift" style={{ animationDelay: '750ms', animationFillMode: 'both', padding: '1rem' }}>
            <Text fw={600} mb="xs">Top earners (USD)</Text>
              <Table striped withTableBorder className="row-hover">
                <Table.Thead>
                  <Table.Tr>
                    <Table.Th>Name</Table.Th><Table.Th>Dept</Table.Th><Table.Th>USD</Table.Th>
                  </Table.Tr>
                </Table.Thead>
                <Table.Tbody>
                  {data.top_earners.slice(0, 8).map((t, i) => (
                    <Table.Tr key={t.id} className="animate-slide-in" style={{ animationDelay: `${i * 40}ms` }}>
                      <Table.Td>{t.name}</Table.Td>
                      <Table.Td>{t.department}</Table.Td>
                      <Table.Td>${Number(t.usd_equivalent).toLocaleString()}</Table.Td>
                    </Table.Tr>
                  ))}
                </Table.Tbody>
              </Table>
            </Card>
        </Grid.Col>
      </Grid>

      <SimpleGrid cols={{ base: 1, md: 2 }} className="section-gap">
        <Card withBorder className="card-lift" style={{ animationDelay: '1000ms', animationFillMode: 'both', padding: '1rem' }}>
            <Text fw={600}>Avg by department (USD)</Text>
            {entries(data.avg_by_department).map(({ k, v }) => (
              <Text key={k} size="sm" mt={4}>{k}: ${Number(v).toLocaleString()}</Text>
            ))}
        </Card>
      </SimpleGrid>
    </div>
  );
}
