import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import ModelsService from "#/api/models-service/models-service.api";
import { ModelPresetActivateRequest } from "#/api/open-hands.types";

export function useModelPresets() {
  return useQuery({
    queryKey: ["model-presets"],
    queryFn: () => ModelsService.listPresets(),
  });
}

export function useSetActivePreset() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: ModelPresetActivateRequest) =>
      ModelsService.setActivePreset(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["model-presets"] });
    },
  });
}
