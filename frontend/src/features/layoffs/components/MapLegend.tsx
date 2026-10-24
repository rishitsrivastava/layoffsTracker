
export function MapLegend() {
  return (
    <div className="map-legend" aria-label="Map legend">
      <span className="legend-item">
        <span className="legend-dot confirmed" />
        Confirmed layoff location
      </span>

      <span className="legend-item">
        <span className="legend-dot office-reference" />
        Company office reference
      </span>
    </div>
  );
}
