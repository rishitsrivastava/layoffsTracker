
import { useQuery } from "@tanstack/react-query";
import { layoffsAPI } from "../api/layoffsApi";

export function useLayoffMap() {
  return useQuery({
    queryKey: ["layoffs", "map"],
    queryFn: layoffsAPI.getMapItems,
  });
}
