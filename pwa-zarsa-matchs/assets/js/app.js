// ===============================================
// 1. DÉFINITION DES SÉLECTEURS, VARIABLES GLOBALES ET CHARGEMENT
// ===============================================

const DATA_URL = "/data/matches.json";
let ALL_MATCHES = [];
const ELEMENTS = {
  prochainsMatchs: document.getElementById("prochains-matchs"),
  statsZarsaA: document.getElementById("stats-zarsa-a"),
  calendrierZarsaA: document
    .getElementById("calendrier-zarsa-a")
    .querySelector(".match-list"),
  calendrierZarsaB: document
    .getElementById("calendrier-zarsa-b")
    .querySelector(".match-list"),
  statsZarsaB: document.getElementById("calendrier-zarsa-b").parentElement,
};

// Stockage de l'état des filtres (Statut + Compétition)
let currentFilters = {
  "Zarsa A": { statut: "all", competition: "all" },
  "Zarsa B": { statut: "all", competition: "all" },
};

/**
 * Fonction principale : Charge les données et lance l'affichage.
 */
async function initApp() {
  try {
    const response = await fetch(DATA_URL);
    const matches = await response.json();

    matches.sort((a, b) => new Date(a.date) - new Date(b.date));

    ALL_MATCHES = matches;

    const zarsaA = matches.filter((m) => m.equipe === "Zarsa A");
    const zarsaB = matches.filter((m) => m.equipe === "Zarsa B");

    // Affichage initial
    displayProchainsMatchs(zarsaA, zarsaB);
    displayCalendrier(zarsaA, ELEMENTS.calendrierZarsaA);
    displayCalendrier(zarsaB, ELEMENTS.calendrierZarsaB);

    // Stats et Bilans
    displayStatsAndClassementA(zarsaA);
    displayStatsBilanB(zarsaB);

    // Initialisation des fonctionnalités
    setupFilters();
    displayLastUpdateInfo();
  } catch (error) {
    console.error(
      "Erreur lors du chargement ou du traitement des données:",
      error
    );
    // Affichage d'un message d'erreur si la récupération échoue (par exemple, si matches.json est mal formaté ou introuvable)
    ELEMENTS.prochainsMatchs.innerHTML =
      '<p class="error">Impossible de charger les données des matchs. Vérifiez la connexion ou le cache.</p>';
  }
}

// ===============================================
// 2. LOGIQUE D'AFFICHAGE ET CARTE DE MATCH (Fonctions complètes)
// ===============================================

function displayProchainsMatchs(zarsaA, zarsaB) {
  const now = new Date();

  // N'affichez que les matchs futurs
  const prochainsA = zarsaA.filter((m) => new Date(m.date) > now).slice(0, 2);
  const prochainsB = zarsaB.filter((m) => new Date(m.date) > now).slice(0, 2);

  const prochainsAHtml = prochainsA
    .map((m) => createMatchCard(m, true))
    .join("");
  const prochainsBHtml = prochainsB
    .map((m) => createMatchCard(m, true))
    .join("");

  ELEMENTS.prochainsMatchs.innerHTML = `
        <h2>Prochains Matchs Importants</h2>
        <div class="prochains-list">
            <div class="prochains-equipe">
                <h4>Zarsa A (Seniors)</h4>
                ${prochainsAHtml || "<p>Pas de match senior à venir.</p>"}
            </div>
            <div class="prochains-equipe">
                <h4>Zarsa B (Vétérans)</h4>
                ${prochainsBHtml || "<p>Pas de match vétéran à venir.</p>"}
            </div>
        </div>
    `;
}

function displayCalendrier(matches, containerElement) {
  const html = matches.map((m) => createMatchCard(m, false)).join("");
  containerElement.innerHTML = html;
}

