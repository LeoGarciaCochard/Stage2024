-- -- Fonction pour lire le fichier CSV
-- local function read_csv(file_path)
--     local csv = {}
--     local file = io.open(file_path, "r")
--     if not file then
--         print("Erreur : impossible d'ouvrir le fichier CSV")
--         return nil
--     end
--     for line in file:lines() do
--         local row = {}
--         for value in string.gmatch(line, "([^,]+)") do
--             table.insert(row, value)
--         end
--         table.insert(csv, row)
--     end
--     file:close()
--     return csv
-- end

-- -- Fonction pour convertir une table en dictionnaire
-- local function convert_to_dict(csv)
--     local dict = {}
--     if not csv then
--         print("Erreur : CSV est nil")
--         return dict
--     end
--     for i = 2, #csv do  -- Commence à 2 pour ignorer les en-têtes
--         local timecode = tonumber(csv[i][2])
--         local parameter = tonumber(csv[i][3])
--         if timecode and parameter then
--             dict[timecode] = parameter
--         else
--             print("Erreur : valeur non valide à l'index " .. i)
--         end
--     end
--     return dict
-- end

-- -- Initialisation du script
-- function initialize(box)
--     print("Lua script initialized")
-- end

-- -- Déchargement du script
-- function uninitialize(box)
--     print("Lua script uninitialized")
-- end

-- -- Fonction principale du script
-- function process(box)
--     -- Lire le fichier CSV
--     local file_path = "C:/Users/milio/PycharmProjects/Stage/OpenVibe/enregistrement_en_cours/timecodes.csv"  -- Remplacez par le chemin de votre fichier CSV
--     local csv = read_csv(file_path)
    
--     -- Vérifier si le CSV a été correctement lu
--     if not csv then
--         print("Erreur : Impossible de lire le fichier CSV")
--         return
--     end
    
--     -- Convertir le CSV en dictionnaire
--     local timecode_dict = convert_to_dict(csv)
    
--     -- Variables de contrôle des stimulations
--     local stimulations_sent = {}
--     for timecode, parameter in pairs(timecode_dict) do
--         stimulations_sent[timecode] = false
--     end
    
--     while true do
--         -- Obtenir le temps actuel dans le scénario
--         local current_time = box:get_current_time()
        
--         for timecode, parameter in pairs(timecode_dict) do
--             if not stimulations_sent[timecode] and current_time >= timecode and current_time < (timecode + 0.1) then
--                 -- Définir l'identifiant de stimulation en fonction du paramètre
--                 local stimulation_id
--                 if parameter == 0 then
--                     stimulation_id = 0x00008101  -- Label pour paramètre 0
--                 else
--                     stimulation_id = 0x00008102  -- Label pour paramètre 1
--                 end
                
--                 -- Envoyer la stimulation
--                 box:send_stimulation(1, stimulation_id, current_time, 0)
--                 -- Imprimer un message pour le débogage
--                 print("Stimulation sent at " .. timecode .. " seconds with ID: " .. string.format("0x%08x", stimulation_id) .. " and parameter: " .. parameter)
                
--                 -- Marquer la stimulation comme envoyée
--                 stimulations_sent[timecode] = true
--             end
--         end
        
--         -- Pause pour éviter une utilisation excessive du CPU
--         box:sleep()

--         -- Sortir de la boucle si toutes les stimulations ont été envoyées
--         local all_sent = true
--         for timecode, sent in pairs(stimulations_sent) do
--             if not sent then
--                 all_sent = false
--                 break
--             end
--         end
--         if all_sent then
--             break
--         end
--     end
-- end

-- Fonction pour lire le fichier CSV
local function read_csv(file_path)
    local csv = {}
    local file = io.open(file_path, "r")
    if not file then
        print("Erreur : impossible d'ouvrir le fichier CSV")
        return nil
    end
    for line in file:lines() do
        local row = {}
        for value in string.gmatch(line, "([^,]+)") do
            table.insert(row, value)
        end
        table.insert(csv, row)
    end
    file:close()
    return csv
