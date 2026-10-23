
import {
  CircleMarker,
  MapContainer,
  Popup,
  TileLayer,
  useMap,
} from "react-leaflet";
import { useEffect } from "react";
import type { LayoffMapItem } from "../types/layoff";

interface LayoffMapProps {
  items: LayoffMapItem[];
  selectedId: number | null;
  onSelect: (id: number) => void;
}

function FitIndia() {
  const map = useMap();

  useEffect(() => {
    map.setView([22.5, 79], 5);
  }, [map]);

  return null;
}

export function LayoffMap({
  items,
  selectedId,
  onSelect,
}: LayoffMapProps) {
  return (
    <MapContainer
      center={[22.5, 79]}
      zoom={5}
      minZoom={4}
      maxZoom={12}
      scrollWheelZoom
      className="layoff-map"
    >
      <FitIndia />

      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {items.map((item) => {
        const isSelected = item.id === selectedId;
        const isOfficeReference =
          item.locationStatus === "OFFICE_REFERENCE";

        return (
          <CircleMarker
            key={item.id}
            center={[item.latitude, item.longitude]}
            radius={isSelected ? 10 : 7}
            pathOptions={{
              color: isOfficeReference ? "#e5a34b" : "#55c7a5",
              fillColor: isOfficeReference ? "#e5a34b" : "#55c7a5",
              fillOpacity: 0.9,
              weight: isSelected ? 3 : 1,
            }}
            eventHandlers={{
              click: () => onSelect(item.id),
            }}
          >
            <Popup>
              <strong>{item.companyName}</strong>
              <br />
              {item.employeesAffected == null
                ? "Employee count unknown"
                : `${item.employeesAffected.toLocaleString()} employees affected`}
              <br />
              {item.location ?? "Location unavailable"}
              <br />
              {isOfficeReference
                ? "Company office reference — not a confirmed layoff location"
                : "Reported layoff location"}
              <br />
              <button
                type="button"
                onClick={() => onSelect(item.id)}
              >
                View event details
              </button>
            </Popup>
          </CircleMarker>
        );
      })}
    </MapContainer>
  );
}
