import { useEffect, useState } from "react";
import {
  Button,
  Container,
  Modal,
  NumberInput,
  Table,
  Text,
  TextInput,
  Title,
} from "@mantine/core";
import { notifications } from "@mantine/notifications";
import { listRates, updateRate } from "../lib/api";
import type { Rate } from "../lib/types";

export function Rates() {
  const [rows, setRows] = useState<Rate[]>([]);
  const [error, setError] = useState("");
  const [editRow, setEditRow] = useState<Rate | null>(null);
  const [rate, setRate] = useState<number>(0);
  const [day, setDay] = useState("");
  const [reason, setReason] = useState("");
  const [loaded, setLoaded] = useState(false);

  async function load() {
    try {
      setRows(await listRates());
    } catch (e) {
      setError((e as Error).message);
    }
    setLoaded(true);
  }

  useEffect(() => {
    void load();
  }, []);

  function openEdit(row: Rate) {
    setEditRow(row);
    setRate(Number(row.rate_to_usd));
    setDay(row.effective_date);
    setReason("");
  }

  async function save() {
    if (!editRow) return;
    try {
      await updateRate(editRow.currency_code, rate, day, reason || undefined);
      notifications.show({
        color: "green",
        message: `${editRow.currency_code} rate updated`,
      });
      setEditRow(null);
      await load();
    } catch (e) {
      notifications.show({ color: "red", message: (e as Error).message });
    }
  }

  if (error) return <Text c="red">Failed to load rates: {error}</Text>;

  return (
    <Container size="xl" py="xl">
      <Title order={2} mb="xs">
        Exchange rates
      </Title>
      <Text size="sm" c="dimmed" mb="xl">
        Rate converts local salary to USD on read. Dashboard shows the rate date
        in use.
      </Text>

      {!loaded && <div className="shimmer" style={{ height: 260 }} />}

      <Table
        striped
        withTableBorder
        className="row-hover"
        mb="xl"
        layout="fixed"
      >
        <Table.Thead>
          <Table.Tr>
            <Table.Th>Currency</Table.Th>
            <Table.Th>Rate to USD</Table.Th>
            <Table.Th>Effective date</Table.Th>
            <Table.Th>Actions</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {rows.map((r, i) => (
            <Table.Tr
              key={r.currency_code}
              className="animate-slide-in"
              style={{
                animationDelay: `${i * 80}ms`,
                animationFillMode: "both",
              }}
            >
              <Table.Td>{r.currency_code}</Table.Td>
              <Table.Td>{r.rate_to_usd}</Table.Td>
              <Table.Td>{r.effective_date}</Table.Td>
              <Table.Td>
                <Button
                  size="sm"
                  variant="light"
                  className="btn-press"
                  onClick={() => openEdit(r)}
                >
                  Edit
                </Button>
              </Table.Td>
            </Table.Tr>
          ))}
        </Table.Tbody>
      </Table>

      <Modal
        opened={editRow !== null}
        onClose={() => setEditRow(null)}
        title={`Edit rate — ${editRow?.currency_code ?? ""}`}
        size="md"
      >
        <NumberInput
          label="Rate to USD"
          value={rate}
          onChange={(v) => setRate(typeof v === "number" ? v : Number(v) || 0)}
          min={0}
          decimalScale={6}
        />
        <TextInput
          label="Effective date"
          type="date"
          value={day}
          onChange={(e) => setDay(e.target.value)}
          mt="sm"
        />
        <TextInput
          label="Reason (optional)"
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          mt="sm"
        />
        <Button mt="md" className="btn-press" onClick={() => void save()}>
          Save rate
        </Button>
      </Modal>
    </Container>
  );
}
