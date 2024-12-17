#!/bin/bash

# Variables globals per als missatges en diversos idiomes
declare -A MESSAGES=(
    ["select_language_ca"]="Selecciona l'idioma (1 - Català, 2 - Español, 3 - English): "
    ["select_language_es"]="Selecciona el idioma (1 - Català, 2 - Español, 3 - English): "
    ["select_language_en"]="Select language (1 - Català, 2 - Español, 3 - English): "
    ["checking_dependencies_ca"]="Comprovant dependències..."
    ["checking_dependencies_es"]="Comprobando dependencias..."
    ["checking_dependencies_en"]="Checking dependencies..."
    ["dependencies_installed_ca"]="Totes les dependències estan instal·lades."
    ["dependencies_installed_es"]="Todas las dependencias están instaladas."
    ["dependencies_installed_en"]="All dependencies are installed."
    ["username_config_ca"]="Configurant el nom d'usuari..."
    ["username_config_es"]="Configurando el nombre de usuario..."
    ["username_config_en"]="Configuring username..."
    ["image_dir_config_ca"]="Configurant el directori per guardar les imatges..."
    ["image_dir_config_es"]="Configurando el directorio para guardar las imágenes..."
    ["image_dir_config_en"]="Configuring directory to save images..."
    ["pishrink_setup_ca"]="Baixant i configurant PiShrink..."
    ["pishrink_setup_es"]="Descargando y configurando PiShrink..."
    ["pishrink_setup_en"]="Downloading and setting up PiShrink..."
    ["checking_pindivil_ca"]="Verificant el fitxer pindivil.py..."
    ["checking_pindivil_es"]="Verificando el archivo pindivil.py..."
    ["checking_pindivil_en"]="Checking pindivil.py file..."
    ["downloading_pindivil_ca"]="El fitxer pindivil.py no es troba. Descarregant-lo des de GitHub..."
    ["downloading_pindivil_es"]="El archivo pindivil.py no se encuentra. Descargándolo desde GitHub..."
    ["downloading_pindivil_en"]="The pindivil.py file is missing. Downloading it from GitHub..."
    ["launcher_creation_ca"]="Creant el llançador d'aplicació per a Pindivil..."
    ["launcher_creation_es"]="Creando el lanzador de aplicación para Pindivil..."
    ["launcher_creation_en"]="Creating application launcher for Pindivil..."
    ["install_complete_ca"]="Instal·lació completa. Ara pots llançar Pindivil des del menú d'aplicacions."
    ["install_complete_es"]="Instalación completa. Ahora puedes lanzar Pindivil desde el menú de aplicaciones."
    ["install_complete_en"]="Installation complete. You can now launch Pindivil from the applications menu."
)

# Funció per imprimir un missatge en l'idioma seleccionat
function print_message() {
    local key="$1"
    echo -e "\n========================================"
    echo -e "${MESSAGES[${key}_${LANGUAGE}]}"
    echo -e "========================================\n"
}

# Funció per comprovar si una comanda està disponible
function check_command() {
    local cmd=$1
    if ! command -v $cmd &> /dev/null; then
        echo "Error: La comanda $cmd no està disponible. Assegura't que $cmd estigui instal·lat."
        return 1
    fi
    return 0
}

# Preguntar per l'idioma amb números
print_message "select_language"
read -p "Selecciona un idioma (1 - Català, 2 - Español, 3 - English): " LANG_OPTION

case $LANG_OPTION in
    1)
        LANGUAGE="ca"
        ;;
    2)
        LANGUAGE="es"
        ;;
    3)
        LANGUAGE="en"
        ;;
    *)
        LANGUAGE="ca"
        echo "Opció no vàlida. S'utilitzarà català per defecte."
        ;;
esac

# Comprovar dependències
print_message "checking_dependencies"
REQUIRED_PKG=("git" "python3" "lsblk" "xterm")
for pkg in "${REQUIRED_PKG[@]}"; do
    check_command $pkg || exit 1
done
print_message "dependencies_installed"

# Configuració del nom d'usuari
print_message "username_config"
read -p "Introdueix el nom d'usuari (per defecte: pi): " USERNAME
USERNAME=${USERNAME:-pi}

USER_HOME="/home/$USERNAME"

# Creació de les carpetes necessàries a /home/$USERNAME
echo "Creant directoris a $USER_HOME..."
mkdir -p "$USER_HOME/images"
mkdir -p "$USER_HOME/.local/share/applications"
echo "Directoris creats a $USER_HOME/images."

# Configuració del directori d'imatges
print_message "image_dir_config"
read -p "Introdueix el directori on es guardaran les imatges (per defecte: $USER_HOME/images): " IMAGE_DIR
IMAGE_DIR=${IMAGE_DIR:-$USER_HOME/images}

# Configurar PiShrink
print_message "pishrink_setup"
if ! git clone https://github.com/Drewsif/PiShrink.git; then
    echo "Error: No s'ha pogut clonar PiShrink."
    exit 1
fi
chmod +x PiShrink/pishrink.sh
sudo mv PiShrink/pishrink.sh /usr/local/bin/pishrink || { echo "Error: No s'ha pogut moure PiShrink al directori bin."; exit 1; }

# Verificar pindivil.py
print_message "checking_pindivil"
if [ ! -f "/home/$USERNAME/pindivil/pindivil.py" ]; then
    print_message "downloading_pindivil"
    if ! wget -q https://raw.githubusercontent.com/jordilino/Pindivil/main/pindivil.py -O /home/$USERNAME/pindivil/pindivil.py; then
        echo "Error: No s'ha pogut descarregar pindivil.py. Comprova la connexió a internet."
        exit 1
    fi
    print_message "Fitxer pindivil.py descarregat correctament."
else
    echo "El fitxer pindivil.py ja existeix."
fi

# Creació del llançador d'aplicació
print_message "launcher_creation"
cat << EOF > "$USER_HOME/.local/share/applications/pindivil.desktop"
[Desktop Entry]
Name=Pindivil
Comment=Llançador per a Pindivil
Exec=pkexec env DISPLAY=$DISPLAY XAUTHORITY=$XAUTHORITY python3 /home/$USERNAME/pindivil/pindivil.py
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=Utility;
EOF

chmod +x "$USER_HOME/.local/share/applications/pindivil.desktop"

# Finalització
print_message "install_complete"
