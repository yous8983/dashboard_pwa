import { create } from "zustand";

export const useStore = create((set) => ({
  stats: {
    activeProjects: 0,
    completedTasks: 248,
    workedHours: "342h",
    completionRate: "78%",
    trends: {
      projects: "+15% vs mois dernier",
      tasks: "+8% vs mois dernier",
      hours: "Ce mois-ci",
      completion: "+12% vs mois dernier",
    },
  },
  // Ajoutez plus tard pour projets, tâches, etc.
  setStats: (newStats) => set({ stats: newStats }),
}));
