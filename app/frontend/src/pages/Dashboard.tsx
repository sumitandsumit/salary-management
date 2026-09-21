import { useEffect, useState } from 'react';
import { Card, Grid, SimpleGrid, Table, Text, Title } from '@mantine/core';
import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { fetchSummary } from '../lib/api';
import type { AnalyticsSummary } from '../lib/types';

function entries(record: Record<string, string>) {
  return Object.entries(record).map(([k, v]) => ({ k, v }));
}

export function Dashboard() {
  const [data, setData] = useState<AnalyticsSummary | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchSummary().then(setData).catch((e: Error) => setError(e.message));
  }, []);

  if (error) return <Text c="red">Failed to load analytics: {error}</Text>;
  if (!data) return <Text>Loading…</Text>;

  return (
    <>
      <Title order={3} mb="md">
        How we pay people
      </Title>
      <SimpleGrid cols={{ base: 1, sm: 3 }} mb="md">
        <Card withBorder>
          <Text size="sm" c="dimmed">Headcount (active)</Text>
          <Text size="xl" fw={700}>{data.headcount}</Text>
        </Card>
        <Card withBorder>
          <Text size="sm" c="dimmed">Total payroll (USD)</Text>
          <Text size="xl" fw={700}>${Number(data.total_usd).toLocaleString()}</Text>
        </Card>
        <Card withBorder>
          <Text size="sm" c="dimmed">FX rate date</Text>
          <Text size="xl" fw={700}>{data.rate_date ?? '—'}</Text>
        </Card>
      </SimpleGrid>
      <Grid>
        <Grid.Col span={{ base: 12, md: 6 }}>
          <Card withBorder>
            <Text fw={600} mb="xs">Distribution (USD)</Text>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={data.distribution}>
                <XAxis dataKey="label" />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="count" />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Grid.Col>
        <Grid.Col span={{ base: 12, md: 6 }}>
          <Card withBorder>
            <Text fw={600} mb="xs">Top earners (USD)</Text>
            <Table striped withTableBorder>
              <Table.Thead>
                <Table.Tr><Table.Th>Name</Table.Th><Table.Th>Dept</Table.Th><Table.Th>USD</Table.Th></Table.Tr>
              </Table.Thead>
              <Table.Tbody>
                {data.top_earners.slice(0, 8).map((t) => (
                  <Table.Tr key={t.id}>
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
      <SimpleGrid cols={{ base: 1, md: 2 }} mt="md">
        <Card withBorder>
          <Text fw={600}>Avg by department (USD)</Text>
          {entries(data.avg_by_department).map(({ k, v }) => (
            <Text key={k} size="sm">{k}: ${Number(v).toLocaleString()}</Text>
          ))}
        </Card>
        <Card withBorder>
          <Text fw={600}>Avg by country (USD)</Text>
          {entries(data.avg_by_country).map(({ k, v }) => (
            <Text key={k} size="sm">{k}: ${Number(v).toLocaleString()}</Text>
          ))}
        </Card>
      </SimpleGrid>
    </>
  );
}
