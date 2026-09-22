import { useEffect, useState } from 'react';
import {
  Card,
  Container,
  Grid,
  SimpleGrid,
  Table,
  Text,
  Title,
} from '@mantine/core';
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
    <Card withBorder className="card-lift animate-fade-in-up" style={{ animationDelay: `${delay}ms`, animationFillMode: 'both' }}>
      <Text size="sm" c="dimmed">{label}</Text>
      <Text size="xl" fw={700} mt={8} mb={4}>{value}</Text>
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
      <Container size="xl" py="xl">
        <div className="shimmer" style={{ height: 32, width: 240, marginBottom: 16 }} />
        <SimpleGrid cols={{ base: 1, sm: 3 }}>
          {[0, 1, 2].map((i) => (
            <div key={i} className="shimmer" style={{ height: 100 }} />
          ))}
        </SimpleGrid>
      </Container>
    );

  return (
    <Container size="xl" py="xl">
      <Title order={2} mb={4}>How we pay people</Title>
      <Text size="sm" c="dimmed" mb="xl">
        Payroll overview — amounts normalized to USD using the current FX rate.
      </Text>

      <SimpleGrid cols={{ base: 1, sm: 3 }} mb="xl">
        {[
          { label: 'Headcount (active)', value: String(data.headcount) },
          { label: 'Total payroll (USD)', value: `$${Number(data.total_usd).toLocaleString()}` },
          { label: 'FX rate date', value: data.rate_date ?? '—' },
        ].map((kpi, i) => (
          <KpiCard key={kpi.label} {...kpi} delay={400 + i * 120} />
        ))}
      </SimpleGrid>

      <Grid mb="xl">
        <Grid.Col span={{ base: 12, md: 6 }}>
          <Card withBorder className="card-lift animate-fade-in" style={{ animationDelay: '600ms', animationFillMode: 'both', p: 'md' }}>
            <Text fw={600} mb="sm">Distribution (USD)</Text>
            <ResponsiveContainer width="100%" height={240}>
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
          <Card withBorder className="card-lift animate-fade-in" style={{ animationDelay: '750ms', animationFillMode: 'both', p: 'md' }}>
            <Text fw={600} mb="sm">Top earners (USD)</Text>
            <Table striped withTableBorder className="row-hover">
              <Table.Thead>
                <Table.Tr>
                  <Table.Th>Name</Table.Th><Table.Th>Dept</Table.Th><Table.Th>USD</Table.Th>
                </Table.Tr>
              </Table.Thead>
              <Table.Tbody>
                {data.top_earners.slice(0, 5).map((t, i) => (
                  <Table.Tr key={t.id} className="animate-slide-in" style={{ animationDelay: `${i * 60}ms`, animationFillMode: 'both' }}>
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

      <SimpleGrid cols={{ base: 1, md: 2 }} mb="xl">
        <Card withBorder className="card-lift animate-fade-in" style={{ animationDelay: '1000ms', animationFillMode: 'both', p: 'md' }}>
          <Text fw={600} mb="sm">Avg by department (USD)</Text>
          {entries(data.avg_by_department).map(({ k, v }) => (
            <Text key={k} size="sm" mt={8} mb={4}>{k}: ${Number(v).toLocaleString()}</Text>
          ))}
        </Card>
        <Card withBorder className="card-lift animate-fade-in" style={{ animationDelay: '1100ms', animationFillMode: 'both', p: 'md' }}>
          <Text fw={600} mb="sm">Avg by country (USD)</Text>
          {entries(data.avg_by_country).map(({ k, v }) => (
            <Text key={k} size="sm" mt={8} mb={4}>{k}: ${Number(v).toLocaleString()}</Text>
          ))}
        </Card>
      </SimpleGrid>
    </Container>
  );
}
