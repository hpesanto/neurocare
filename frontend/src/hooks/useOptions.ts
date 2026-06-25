import { useQuery } from "@tanstack/react-query";
import api from "../api/client";

interface Option {
  value: string;
  label: string;
}

export function useOptions(endpoint: string, labelField: string = "nome") {
  const { data, isLoading } = useQuery<Option[]>({
    queryKey: ["options", endpoint],
    queryFn: async () => {
      const res = await api.get(endpoint, { params: { page_size: 1000 } });
      const results = res.data.results ?? res.data;
      return results.map((item: Record<string, unknown>) => ({
        value: String(item.id),
        label: String(item[labelField] ?? item.id),
      }));
    },
    staleTime: 60_000,
  });

  return { options: data ?? [], isLoading };
}
