#!/bin/bash

# Variables globals per als missatges en diversos idiomes
declare -A MESSAGES=(
    ["select_language_ca"]="Selecciona l'idioma (ca, es, en): "
    ["select_language_es"]="Selecciona el idioma (ca, es, en): "
    ["select_language_en"]="Select language (ca, es, en): "
    ["checking_dependencies_ca"]="Comprovant dependències per desinstal·lar..."
    ["checking_dependencies_es"]="Comprobando dependencias para desinstalar..."
    ["checking_dependencies_en"]="Checking dependencies for uninstallation..."
    ["dependencies_installed_ca"]="Totes les dependències estan instal·lades, però es desinstal·laran."
    ["dependencies_installed_es"]="Todas las dependencias están instaladas, pero serán desinstaladas."
    ["dependencies_installed_en"]="All dependencies are installed, but will be uninstalled."
    ["username_config_ca"]="Configurant el nom d'usuari per desinstal·lar..."
    ["username_config_es"]="Configurando el nombre de usuario para desinstalar..."
    ["username_config_en"]="Configuring username for uninstallation..."
    ["image_dir_config_ca"]="Configurant el directori per eliminar les imatges..."
    ["image_dir_config_es"]="Configurando el directorio para eliminar las imágenes..."
    ["image_dir_config_en"]="Configuring directory to remove images..."
    ["pishrink_setup_ca"]="Eliminant PiShrink..."
    ["pishrink_setup_es"]="Eliminando PiShrink..."
    ["pishrink_setup_en"]="Removing PiShrink..."
    ["checking_pindivil_ca"]="Verificant el fitxer pindivil.py per eliminar..."
    ["checking_pindivil_es"]="Verificando el archivo pindivil.py para eliminar..."
    ["checking_pindivil_en"]="Checking pindivil.py file for removal..."
    ["downloading_pindivil_ca"]="El fitxer pindivil.py no es troba. Eliminant-lo..."
    ["downloading_pindivil_es"]="El archivo pindivil.py no se encuentra. Eliminándolo..."
    ["downloading_pindivil_en"]="The pindivil.py file is missing. Removing it..."
    ["launcher_creation_ca"]="Eliminant el llançador d'aplicació per a Pindivil..."
    ["launcher_creation_es"]="Eliminando el lanzador de aplicación para Pindivil..."
    ["launcher_creation_en"]="Removing application launcher for Pindivil..."
    ["uninstall_complete_ca"]="Desinstal·lació completa. Pindivil ha estat eliminat."
    ["uninstall_complete_es"]="Desinstalación completa. Pindivil ha sido eliminado."
    ["uninstall_complete_en"]="Uninstallation complete. Pindivil has been removed."
    ["remove_dependencies_ca"]="Si vols eliminar les dependències instal·lades, pots executar la següent comanda:"
    ["remove_dependencies_es"]="Si deseas eliminar las dependencias instaladas, puedes ejecutar el siguiente comando:"
    ["remove_dependencies_en"]="If you want to remove the installed dependencies, you can run the following command:"
)

# Funció per imprimir un missatge en l'idioma seleccionat
function print_message() {
    local key="$1"
    echo -e "\n========================================"
    echo -e "${MESSAGES[${key}_${LANGUAGE}]}"
    echo -e "========================================\n"
}

# Preguntar per l'idioma
read -p "Selecciona l'idioma (ca, es, en): " LANGUAGE
LANGUAGE=${LANGUAGE:-ca}

if [[ ! "$LANGUAGE" =~ ^(ca|es|en)$ ]]; then
    LANGUAGE="ca"
    echo "Idioma no vàlid. S'utilitzarà català per defecte."
fi

# Comprovar dependències
print_message "checking_dependencies"
REQUIRED_PKG=("git" "python3" "lsblk" "xterm" "python3-venv")
for pkg in "${REQUIRED_PKG[@]}"; do
    if ! command -v $pkg &> /dev/null; then
        echo "Error: La comanda $pkg no està disponible. Assegura't que $pkg estigui instal·lat."
        exit 1
    fi
done
print_message "dependencies_installed"

# Configuració del nom d'usuari
print_message "username_config"
read -p "Introdueix el nom d'usuari (per defecte: pi): " USERNAME
USERNAME=${USERNAME:-pi}

USER_HOME="/home/$USERNAME"
INSTALL_DIR="$USER_HOME/pindivil"
IMAGE_DIR="$USER_HOME/images"
DESKTOP_FILE="$USER_HOME/.local/share/applications/pindivil.desktop"
PISHRINK_PATH="/usr/local/bin/pishrink"
PINDIVIL_FILE="$INSTALL_DIR/pindivil.py"
PI_SHRINK_DIR="$USER_HOME/PiShrink"

# Verificar i eliminar fitxers i directoris relacionats
print_message "checking_pindivil"
if [ -f "$PINDIVIL_FILE" ]; then
    echo "Eliminant el fitxer pindivil.py..."
    rm -f "$PINDIVIL_FILE"
fi

if [ -d "$PI_SHRINK_DIR" ]; then
    echo "Eliminant el directori PiShrink..."
    rm -rf "$PI_SHRINK_DIR"
fi

if [ -f "$DESKTOP_FILE" ]; then
    echo "Eliminant el llançador d'aplicació..."
    rm -f "$DESKTOP_FILE"
fi

if [ -d "$IMAGE_DIR" ]; then
    echo "Eliminant el directori d'imatges..."
    rm -rf "$IMAGE_DIR"
fi

if [ -f "$PISHRINK_PATH" ]; then
    echo "Eliminant PiShrink..."
    sudo rm -f "$PISHRINK_PATH"
fi

# Finalització
print_message "uninstall_complete"

# Mostrar comandes per eliminar les dependències
print_message "remove_dependencies"

# Mostrar el comando para desinstalar las dependencias
echo -e "\n========================================"
echo -e "sudo apt-get remove --purge git python3 lsblk xterm python3-venv"
echo -e "========================================"
