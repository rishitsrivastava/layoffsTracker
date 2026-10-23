import { AppLayout } from "./components/layout/AppLayout";
import { LayoffsMapPage } from "./features/layoffs/pages/LayoffsMapPage";

export default function App() {
  return (
    <AppLayout>
      <LayoffsMapPage />
    </AppLayout>
  );
}