function createMatchCard(match, isHighlight) {
  const dateObj = new Date(match.date);
  const dateStr = dateObj.toLocaleDateString("fr-FR", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
  const timeStr =
    match.statut !== "Terminé"
      ? dateObj.toLocaleTimeString("fr-FR", {
          hour: "2-digit",
          minute: "2-digit",
        })
      : "";

  let statutHtml = "";
  let cssClass = "match-card";

  if (match.statut === "Terminé") {
    const diff = match.score_zarsa - match.score_adverse;
    const vainqueur = diff > 0 ? "Victoire" : diff < 0 ? "Défaite" : "Nul";
    statutHtml = `<span class="score">${match.score_zarsa} - ${
      match.score_adverse
    }</span> <span class="result ${vainqueur.toLowerCase()}">${vainqueur}</span>`;
    cssClass += " finished";
  } else {
    statutHtml = `<span class="location">${
      match.domicile ? "Domicile" : "Extérieur"
    }</span>`;
    cssClass += " upcoming";
  }

  if (isHighlight) cssClass += " highlight";

  return `
        <div class="${cssClass}">
            <div class="match-info">
                <span class="team">${match.equipe} (${match.competition})</span>
                <span class="date">${dateStr} ${
    timeStr ? "à " + timeStr : ""
  }</span>
                <span class="adverse">vs ${match.adverse}</span>
            </div>
            <div class="match-statut">
                ${statutHtml}
            </div>
        </div>
    `;
}

// ===============================================
// 3. LOGIQUE D'AFFICHAGE DU CLASSEMENT A ET TIMELINE
// ===============================================

function displayStatsAndClassementA(zarsaAMatches) {
  const matchsTermines = zarsaAMatches.filter((m) => m.statut === "Terminé");

  // --- Calcul des stats pour ZARSA A ---
  let stats = { V: 0, N: 0, D: 0, BP: 0, BC: 0, Pts: 0 };
  let forme = [];

  matchsTermines.forEach((m) => {
    const diff = m.score_zarsa - m.score_adverse;
    stats.BP += m.score_zarsa;
    stats.BC += m.score_adverse;

    if (diff > 0) {
      stats.V++;
      stats.Pts += 3;
      forme.push("V");
    } else if (diff === 0) {
      stats.N++;
      stats.Pts += 1;
      forme.push("N");
    } else {
      stats.D++;
      forme.push("D");
    }
  });

  const J = matchsTermines.length;
  stats.J = J;
  stats.Diff = stats.BP - stats.BC;

  // --- TIMELINE D'ÉVOLUTION (5 derniers matchs) ---
  const lastFive = forme.slice(-5).reverse();
  const timelineHtml = lastFive
    .map(
      (r) => `
        <span class="timeline-result result-${r.toLowerCase()}">${r}</span>
    `
    )
    .join("");

  // --- Calculs Avancés ---
  const ratioPoints = J > 0 ? (stats.Pts / J).toFixed(1) : 0;

  // --- Génération de l'affichage du Bilan ---
  const bilanHtml = `
        <div class="bilan-summary">
            <p><strong>Ratio Pts/Match:</strong> <strong>${ratioPoints}</strong></p>
            <p><strong>Forme (5 derniers):</strong> ${timelineHtml}</p>
            <p><strong>Matchs Joués:</strong> ${J}</p>
            <p><strong>Victoires:</strong> <span class="stat-V">${
              stats.V
            }</span></p>
            <p><strong>Nuls:</strong> <span class="stat-N">${stats.N}</span></p>
            <p><strong>Défaites:</strong> <span class="stat-D">${
              stats.D
            }</span></p>
            <p><strong>Buts (P/C):</strong> ${stats.BP}/${stats.BC}</p>
            <p><strong>Différence:</strong> ${stats.Diff > 0 ? "+" : ""}${
    stats.Diff
  }</p>
            <p><strong>Points:</strong> <strong>${stats.Pts}</strong></p>
        </div>
        
        <div class="stats-complementaires">
            ${displayButeursSimules()}
        </div>
    `;
  ELEMENTS.statsZarsaA.querySelector(".stats-summary").innerHTML = bilanHtml;

  // --- Simulation du Classement Détaillé ---
  const autresEquipes = [
    {
      Nom: "FC Riviera",
      J: 6,
      V: 4,
      N: 1,
      D: 1,
      BP: 12,
      BC: 5,
      Diff: 7,
      Pts: 13,
    },
    { Nom: "AS Port", J: 6, V: 3, N: 2, D: 1, BP: 9, BC: 7, Diff: 2, Pts: 11 },
    {
      Nom: "Olympique V",
      J: 6,
      V: 1,
      N: 1,
      D: 4,
      BP: 6,
      BC: 15,
      Diff: -9,
      Pts: 4,
    },
  ];

  const zarsaAData = {
    Nom: "Zarsa A",
    J: stats.J,
    V: stats.V,
    N: stats.N,
    D: stats.D,
    BP: stats.BP,
    BC: stats.BC,
    Diff: stats.Diff,
    Pts: stats.Pts,
  };
  let classement = [zarsaAData, ...autresEquipes];

  classement.sort((a, b) => {
    if (b.Pts !== a.Pts) return b.Pts - a.Pts;
    return b.Diff - a.Diff;
  });

  const classementHtml = classement
    .map(
      (team, index) => `
        <tr class="${team.Nom === "Zarsa A" ? "highlight-team" : ""}">
            <td>${index + 1}</td>
            <td>${team.Nom}</td>
            <td>${team.J}</td>
            <td class="stat-V">${team.V}</td>
            <td class="stat-N">${team.N}</td>
            <td class="stat-D">${team.D}</td>
            <td>${team.BP}</td>
            <td>${team.BC}</td>
            <td>${team.Diff}</td>
            <td class="stat-Pts"><strong>${team.Pts}</strong></td>
        </tr>
    `
    )
    .join("");

  const classementTable = `
        <h3>Classement Zarsa A - Championnat</h3>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Équipe</th>
                    <th>J</th>
                    <th>V</th>
                    <th>N</th>
                    <th>D</th>
                    <th>BP</th>
                    <th>BC</th>
                    <th>Diff</th>
                    <th>Pts</th>
                </tr>
            </thead>
            <tbody>
                ${classementHtml}
            </tbody>
        </table>
    `;

  ELEMENTS.statsZarsaA.querySelector(".classement").innerHTML = classementTable;
}

// ===============================================
// 4. CLASSEMENT ET STATS ZARSA B (Bilan Séparé)
// ===============================================

function displayStatsBilanB(zarsaBMatches) {
  const matchsTermines = zarsaBMatches.filter((m) => m.statut === "Terminé");

  const V = matchsTermines.filter(
    (m) => m.score_zarsa > m.score_adverse
  ).length;
  const N = matchsTermines.filter(
    (m) => m.score_zarsa === m.score_adverse
  ).length;
  const D = matchsTermines.filter(
    (m) => m.score_zarsa < m.score_adverse
  ).length;

  const classementBHtml = `
        <div class="stats-summary stats-veterans">
            <h4>Bilan Zarsa B (Vétérans)</h4>
            <p><strong>Joués:</strong> ${matchsTermines.length}</p>
            <p><strong>Victoires:</strong> ${V}</p>
            <p><strong>Nuls:</strong> ${N}</p>
            <p><strong>Défaites:</strong> ${D}</p>
        </div>
    `;

  const h2B = ELEMENTS.statsZarsaB.querySelector("h2");
  if (h2B) {
    h2B.insertAdjacentHTML("afterend", classementBHtml);
  }
}

// ===============================================
// 5. STATISTIQUES DÉTAILLÉES ET BUTTEURS SIMULÉS
// ===============================================

function displayButeursSimules() {
  const buteurs = [
    { nom: "M. Dubois", buts: 5 },
    { nom: "F. Kante", buts: 3 },
    { nom: "L. Petit", buts: 2 },
  ];

  const buteursHtml = buteurs
    .map(
      (b) => `
        <li>${b.nom}: <strong>${b.buts} buts</strong></li>
    `
    )
    .join("");

  return `
        <div class="buteurs-section">
            <h4>Meilleurs Buteurs (Zarsa A)</h4>
            <ul class="top-scorers">
                ${buteursHtml}
            </ul>
        </div>
    `;
}

// ===============================================
// 6. LOGIQUE DE FILTRAGE MULTI-CRITÈRES (Statut + Compétition)
// ===============================================

function setupFilters() {
  // 1. Filtres de Statut (Tous/À Venir/Terminés)
  document.querySelectorAll(".filtres-a, .filtres-b").forEach((container) => {
    container.addEventListener("click", (e) =>
      handleFilterChange(e, container, "statut")
    );
  });

  // 2. Filtres de Compétition (Championnat/Coupe)
  const compNav = document.querySelector(
    "#calendrier-zarsa-a .competitions-nav"
  );
  if (compNav) {
    compNav.addEventListener("click", (e) =>
      handleFilterChange(e, compNav, "competition")
    );
  }
}

function handleFilterChange(e, container, filterType) {
  if (e.target.tagName === "BUTTON") {
    const equipe =
      container.classList.contains("filtres-a") ||
      container.closest("#calendrier-zarsa-a")
        ? "Zarsa A"
        : "Zarsa B";
    const filterValue = e.target.dataset.filter || e.target.dataset.competition;

    // Mise à jour de l'état
    currentFilters[equipe][filterType] = filterValue;

    // Mise à jour visuelle du bouton actif
    container
      .querySelectorAll("button")
      .forEach((btn) => btn.classList.remove("active"));
    e.target.classList.add("active");

    applyFilters(equipe);
  }
}

/**
 * Applique tous les filtres actifs à l'équipe spécifiée et affiche le résultat.
 */
function applyFilters(equipe) {
  const filters = currentFilters[equipe];
  let filteredMatches = ALL_MATCHES.filter((m) => m.equipe === equipe);

  // 1. Filtrage par Compétition
  if (filters.competition !== "all") {
    filteredMatches = filteredMatches.filter((m) =>
      m.competition.includes(filters.competition)
    );
  }

  // 2. Filtrage par Statut
  if (filters.statut === "upcoming") {
    filteredMatches = filteredMatches.filter((m) => m.statut !== "Terminé");
  } else if (filters.statut === "finished") {
    filteredMatches = filteredMatches.filter((m) => m.statut === "Terminé");
  }

  const targetElement =
    equipe === "Zarsa A"
      ? ELEMENTS.calendrierZarsaA
      : ELEMENTS.calendrierZarsaB;
  displayCalendrier(filteredMatches, targetElement);
}

// ===============================================
// 7. FONCTIONNALITÉ DE MISE À JOUR SIMULÉE
// ===============================================

function displayLastUpdateInfo() {
  const updateElement = document.createElement("p");
  const now = new Date();

  const dateStr = now.toLocaleDateString("fr-FR", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  updateElement.innerHTML = `
        <small>Dernière mise à jour des données (Simulée) : <strong>${dateStr}</strong></small>
        <button id="refresh-data" onclick="location.reload()" style="margin-left: 10px;">Actualiser</button>
    `;
  updateElement.style.textAlign = "center";
  updateElement.style.marginTop = "20px";

  document.querySelector("main").appendChild(updateElement);
}

// ===============================================
// 8. LANCEMENT DE L'APPLICATION
// ===============================================

document.addEventListener("DOMContentLoaded", initApp);
