
import { useState } from "react";
import { AlertCircle } from "lucide-react";
import { LayoffMap } from "../components/LayoffMap";
import { LayoffDetailsPanel } from "../components/LayoffDetailsPanel";
import { MapLegend } from "../components/MapLegend";
import { useLayoffMap } from "../hooks/useLayoffMap";

export function LayoffsMapPage() {
  const [selectedId, setSelectedId] = useState<number | null>(null);

  const { data, isLoading, isError, error, refetch } = useLayoffMap();

  return (
    <section className="map-page">
      <div className="page-heading">
        <div>
          <p className="eyebrow">PUBLIC DATA · INDIA</p>
          <h1>Layoffs across India</h1>
          <p className="page-description">
            Explore reported workforce reductions and their supporting sources.
          </p>
        </div>

        <div className="event-count">
          <strong>{data?.length ?? "—"}</strong>
          <span>Mapped events</span>
        </div>
      </div>

      <MapLegend />

      {isLoading ? (
        <div className="map-state">Loading map data…</div>
      ) : isError ? (
        <div className="map-state" role="alert">
          <AlertCircle size={24} />
          <h2>Unable to load map data</h2>
          <p>{error.message}</p>
          <button type="button" onClick={() => refetch()}>
            Try again
          </button>
        </div>
      ) : (
        <div className="map-workspace">
          <div className="map-frame">
            <LayoffMap
              items={data ?? []}
              selectedId={selectedId}
              onSelect={setSelectedId}
            />
          </div>

          {selectedId !== null && (
            <LayoffDetailsPanel
              id={selectedId}
              onClose={() => setSelectedId(null)}
            />
          )}
        </div>
      )}

      <p className="location-disclaimer">
        Some markers represent company-office locations rather than confirmed
        layoff locations. Check each event's location status.
      </p>
    </section>
  );
}
