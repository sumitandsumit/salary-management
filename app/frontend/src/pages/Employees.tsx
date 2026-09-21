import { useEffect, useState } from 'react';
import {
  Button,
  Group,
  Modal,
  NumberInput,
  Pagination,
  Select,
  Table,
  Text,
  TextInput,
} from '@mantine/core';
import { useDebouncedValue } from '@mantine/hooks';
import { notifications } from '@mantine/notifications';
import {
  deactivateEmployee,
  incrementSalary,
  listEmployees,
  updateEmployee,
} from '../lib/api';
import type { Employee } from '../lib/types';
import { EmployeeCreateModal } from '../features/employees/EmployeeCreateModal';

const PAGE_SIZE = 25;

export function Employees() {
  const [search, setSearch] = useState('');
  const [debounced] = useDebouncedValue(search, 300);
  const [dept, setDept] = useState('');
  const [country, setCountry] = useState('');
  const [page, setPage] = useState(1);
  const [rows, setRows] = useState<Employee[]>([]);
  const [total, setTotal] = useState(0);
  const [editRow, setEditRow] = useState<Employee | null>(null);
  const [incRow, setIncRow] = useState<Employee | null>(null);
  const [percent, setPercent] = useState<number>(10);
  const [reason, setReason] = useState('annual review');
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    listEmployees({ search: debounced, dept, country, page, size: PAGE_SIZE })
      .then((res) => {
        setRows(res.data);
        setTotal(res.meta.total);
      })
      .catch((e: Error) => notifications.show({ color: 'red', message: e.message }));
  }, [debounced, dept, country, page, reloadKey]);

  const reload = () => setReloadKey((k) => k + 1);

  async function onIncrement() {
    if (!incRow) return;
    try {
      await incrementSalary(incRow.id, Number(percent), reason);
      notifications.show({ color: 'green', message: 'Salary updated' });
      setIncRow(null);
      reload();
    } catch (e) {
      notifications.show({ color: 'red', message: (e as Error).message });
    }
  }

  async function onDeactivate(row: Employee) {
    try {
      await deactivateEmployee(row.id);
      notifications.show({ message: `${row.name} deactivated` });
      reload();
    } catch (e) {
      notifications.show({ color: 'red', message: (e as Error).message });
    }
  }

  return (
    <>
      <Group mb="md" grow>
        <TextInput placeholder="Search name/email" value={search} onChange={(e) => { setSearch(e.target.value); setPage(1); }} />
        <TextInput placeholder="Dept (e.g. Eng)" value={dept} onChange={(e) => { setDept(e.target.value); setPage(1); }} />
        <TextInput placeholder="Country (e.g. IN)" value={country} onChange={(e) => { setCountry(e.target.value.toUpperCase()); setPage(1); }} />
        <EmployeeCreateModal onCreated={reload} />
      </Group>
      <Text size="sm" c="dimmed" mb="xs">{total} employees</Text>
      <Table striped withTableBorder>
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Name</Table.Th><Table.Th>Email</Table.Th><Table.Th>Dept</Table.Th>
            <Table.Th>Salary</Table.Th><Table.Th>Status</Table.Th><Table.Th>Actions</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {rows.map((r) => (
            <Table.Tr key={r.id}>
              <Table.Td>{r.name}</Table.Td>
              <Table.Td>{r.email}</Table.Td>
              <Table.Td>{r.department}</Table.Td>
              <Table.Td>{r.base_salary} {r.currency}</Table.Td>
              <Table.Td>{r.status}</Table.Td>
              <Table.Td>
                <Group gap="xs">
                  <Button size="xs" variant="light" onClick={() => setEditRow(r)}>Edit</Button>
                  <Button size="xs" variant="light" onClick={() => setIncRow(r)}>+%</Button>
                  <Button size="xs" variant="subtle" color="red" onClick={() => void onDeactivate(r)}>Offboard</Button>
                </Group>
              </Table.Td>
            </Table.Tr>
          ))}
        </Table.Tbody>
      </Table>
      <Pagination mt="md" value={page} onChange={setPage} total={Math.max(1, Math.ceil(total / PAGE_SIZE))} />

      <Modal opened={editRow !== null} onClose={() => setEditRow(null)} title="Edit employee">
        <EditForm row={editRow} onSaved={() => { setEditRow(null); reload(); }} />
      </Modal>
      <Modal opened={incRow !== null} onClose={() => setIncRow(null)} title={`Increment — ${incRow?.name ?? ''}`}>
        <NumberInput
          label="Percent (0–100)"
          value={percent}
          onChange={(v) => setPercent(typeof v === 'number' ? v : Number(v) || 0)}
          min={0}
          max={100}
        />
        <TextInput label="Reason" value={reason} onChange={(e) => setReason(e.target.value)} mt="sm" />
        <Button mt="md" onClick={() => void onIncrement()}>Apply</Button>
      </Modal>
    </>
  );
}

function EditForm({ row, onSaved }: { row: Employee | null; onSaved: () => void }) {
  const [dept, setDept] = useState(row?.department ?? '');
  const [title, setTitle] = useState(row?.job_title ?? '');
  useEffect(() => {
    setDept(row?.department ?? '');
    setTitle(row?.job_title ?? '');
  }, [row]);
  if (!row) return null;
  return (
    <>
      <TextInput label="Department" value={dept} onChange={(e) => setDept(e.target.value)} />
      <TextInput label="Job title" value={title} onChange={(e) => setTitle(e.target.value)} mt="sm" />
      <Select label="Status" value={row.status} data={['active', 'inactive']} onChange={() => {}} mt="sm" />
      <Button
        mt="md"
        onClick={() => {
          updateEmployee(row.id, { department: dept, job_title: title })
            .then(onSaved)
            .catch((e: Error) => notifications.show({ color: 'red', message: e.message }));
        }}
      >
        Save
      </Button>
    </>
  );
}
