#!/bin/bash

# Variables globals per als missatges en diversos idiomes
declare -A MESSAGES=(
    ["uninstalling_ca"]="Desinstal·lant Pindivil..."
    ["uninstalling_es"]="Desinstalando Pindivil..."
    ["uninstalling_en"]="Uninstalling Pindivil..."
    ["removing_files_ca"]="Eliminant els fitxers instal·lats..."
    ["removing_files_es"]="Eliminando los archivos instalados..."
    ["removing_files_en"]="Removing installed files..."
    ["removing_launcher_ca"]="Eliminant el llançador d'aplicació..."
    ["removing_launcher_es"]="Eliminando el lanzador de aplicación..."
    ["removing_launcher_en"]="Removing application launcher..."
    ["uninstall_complete_ca"]="Pindivil s'ha desinstal·lat correctament."
    ["uninstall_complete_es"]="Pindivil ha sido desinstalado correctamente."
    ["uninstall_complete_en"]="Pindivil has been uninstalled successfully."
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

# Mostrar missatge d'inici de desinstal·lació
print_message "uninstalling"

# Eliminar fitxers instal·lats
print_message "removing_files"
sudo rm -f /usr/local/bin/pindivil
sudo rm -f /usr/local/bin/pindivil.png

# Eliminar el llançador d'aplicació
print_message "removing_launcher"
sudo rm -f /usr/share/applications/pindivil.desktop

# Informar l'usuari
print_message "uninstall_complete"
