import { AppShell, Burger, Group, NavLink, Title } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { Link, Outlet, useLocation } from "react-router-dom";

export function Layout() {
  const [opened, { toggle }] = useDisclosure(false);
  const { pathname } = useLocation();
  return (
    <AppShell
      header={{ height: 56 }}
      navbar={{ width: 220, breakpoint: "sm", collapsed: { mobile: !opened } }}
    >
      <AppShell.Header>
        <Group h="100%" px="md">
          <Burger opened={opened} onClick={toggle} hiddenFrom="sm" size="sm" />
          <Title order={4}>ACME Salary Management</Title>
        </Group>
      </AppShell.Header>
      <AppShell.Navbar p="md">
        <NavLink
          label="Dashboard"
          component={Link}
          to="/"
          active={pathname === "/"}
        />
        <NavLink
          label="Employees"
          component={Link}
          to="/employees"
          active={pathname.startsWith("/employees")}
        />
        <NavLink
          label="Exchange rates"
          component={Link}
          to="/rates"
          active={pathname.startsWith("/rates")}
        />
      </AppShell.Navbar>
      <AppShell.Main>
        <Outlet />
      </AppShell.Main>
    </AppShell>
  );
}
