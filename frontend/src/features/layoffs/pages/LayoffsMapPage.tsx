import { MapPinned } from "lucide-react";

export function LayoffsMapPage() {
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
      </div>

      <div className="map-placeholder">
        <MapPinned size={40} strokeWidth={1.25} />

        <h2>Your map goes here</h2>

        <p>
          The interactive map will display verified layoff locations and
          clearly distinguish company-office reference locations.
        </p>
      </div>

      <p className="location-disclaimer">
        Some markers may represent company-office locations rather than
        confirmed layoff locations. Check each event's location status.
      </p>
    </section>
  );
}