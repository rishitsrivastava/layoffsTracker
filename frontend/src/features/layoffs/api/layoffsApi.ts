import { apiGet } from "../../../lib/httpClient";
import type { LayoffDetails, LayoffMapItem } from "../types/layoff";

export const layoffsAPI = {
    getMapItems(): Promise<LayoffMapItem[]> {
        return apiGet<LayoffMapItem[]>("/layoffs/map");
    },

    getDetails(id: number): Promise<LayoffDetails> {
        return apiGet<LayoffDetails>(`/layoffs/${id}`);
    }
}