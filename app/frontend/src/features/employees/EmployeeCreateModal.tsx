import { useState } from 'react';
import { Button, Modal, TextInput } from '@mantine/core';
import { notifications } from '@mantine/notifications';
import { createEmployee } from '../../lib/api';

export function EmployeeCreateModal({ onCreated }: { onCreated: () => void }) {
  const [opened, setOpened] = useState(false);
  const [form, setForm] = useState({
    name: '',
    email: '',
    department: 'Eng',
    job_title: 'SDE II',
    country: 'IN',
    currency: 'INR',
    base_salary: '800000.00',
    bonus: '0.00',
    joining_date: '2023-01-15',
  });

  function set(key: string, value: string) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  async function submit() {
    try {
      await createEmployee({ ...form });
      notifications.show({ color: 'green', message: 'Employee created' });
      setOpened(false);
      onCreated();
    } catch (e) {
      notifications.show({ color: 'red', message: (e as Error).message });
    }
  }

  return (
    <>
      <Button onClick={() => setOpened(true)}>New employee</Button>
      <Modal opened={opened} onClose={() => setOpened(false)} title="New employee">
        <TextInput label="Name" value={form.name} onChange={(e) => set('name', e.target.value)} />
        <TextInput label="Email" value={form.email} onChange={(e) => set('email', e.target.value)} mt="sm" />
        <TextInput label="Department" value={form.department} onChange={(e) => set('department', e.target.value)} mt="sm" />
        <TextInput label="Job title" value={form.job_title} onChange={(e) => set('job_title', e.target.value)} mt="sm" />
        <TextInput label="Base salary" value={form.base_salary} onChange={(e) => set('base_salary', e.target.value)} mt="sm" />
        <Button mt="md" onClick={() => void submit()}>Create</Button>
      </Modal>
    </>
  );
}
