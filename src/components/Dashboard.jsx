import { mockStats } from "../data/mock";

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <p>Vue d'ensemble de vos projets et statistiques</p>
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Projets actifs</h3>
          <p>{mockStats.activeProjects}</p>
          <span>{mockStats.trends.projects}</span>
        </div>
        <div className="stat-card">
          <h3>Tâches terminées</h3>
          <p>{mockStats.completedTasks}</p>
          <span>{mockStats.trends.tasks}</span>
        </div>
        <div className="stat-card">
          <h3>Heures travaillées</h3>
          <p>{mockStats.workedHours}</p>
          <span>{mockStats.trends.hours}</span>
        </div>
        <div className="stat-card">
          <h3>Taux de complétion</h3>
          <p>{mockStats.completionRate}</p>
          <span>{mockStats.trends.completion}</span>
        </div>
      </div>
      <button className="new-project-btn">+ Créer votre premier projet</button>
    </div>
  );
}
