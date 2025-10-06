import { useStore } from "../store";
import { Bar } from "react-chartjs-2";
import { motion } from "framer-motion";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default function Dashboard() {
  const { stats } = useStore();

  const chartData = {
    labels: ["Projets", "Tâches", "Heures", "Complétion"],
    datasets: [
      {
        label: "Stats",
        data: [stats.activeProjects, stats.completedTasks, 342, 78], // Parse si besoin
        backgroundColor: ["#4caf50", "#2196f3", "#ff9800", "#9c27b0"],
      },
    ],
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <h1>Dashboard</h1>
      <p>Vue d'ensemble de vos projets et statistiques</p>
      <div className="stats-grid">
        {/* Stat cards comme avant, en utilisant stats */}
      </div>
      <div className="chart-container">
        <Bar data={chartData} options={{ responsive: true }} />
      </div>
      <button className="new-project-btn">+ Créer votre premier projet</button>
    </motion.div>
  );
}
