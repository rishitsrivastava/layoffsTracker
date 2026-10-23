export type LocationStatus = 
    | "CONFIRMED"
    | "OFFICE_REFERENCE"
    | "UNKNOWN";

export interface LayoffMapItem {
    id: number,
    companyName: string,
    employeesAffected: number | null,
    location: string | null,
    locationStatus: LocationStatus,
    latitude: number,
    longitude: number
}

export interface LayoffDetails extends LayoffMapItem {
    sources: string[] | null,
    country: string;
    headquarters: string | null;
    layoffDate: string | null;
    reason: string | null;
    verificationStatus: string;
    createdAt: string;
    updatedAt: string;
}