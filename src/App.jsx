import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Dashboard from "./components/Dashboard";
import Projects from "./components/Projects";
import Kanban from "./components/Kanban";
import Timeline from "./components/Timeline";
import Reports from "./components/Reports";
import "./App.css"; // Si CSS séparé

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="sidebar">
          <h2>Navigation</h2>
          <ul>
            <li>
              <Link to="/">Dashboard</Link>
            </li>
            <li>
              <Link to="/projects">Projets</Link>
            </li>
            <li>
              <Link to="/kanban">Kanban</Link>
            </li>
            <li>
              <Link to="/timeline">Timeline</Link>
            </li>
            <li>
              <Link to="/reports">Rapports</Link>
            </li>
          </ul>
        </nav>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/projects" element={<Projects />} />
            <Route path="/kanban" element={<Kanban />} />
            <Route path="/timeline" element={<Timeline />} />
            <Route path="/reports" element={<Reports />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
