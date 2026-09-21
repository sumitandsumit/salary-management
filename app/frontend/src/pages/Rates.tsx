import { useEffect, useState } from 'react';
import { Button, Group, Modal, NumberInput, Table, Text, TextInput, Title } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { listRates, updateRate } from '../lib/api';
import type { Rate } from '../lib/types';

export function Rates() {
  const [rows, setRows] = useState<Rate[]>([]);
  const [error, setError] = useState('');
  const [editRow, setEditRow] = useState<Rate | null>(null);
  const [rate, setRate] = useState<number>(0);
  const [day, setDay] = useState('');
  const [reason, setReason] = useState('');

  async function load() {
    try {
      setRows(await listRates());
    } catch (e) {
      setError((e as Error).message);
    }
  }

  useEffect(() => {
    void load();
  }, []);

  function openEdit(row: Rate) {
    setEditRow(row);
    setRate(Number(row.rate_to_usd));
    setDay(row.effective_date);
    setReason('');
  }

  async function save() {
    if (!editRow) return;
    try {
      await updateRate(editRow.currency_code, rate, day, reason || undefined);
      notifications.show({ color: 'green', message: `${editRow.currency_code} rate updated` });
      setEditRow(null);
      await load();
    } catch (e) {
      notifications.show({ color: 'red', message: (e as Error).message });
    }
  }

  if (error) return <Text c="red">Failed to load rates: {error}</Text>;

  return (
    <>
      <Title order={3} mb="xs">Exchange rates</Title>
      <Text size="sm" c="dimmed" mb="md">
        Rate converts local salary to USD on read. Dashboard shows the rate date in use.
      </Text>
      <Table striped withTableBorder>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Currency</Table.Th><Table.Th>Rate to USD</Table.Th>
            <Table.Th>Effective date</Table.Th><Table.Th>Actions</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {rows.map((r) => (
            <Table.Tr key={r.currency_code}>
              <Table.Td>{r.currency_code}</Table.Td>
              <Table.Td>{r.rate_to_usd}</Table.Td>
              <Table.Td>{r.effective_date}</Table.Td>
              <Table.Td>
                <Group gap="xs">
                  <Button size="xs" variant="light" onClick={() => openEdit(r)}>Edit</Button>
                </Group>
              </Table.Td>
            </Table.Tr>
          ))}
        </Table.Tbody>
      </Table>

      <Modal opened={editRow !== null} onClose={() => setEditRow(null)} title={`Edit rate — ${editRow?.currency_code ?? ''}`}>
        <NumberInput
          label="Rate to USD"
          value={rate}
          onChange={(v) => setRate(typeof v === 'number' ? v : Number(v) || 0)}
          min={0}
          decimalScale={6}
        />
        <TextInput label="Effective date" type="date" value={day} onChange={(e) => setDay(e.target.value)} mt="sm" />
        <TextInput label="Reason (optional)" value={reason} onChange={(e) => setReason(e.target.value)} mt="sm" />
        <Button mt="md" onClick={() => void save()}>Save rate</Button>
      </Modal>
    </>
  );
}
