import sys
import os
import threading
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
                             QFileDialog, QMessageBox, QTextEdit, QSizePolicy, QHBoxLayout)

import subprocess

class PindivilApp(QWidget):
    append_signal = pyqtSignal(str, bool)

    def __init__(self):
        super().__init__()

        # Inicializar el idioma predeterminado
        self.current_language = "en"  # Idioma predeterminado (Inglés)

        self.setWindowTitle(self.get_text("app_title"))  # Título cambiado dinámicamente según el idioma
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.layout = QVBoxLayout()

        # Cargar logo de la aplicación
        self.logo_label = QLabel(self)
        pixmap = QPixmap("/usr/local/bin/pindivil.png")
        self.logo_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo_label)

        # Frase de bienvenida en el idioma actual
        self.info_label = QLabel(self.get_text("welcome_msg"), self)
        self.info_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.info_label)

        # Botones
        self.check_space_button = QPushButton(self.get_text("check_space"), self)
        self.check_space_button.clicked.connect(self.check_space)
        self.layout.addWidget(self.check_space_button)

        self.select_dir_button = QPushButton(self.get_text("select_dir"), self)
        self.select_dir_button.clicked.connect(self.select_directory)
        self.layout.addWidget(self.select_dir_button)

        self.create_image_button = QPushButton(self.get_text("create_image"), self)
        self.create_image_button.clicked.connect(self.create_image)
        self.layout.addWidget(self.create_image_button)

        self.create_image_shrink_button = QPushButton(self.get_text("create_image_shrink"), self)
        self.create_image_shrink_button.clicked.connect(self.create_and_shrink_image)
        self.layout.addWidget(self.create_image_shrink_button)

        self.write_image_button = QPushButton(self.get_text("write_image"), self)
        self.write_image_button.clicked.connect(self.write_image)
        self.layout.addWidget(self.write_image_button)

        self.shrink_image_button = QPushButton(self.get_text("shrink_image"), self)
        self.shrink_image_button.clicked.connect(self.shrink_image)
        self.layout.addWidget(self.shrink_image_button)

        self.cancel_button = QPushButton(self.get_text("cancel"), self)
        self.cancel_button.clicked.connect(self.cancel_process)
        self.cancel_button.setDisabled(True)
        self.layout.addWidget(self.cancel_button)

        self.exit_button = QPushButton(self.get_text("exit"), self)
        self.exit_button.clicked.connect(self.exit_application)
        self.layout.addWidget(self.exit_button)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

        self.output_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setLayout(self.layout)

        self.output_text.setText("")
        self.current_process = None
        self.append_signal.connect(self.append_output)

        # Layout para cambiar de idioma
        self.language_layout = QHBoxLayout()

        self.catalan_button = QPushButton("Català", self)
        self.catalan_button.clicked.connect(lambda: self.set_language("ca"))
        self.language_layout.addWidget(self.catalan_button)

        self.spanish_button = QPushButton("Español", self)
        self.spanish_button.clicked.connect(lambda: self.set_language("es"))
        self.language_layout.addWidget(self.spanish_button)

        self.english_button = QPushButton("English", self)
        self.english_button.clicked.connect(lambda: self.set_language("en"))
        self.language_layout.addWidget(self.english_button)

        self.latin_button = QPushButton("Latine", self)
        self.latin_button.clicked.connect(lambda: self.set_language("la"))
        self.language_layout.addWidget(self.latin_button)

        self.layout.addLayout(self.language_layout)

    def get_text(self, key):
        """Obtiene el texto correspondiente al idioma actual."""
        if not hasattr(self, 'current_language'):
            self.current_language = "en"
        return self.translations.get(self.current_language, self.translations["en"]).get(key, key)

    def append_output(self, message, overwrite=False):
        if overwrite:
            self.output_text.setText(message)
        else:
            self.output_text.append(message)
        self.output_text.moveCursor(self.output_text.textCursor().End)

    def set_language(self, lang_code):
        """Función para cambiar el idioma."""
        self.current_language = lang_code
        self.setWindowTitle(self.get_text("app_title"))
        self.info_label.setText(self.get_text("welcome_msg"))
        self.check_space_button.setText(self.get_text("check_space"))
        self.select_dir_button.setText(self.get_text("select_dir"))
        self.create_image_button.setText(self.get_text("create_image"))
        self.create_image_shrink_button.setText(self.get_text("create_image_shrink"))
        self.write_image_button.setText(self.get_text("write_image"))
        self.shrink_image_button.setText(self.get_text("shrink_image"))
        self.cancel_button.setText(self.get_text("cancel"))
        self.exit_button.setText(self.get_text("exit"))

    def find_and_prepare_device(self):
        """Busca el primer dispositivo USB disponible de forma más general."""
        devices = [f"/dev/{d}" for d in os.listdir('/dev') if d.startswith('sd')]
        for device in devices:
            if os.path.exists(device):
                self.append_signal.emit(f"Device found: {device}", False)
                mounted = os.popen(f"lsblk -o MOUNTPOINT -nr {device}").read().strip()
                if mounted:
                    self.append_signal.emit(f"Unmounting {device}...", False)
                    os.system(f"sudo umount {device}*")
                return device
        QMessageBox.critical(self, self.get_text("warning"), self.get_text("no_device_detected"))
        return None

    def check_space(self):
        self.append_signal.emit(self.get_text("usb_space_check"), True)
        device = self.find_and_prepare_device()
        if device:
            fdisk_output = os.popen(f"fdisk -l {device}").read().strip()
            self.append_signal.emit(fdisk_output, False)

    def select_directory(self):
        dir_name = QFileDialog.getExistingDirectory(self, self.get_text("select_dir"), "/home/pi/images")
        if dir_name:
            self.append_signal.emit(f"Selected directory: {dir_name}", True)

    def show_warning_dialog(self, message):
        """Mostrar un diàleg de confirmació amb missatge."""
        reply = QMessageBox.warning(self, self.get_text("warning"), message,
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return reply == QMessageBox.Yes

    def create_image(self):
        device = self.find_and_prepare_device()
        if not device:
            return

        if not self.show_warning_dialog(self.get_text("warning_msg").format(device=device)):
            return

        file_name, _ = QFileDialog.getSaveFileName(self, self.get_text("create_image"), "/home/pi/images", "Image Files (*.img *.xz)")
        if file_name:
            self.append_signal.emit(self.get_text("image_creation"), True)
            if file_name.endswith('.xz'):
                command = f"sudo dd if={device} bs=4M status=progress | xz -T0 > {file_name}"
            else:
                command = f"sudo dd if={device} of={file_name} bs=4M status=progress"
            self.start_process(command, self.handle_finished_create)

    def create_and_shrink_image(self):
        """Crea una imatge i la redueix després amb PiShrink."""
        device = self.find_and_prepare_device()
        if not device:
            return

        if not self.show_warning_dialog(self.get_text("warning_msg").format(device=device)):
            return

        file_name, _ = QFileDialog.getSaveFileName(self, self.get_text("create_image_shrink"), "/home/pi/images", "Image Files (*.img *.xz)")
        if file_name:
            self.append_signal.emit(self.get_text("image_creation"), True)
            if file_name.endswith('.xz'):
                command = f"sudo dd if={device} bs=4M status=progress | xz -T0 > {file_name}"
            else:
                command = f"sudo dd if={device} of={file_name} bs=4M status=progress"
            self.start_process(command, lambda: self.shrink_image(file_name))

    def handle_finished_create(self):
        self.append_signal.emit(self.get_text("image_creation_done"), True)
        self.cancel_button.setDisabled(True)

    def shrink_image(self, file_name=None, compress_to=None):
        if not self.is_pishrink_installed():
            QMessageBox.critical(self, self.get_text("warning"), self.get_text("piShrink_not_installed"))
            return
        if not file_name:
            file_name, _ = QFileDialog.getOpenFileName(self, self.get_text("shrink_image"), "/home/pi/images", "Image Files (*.img *.xz)")
        if file_name:
            if file_name.endswith('.xz'):
                uncompressed_file = file_name.replace('.xz', '.img')
                self.append_signal.emit(f"Decompressing {file_name}...", True)
                command = f"xz -T0 -d -k {file_name}"
                self.start_process(command, lambda: self.shrink_image(uncompressed_file))
            else:
                self.append_signal.emit(f"Shrinking {file_name}...", True)
                command = f"sudo piShrink {file_name}"
                self.start_process(command, lambda: self.compress_image(file_name, compress_to))

    def compress_image(self, file_name, compress_to=None):
        self.append_signal.emit(f"Compressing image to {compress_to or file_name}.xz...", True)
        command = f"xz -T0 {file_name}"
        self.start_process(command)

    def write_image(self):
        device = self.find_and_prepare_device()
        if not device:
            return
        file_name, _ = QFileDialog.getOpenFileName(self, self.get_text("write_image"), "/home/pi/images", "Image Files (*.img *.xz)")
        if file_name:
            self.append_signal.emit(f"Writing image {file_name} to {device}...", True)
            if file_name.endswith('.xz'):
                command = f"xz -T0 -d -k {file_name} | sudo dd of={device} bs=4M status=progress"
            else:
                command = f"sudo dd if={file_name} of={device} bs=4M status=progress"
            self.start_process(command)

    def cancel_process(self):
        """Cancela el procés en execució actual."""
        if self.current_process:
            self.current_process.terminate()
            self.append_signal.emit(self.get_text("process_cancelled"), True)

    def start_process(self, command, on_finish_callback=None):
        """Inicia el procés de manera asíncrona."""
        def run_command():
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.current_process = process
            output, error = process.communicate()
            if output:
                self.append_signal.emit(output.decode(), False)
            if error:
                self.append_signal.emit(error.decode(), False)
            if on_finish_callback:
                on_finish_callback()

        process_thread = threading.Thread(target=run_command)
        process_thread.start()

    def is_pishrink_installed(self):
        """Verifica si PiShrink está instalado en el sistema."""
        return os.system("which pishrink > /dev/null 2>&1") == 0

    def exit_application(self):
        QApplication.quit()

# Traducciones de la aplicación para múltiples idiomas
translations = {
    "en": {
        "app_title": "Pindivil - SD Image Manager",
        "welcome_msg": "Welcome to Pindivil!",
        "check_space": "Check USB Space",
        "select_dir": "Select Directory",
        "create_image": "Create Image",
        "create_image_shrink": "Create and Shrink Image",
        "write_image": "Write Image to Device",
        "shrink_image": "Shrink Image",
        "cancel": "Cancel Process",
        "exit": "Exit Application",
        "no_device_detected": "No device detected. Please connect a USB drive.",
        "usb_space_check": "Checking USB space...",
        "image_creation": "Creating image... Please wait.",
        "image_creation_done": "Image creation finished successfully.",
        "process_cancelled": "Process has been cancelled.",
        "warning": "Warning",
        "warning_msg": "Are you sure you want to overwrite the device {}?",
        "piShrink_not_installed": "PiShrink is not installed. Please install it first.",
    },
    "es": {
        "app_title": "Pindivil - Gestor de Imágenes SD",
        "welcome_msg": "¡Bienvenido a Pindivil!",
        "check_space": "Comprobar espacio USB",
        "select_dir": "Seleccionar directorio",
        "create_image": "Crear imagen",
        "create_image_shrink": "Crear y reducir imagen",
        "write_image": "Escribir imagen en dispositivo",
        "shrink_image": "Reducir imagen",
        "cancel": "Cancelar proceso",
        "exit": "Salir de la aplicación",
        "no_device_detected": "No se detectó ningún dispositivo. Conecte una unidad USB.",
        "usb_space_check": "Comprobando espacio USB...",
        "image_creation": "Creando imagen... Por favor espere.",
        "image_creation_done": "Creación de imagen finalizada correctamente.",
        "process_cancelled": "El proceso ha sido cancelado.",
        "warning": "Advertencia",
        "warning_msg": "¿Está seguro de que desea sobrescribir el dispositivo {}?",
        "piShrink_not_installed": "PiShrink no está instalado. Instálelo primero.",
    },
    "ca": {
        "app_title": "Pindivil - Gestor d'Imatges SD",
        "welcome_msg": "Benvingut a Pindivil!",
        "check_space": "Comprovar espai USB",
        "select_dir": "Seleccionar directori",
        "create_image": "Crear imatge",
        "create_image_shrink": "Crear i reduir imatge",
        "write_image": "Escriure imatge al dispositiu",
        "shrink_image": "Reduir imatge",
        "cancel": "Cancel·lar procés",
        "exit": "Sortir de l'aplicació",
        "no_device_detected": "No s'ha detectat cap dispositiu. Connecteu una unitat USB.",
        "usb_space_check": "Comprovant espai USB...",
        "image_creation": "Creant imatge... Si us plau, espereu.",
        "image_creation_done": "Creació d'imatge finalitzada correctament.",
        "process_cancelled": "El procés ha estat cancel·lat.",
        "warning": "Advertència",
        "warning_msg": "Esteu segur que voleu sobrescriure el dispositiu {}?",
        "piShrink_not_installed": "PiShrink no està instal·lat. Instal·leu-lo primer.",
    },
    "la": {
        "app_title": "Pindivil - SD Imaginum Manager",
        "welcome_msg": "Salve in Pindivil!",
        "check_space": "USB Spatium Reprehendo",
        "select_dir": "Selectio Directorii",
        "create_image": "Imaginum Creare",
        "create_image_shrink": "Imaginum Creare et Contractum",
        "write_image": "Imaginum Ad Apparatum Scribere",
        "shrink_image": "Imaginum Contractum",
        "cancel": "Processum Annulla",
        "exit": "Exire Applicationem",
        "no_device_detected": "Nullum apparatum detectum. Please connect USB.",
        "usb_space_check": "USB spatium reprehendens...",
        "image_creation": "Imaginum creans... Quaeso, exspecta.",
        "image_creation_done": "Imaginum creatum confestim!",
        "process_cancelled": "Processus annullatus.",
        "warning": "Monitum",
        "warning_msg": "Esne certo oblitterare apparatum {}?",
        "piShrink_not_installed": "PiShrink non est inscriptum. Primum id instituere.",
    }
}

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = PindivilApp()
    window.translations = translations
    window.show()

    sys.exit(app.exec_())
