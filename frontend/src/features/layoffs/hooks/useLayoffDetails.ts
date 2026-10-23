
import { useQuery } from "@tanstack/react-query";
import { layoffsAPI } from "../api/layoffsApi";

export function useLayoffDetails(id: number | null) {
  return useQuery({
    queryKey: ["layoffs", "details", id],
    queryFn: () => layoffsAPI.getDetails(id!),
    enabled: id !== null,
  });
}