end

-- Fonction pour convertir une table en dictionnaire et trier les timecodes
local function convert_to_dict_and_sort(csv)
    local dict = {}
    local timecodes = {}
    if not csv then
        print("Erreur : CSV est nil")
        return dict, timecodes
    end
    for i = 2, #csv do  -- Commence à 2 pour ignorer les en-têtes
        local id = csv[i][1]
        local timecode = tonumber(csv[i][2])
        local parameter = tonumber(csv[i][3])
        if timecode and parameter then
            dict[timecode] = { id = id, parameter = parameter }
            table.insert(timecodes, timecode)
        else
            print("Erreur : valeur non valide à l'index " .. i)
        end
    end
    table.sort(timecodes)
    return dict, timecodes
end

-- Initialisation du script
function initialize(box)
    print("Lua script initialized")
end

-- Déchargement du script
function uninitialize(box)
    print("Lua script uninitialized")
end

-- Fonction principale du script
function process(box)
    -- Lire le fichier CSV
    local file_path = "C:/Users/milio/PycharmProjects/Stage2024/OpenVibe/enregistrement_en_cours/timecodes.csv"  -- Remplacer par le chemin
    local csv = read_csv(file_path)
    
    -- Vérifier si le CSV a été correctement lu
    if not csv then
        print("Erreur : Impossible de lire le fichier CSV")
        return
    end
    
    -- Convertir le CSV en dictionnaire et trier les timecodes
    local timecode_dict, sorted_timecodes = convert_to_dict_and_sort(csv)
    
    -- Variables de contrôle des stimulations
    local stimulations_sent = {}
    for _, timecode in ipairs(sorted_timecodes) do
        stimulations_sent[timecode] = false
    end
    
    while true do
        -- Obtenir le temps actuel dans le scénario
        local current_time = box:get_current_time()
        
        for _, timecode in ipairs(sorted_timecodes) do
            local stimulation_info = timecode_dict[timecode]
            if not stimulations_sent[timecode] and current_time >= timecode and current_time < (timecode + 0.1) then
                -- Définir l'identifiant de stimulation en fonction du paramètre
                local stimulation_id
                if stimulation_info.parameter == 0 then
                    stimulation_id = 0x00008101  -- Label pour paramètre 0

                elseif  stimulation_info.parameter == 1 then
                    stimulation_id = 0x00008102  -- Label pour paramètre 1

                elseif  stimulation_info.parameter == 2 then
                    stimulation_id = 0x00008103  -- Label pour paramètre 2

                elseif  stimulation_info.parameter == 3 then
                    stimulation_id = 0x00008104  -- Label pour paramètre 3

                elseif  stimulation_info.parameter == 4 then
                    stimulation_id = 0x00008105  -- Label pour paramètre 4

                elseif  stimulation_info.parameter == 5 then
                    stimulation_id = 0x00008106  -- Label pour paramètre 5
                end


                
                -- Envoyer la stimulation
                box:send_stimulation(1, stimulation_id, current_time, 0)
                -- Imprimer un message pour le débogage
                print("Stimulation sent at " .. timecode .. " seconds with ID: " .. string.format("0x%08x", stimulation_id) .. " and parameter: " .. stimulation_info.parameter .. " (ID: " .. stimulation_info.id .. ")")
                
                -- Marquer la stimulation comme envoyée
                stimulations_sent[timecode] = true
            end
        end
        
        -- Pause pour éviter une utilisation excessive du CPU
        box:sleep()

        -- Sortir de la boucle si toutes les stimulations ont été envoyées
        local all_sent = true
        for _, sent in pairs(stimulations_sent) do
            if not sent then
                all_sent = false
                break
            end
        end
        if all_sent then
            break
        end
    end
end
