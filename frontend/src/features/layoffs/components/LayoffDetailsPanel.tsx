
import { X } from "lucide-react";
import { useLayoffDetails } from "../hooks/useLayoffDetails";

interface LayoffDetailsPanelProps {
  id: number;
  onClose: () => void;
}

export function LayoffDetailsPanel({
  id,
  onClose,
}: LayoffDetailsPanelProps) {
  const { data, isLoading, isError } = useLayoffDetails(id);

  return (
    <aside className="details-panel" aria-label="Layoff event details">
      <div className="details-header">
        <div>
          <p className="eyebrow">EVENT DETAILS</p>
          <h2>Layoff report</h2>
        </div>

        <button
          className="icon-button"
          type="button"
          onClick={onClose}
          aria-label="Close event details"
        >
          <X size={18} />
        </button>
      </div>

      {isLoading && <p>Loading event details…</p>}

      {isError && (
        <p role="alert">
          Could not load this event. Please try again.
        </p>
      )}

      {data && (
        <div className="details-content">
          <h3>{data.companyName}</h3>

          <p className="details-location">
            {data.location ?? "Location not reported"}
            {data.country ? `, ${data.country}` : ""}
          </p>

          <div className="details-stat">
            <span>Employees affected</span>
            <strong>
              {data.employeesAffected == null
                ? "Unknown"
                : data.employeesAffected.toLocaleString()}
            </strong>
          </div>

          <div className="details-stat">
            <span>Reported date</span>
            <strong>{data.layoffDate ?? "Not reported"}</strong>
          </div>

          <div className="details-stat">
            <span>Location classification</span>
            <strong>
              {data.locationStatus
                ? data.locationStatus.replaceAll("_", " ")
                : "UNKNOWN"}
            </strong>
          </div>

          {data.locationStatus === "OFFICE_REFERENCE" && (
            <p className="inline-disclaimer">
              This marker identifies a company office, not a confirmed
              location of the layoffs.
            </p>
          )}

          <section className="details-section">
            <h4>Reported reason</h4>
            <p>{data.reason || "No reason reported."}</p>
          </section>

          <section className="details-section">
            <h4>Headquarters</h4>
            <p>{data.headquarters || "Not reported."}</p>
          </section>

          <section className="details-section">
            <h4>Sources</h4>

            {data.sources?.length ? (
              <ul className="source-list">
                {data.sources.map((source) => (
                  <li key={source}>
                    <a href={source} target="_blank" rel="noreferrer">
                      Read source
                    </a>
                  </li>
                ))}
              </ul>
            ) : (
              <p>No source links available.</p>
            )}
          </section>
        </div>
      )}
    </aside>
  );
}
