%% Lecture du fichier CSV et extraction des données

% Nom du fichier CSV
nomFichier = 'fsg_2010_v2.csv';

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

%% Calcul de la puissance moyenne
puissance_moy = mean(puissance_kW, 'omitnan'); % Moyenne en kW

%% Tracé de la puissance en fonction du temps avec énergie et puissance moyenne en annotation
figure;
plot(temps, puissance_kW, 'b', 'LineWidth', 1.5); hold on;
yline(puissance_moy, '--k', 'LineWidth', 1.5); % ligne horizontale pour la puissance moyenne
xlabel('Temps [s]');
ylabel('Puissance [kW]');
title(sprintf('Puissance moteur (Énergie totale : %.3f kWh, Puissance moyenne : %.3f kW)', ...
              energie_kWh, puissance_moy));
legend('Puissance [kW]', 'Puissance moyenne');
grid on;

%% --- Nouvelle figure pour la colonne M ---
colM = data{:, 13}; % Colonne M (13e colonne)
valMoy = mean(colM, 'omitnan'); % Calcul de la moyenne

figure;
plot(temps, colM, 'r', 'LineWidth', 1.5); hold on;
yline(valMoy, '--k', 'LineWidth', 1.5); % Ligne horizontale de la moyenne
xlabel('Temps [s]');
ylabel('Valeur colonne M');
title(sprintf('Colonne M (Moyenne = %.3f)', valMoy));
legend('Colonne M', 'Moyenne');
grid on;
