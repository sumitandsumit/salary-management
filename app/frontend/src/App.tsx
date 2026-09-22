import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Layout } from "./components/Layout";
import { Dashboard } from "./pages/Dashboard";
import { Employees } from "./pages/Employees";
import { Rates } from "./pages/Rates";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="employees" element={<Employees />} />
          <Route path="rates" element={<Rates />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
