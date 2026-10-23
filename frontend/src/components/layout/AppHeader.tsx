import { Activity, MapPinned } from "lucide-react";

export function AppHeader() {
  return (
    <header className="app-header">
      <a className="brand" href="/" aria-label="LayoffsIndia home">
        <span className="brand-icon">
          <Activity size={20} />
        </span>

        <span>
          <strong>LayoffsIndia</strong>
          <span className="brand-subtitle">Workforce intelligence</span>
        </span>
      </a>

      <div className="header-context">
        <MapPinned size={16} />
        <span>India · Layoff tracker</span>
      </div>
    </header>
  );
}