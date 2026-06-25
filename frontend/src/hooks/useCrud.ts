import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import api from "../api/client";

interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export function useCrud<T extends { id: string }>(endpoint: string) {
  const queryClient = useQueryClient();
  const queryKey = [endpoint];

  const list = useQuery<PaginatedResponse<T>>({
    queryKey,
    queryFn: async () => (await api.get(endpoint)).data,
  });

  const create = useMutation({
    mutationFn: async (data: Partial<T>) => (await api.post(endpoint, data)).data as T,
    onSuccess: () => queryClient.invalidateQueries({ queryKey }),
  });

  const update = useMutation({
    mutationFn: async ({ id, ...data }: Partial<T> & { id: string }) =>
      (await api.patch(`${endpoint}${id}/`, data)).data as T,
    onSuccess: () => queryClient.invalidateQueries({ queryKey }),
  });

  const remove = useMutation({
    mutationFn: async (id: string) => {
      await api.delete(`${endpoint}${id}/`);
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey }),
  });

  return {
    items: list.data?.results ?? [],
    count: list.data?.count ?? 0,
    isLoading: list.isLoading,
    error: list.error,
    create: create.mutateAsync,
    update: update.mutateAsync,
    remove: remove.mutateAsync,
    refetch: list.refetch,
  };
}
