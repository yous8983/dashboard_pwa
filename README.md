# Project Manager PWA

Application de gestion de projets en PWA, avec interface en français.

## Fonctionnalités Principales

### Dashboard
- Affichage de stats globales : projets actifs, tâches terminées, heures travaillées, taux de complétion.
- Bouton pour créer un nouveau projet.
- Indicateurs de progression mensuelle (ex. +15% vs mois dernier).

### Projets
- Liste des projets avec recherche et filtre.
- Création de projet : nom, description, plan/objectifs, fonctionnalités (lignes séparées), statut (Planification, etc.), URL dépôt Git, branche, stack technique (virgules), date d'échéance, taille équipe.
- Édition et suppression de projets.
- Affichage de projets récents ou "Aucun projet".

### Kanban
- Vue board avec colonnes : À faire, En cours, En révision (extensible).
- Création de tâche : projet associé, titre, description, statut, priorité (high/medium/low), assigné à, estimation (ex. 4h, 2j).
- Édition de tâche : modifier titre, description, statut, priorité, etc.
- Drag-and-drop pour déplacer tâches entre colonnes.
- Tags de priorité (couleurs : red high, yellow medium).
- Filtre par projet ou statut.

### Timeline
- Diagramme de Gantt : tâches avec progression (barres colorées, % complétion).
- Time tracking : timers actifs/pausés, enregistrement, suppression.
- Création de timer : tâche associée, description.
- Liste d'entrées récentes de time tracking.
- Vue par semaines (S1 à S12).

### Rapports
- Génération de rapports : temps passé par tâche/projet, complétion.

## Exigences PWA
- Offline support via service worker.
- Installable sur desktop/mobile.
- Manifest pour icône et nom.

## Stack
- Front : React, CSS (dark theme).
- Mocks : JSON local pour données.
- Versioning : Git from scratch.

## Roadmap

Roadmap séquencée pour le développement, avec estimations de temps pour un développeur solo (total approx. 1-2 semaines).

1. **Initialisation (1 jour)**
   - Setup Git et projet React PWA.
   - README avec fonctionnalités.

2. **Structure de Base (2 jours)**
   - Navigation latérale (Dashboard, Projets, Kanban, Timeline, Rapports).
   - Thème dark, layout responsive.

3. **Dashboard (1 jour)**
   - Stats mockées.
   - Bouton nouveau projet.

4. **Gestion Projets (2 jours)**
   - Liste, création, édition.

5. **Kanban (3 jours)**
   - Board, tâches, drag-drop.

6. **Timeline & Time Tracking (3 jours)**
   - Gantt chart (utiliser lib comme react-google-charts).
   - Timers avec état.

7. **PWA Features (1 jour)**
   - Service worker, manifest.

8. **Déploiement (1 jour)**
   - Hébergement (ex. Vercel/Netlify) avec mocks.

9. **Tests & Rafinements (2 jours)**
   - Tests unitaires, responsive, offline.