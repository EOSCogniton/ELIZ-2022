%% Lecture du fichier CSV et extraction des données

% Nom du fichier CSV
nomFichier = 'power_axel_50Nm.csv';

% Lecture complète du fichier à partir de la ligne 66
opts = detectImportOptions(nomFichier, 'NumHeaderLines', 65);

% Lecture des données
data = readtable(nomFichier, opts);

% Récupération du temps et de la puissance
temps = data{:, 2};         % Colonne B → temps [s]
puissance_hp = data{:, 10}; % Colonne J → puissance [hp]

%% Conversion en kW
puissance_kW = puissance_hp * 0.7457; % 1 hp = 0.7457 kW

%% Calcul de l'énergie en kWh
energie_kWh = trapz(temps, puissance_kW) / 3600; % (kW·s)/3600 → kWh

%% Tracé de la puissance en fonction du temps avec énergie en annotation
figure;
plot(temps, puissance_kW, 'b', 'LineWidth', 1.5);
xlabel('Temps [s]');
ylabel('Puissance [kW]');
title(sprintf('Puissance moteur (Énergie totale : %.3f kWh)', energie_kWh));
grid on;
