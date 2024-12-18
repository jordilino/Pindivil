#!/bin/bash

# Variables globals per als missatges en diversos idiomes
declare -A MESSAGES=(
    ["installing_ca"]="Instal·lant Pindivil..."
    ["installing_es"]="Instalando Pindivil..."
    ["installing_en"]="Installing Pindivil..."
    ["copying_files_ca"]="Copiant els fitxers necessaris..."
    ["copying_files_es"]="Copiando los archivos necesarios..."
    ["copying_files_en"]="Copying required files..."
    ["setting_permissions_ca"]="Establint permisos d'execució..."
    ["setting_permissions_es"]="Estableciendo permisos de ejecución..."
    ["setting_permissions_en"]="Setting execution permissions..."
    ["creating_launcher_ca"]="Creant el llançador d'aplicació..."
    ["creating_launcher_es"]="Creando el lanzador de aplicación..."
    ["creating_launcher_en"]="Creating application launcher..."
    ["install_complete_ca"]="Pindivil s'ha instal·lat correctament."
    ["install_complete_es"]="Pindivil ha sido instalado correctamente."
    ["install_complete_en"]="Pindivil has been installed successfully."
)

# Funció per imprimir un missatge en l'idioma seleccionat
function print_message() {
    local key="$1"
    echo -e "\n========================================"
    echo -e "${MESSAGES[${key}_${LANGUAGE}]}"
    echo -e "========================================\n"
}

# Preguntar per l'idioma
echo "Selecciona l'idioma - Seleccionar Idioma - Language Selector:"
echo "1. Català (ca)"
echo "2. Español (es)"
echo "3. English (en)"
read -p "Introdueix el número - Introducir numero - Introduce number:" LANG_NUM

# Assignar idioma basat en la selecció
case $LANG_NUM in
    1) LANGUAGE="ca" ;;
    2) LANGUAGE="es" ;;
    3) LANGUAGE="en" ;;
    *) LANGUAGE="ca" ;; # per defecte
esac

# Obtenir el directori del script
script_dir="$(cd "$(dirname \"${BASH_SOURCE[0]}\")" && pwd)"

# Mostrar missatge d'inici d'instal·lació
print_message "installing"

# Copiar fitxers al directori /usr/local/bin
print_message "copying_files"
sudo cp "$script_dir/pindivil.py" /usr/local/bin/pindivil
sudo cp "$script_dir/pindivil.png" /usr/local/bin/pindivil.png
sudo cp "$script_dir/pindivil_icon64x64.png" /usr/local/bin/pindivil_icon64x64.png
sudo cp "$script_dir/pindivil_large_icon.png" /usr/local/bin/pindivil_large_icon.png

# Donar permisos d'execució al script principal
print_message "setting_permissions"
sudo chmod +x /usr/local/bin/pindivil

# Crear un fitxer d'escriptori per facilitar l'accés
print_message "creating_launcher"
desktop_entry="[Desktop Entry]
Name=Pindivil
Exec=pkexec python3 /usr/local/bin/pindivil
Icon=/usr/local/bin/pindivil_icon64x64.png
Type=Application
Categories=Utility;"

echo "$desktop_entry" | sudo tee /usr/share/applications/pindivil.desktop > /dev/null

# Informar l'usuari
print_message "install_complete"
