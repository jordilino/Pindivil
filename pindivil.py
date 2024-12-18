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
        for device in [f"/dev/sd{chr(i)}" for i in range(ord('a'), ord('n') + 1)]:
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
                command = f"sudo dd if={device} bs=4M status=progress | xz > {file_name}"
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
                command = f"sudo dd if={device} bs=4M status=progress | xz > {file_name}"
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
                command = f"xz -d -k {file_name}"
                self.start_process(command, lambda: self.shrink_image(uncompressed_file))
            else:
                self.append_signal.emit(f"Shrinking {file_name}...", True)
                command = f"sudo piShrink {file_name}"
                self.start_process(command, lambda: self.compress_image(file_name, compress_to))

    def compress_image(self, file_name, compress_to=None):
        self.append_signal.emit(f"Compressing image to {compress_to or file_name}.xz...", True)
        command = f"xz {file_name}"
        self.start_process(command)

    def write_image(self):
        device = self.find_and_prepare_device()
        if not device:
            return
        file_name, _ = QFileDialog.getOpenFileName(self, self.get_text("write_image"), "/home/pi/images", "Image Files (*.img *.xz)")
        if file_name:
            if file_name.endswith('.xz'):
                uncompressed_file = file_name.replace('.xz', '.img')
                self.append_signal.emit(f"Decompressing {file_name}...", True)
                command = f"xz -d -k {file_name}"
                self.start_process(command, lambda: self.write_image(uncompressed_file))
            else:
                self.append_signal.emit(f"Writing {file_name} to {device}...", True)
                command = f"sudo dd if={file_name} of={device} bs=4M status=progress"
                self.start_process(command, self.handle_write_finished)

    def handle_write_finished(self):
        self.append_signal.emit(self.get_text("image_creation_done"), True)
        self.cancel_button.setDisabled(True)

    def cancel_process(self):
        if self.current_process:
            self.append_signal.emit(self.get_text("process_cancelled"), True)
            self.current_process.terminate()
            self.current_process = None

    def start_process(self, command, on_finish=None):
        """Iniciar un proceso en segundo plano."""
        def process_runner():
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            self.append_signal.emit(stdout.decode(), False)
            self.append_signal.emit(stderr.decode(), False)
            if on_finish:
                on_finish()

        thread = threading.Thread(target=process_runner)
        thread.start()

    def exit_application(self):
        self.close()

    def is_pishrink_installed(self):
        """Verificar si piShrink está instalado."""
        return os.system("command -v piShrink") == 0


    translations = {
        "en": {
            "app_title": "Pindivil",
            "check_space": "Check USB Space",
            "select_dir": "Select Image Directory",
            "create_image": "Create Image from SD",
            "create_image_shrink": "Create Image from SD and Shrink with PiShrink",
            "write_image": "Write Image to SD",
            "shrink_image": "Shrink Image with PiShrink",
            "cancel": "Cancel",
            "exit": "Exit",
            "warning": "Warning",
            "warning_msg": "Creating the image on {device} will erase all data. Do you want to continue?",
            "usb_space_check": "Checking USB space...",
            "image_creation": "Creating the image...",
            "image_creation_done": "Image creation finished.",
            "image_shrink": "Shrinking the image...",
            "piShrink_not_installed": "PiShrink is not installed.",
            "process_cancelled": "Process cancelled.",
            "no_device_detected": "No USB device detected.",
            "welcome_msg": "Welcome to Pindivil!",
        },
        "ca": {
            "app_title": "Pindivil",
            "check_space": "Comprovar Espai USB",
            "select_dir": "Seleccionar Directori d'Imatges",
            "create_image": "Crear imatge des de la SD",
            "create_image_shrink": "Crear imatge des de la SD i reduir amb PiShrink",
            "write_image": "Gravar imatge a la SD",
            "shrink_image": "Reduir imatge amb PiShrink",
            "cancel": "Cancel·lar",
            "exit": "Sortir",
            "warning": "Advertència",
            "warning_msg": "La creació de la imatge a {device} destruirà totes les dades. Vols continuar?",
            "usb_space_check": "Comprovant espai USB...",
            "image_creation": "Creant la imatge...",
            "image_creation_done": "Creació de la imatge finalitzada.",
            "image_shrink": "Reduint la imatge...",
            "piShrink_not_installed": "PiShrink no està instal·lat.",
            "process_cancelled": "Procés cancel·lat.",
            "no_device_detected": "No s'ha detectat cap dispositiu USB.",
            "welcome_msg": "Benvingut a Pindivil!",
        },
        "es": {
            "app_title": "Pindivil",
            "check_space": "Comprobar Espacio USB",
            "select_dir": "Seleccionar Directorio de Imágenes",
            "create_image": "Crear imagen desde la SD",
            "create_image_shrink": "Crear imagen desde la SD y Reducir con PiShrink",
            "write_image": "Grabar imagen a la SD",
            "shrink_image": "Reducir tamaño .img con PiShrink",
            "cancel": "Cancelar",
            "exit": "Salir",
            "warning": "Advertencia",
            "warning_msg": "¡Atención! La creación de la imagen en {device} destruirá todos los datos del dispositivo. ¿Desea continuar?",
            "usb_space_check": "Comprobando espacio USB...",
            "image_creation": "Creando la imagen...",
            "image_creation_done": "La creación de la imagen ha terminado.",
            "image_shrink": "Reduciendo la imagen...",
            "piShrink_not_installed": "PiShrink no está instalado.",
            "process_cancelled": "Proceso cancelado.",
            "no_device_detected": "No se detectó ningún dispositivo USB.",
            "welcome_msg": "¡Bienvenido a Pindivil!",
        },
        "la": {
            "app_title": "Pindivil",
            "check_space": "Reprehendo USB Spatium",
            "select_dir": "Eligere Directory Imagines",
            "create_image": "Create Imaginatio ab SD",
            "create_image_shrink": "Create Imaginatio ab SD et contrahere cum PiShrink",
            "write_image": "Scribe Imaginatio in SD",
            "shrink_image": "Contrahere Imaginatio cum PiShrink",
            "cancel": "Annulla",
            "exit": "Exire",
            "warning": "Monitio",
            "warning_msg": "Creando imaginem in {device} omnia data delere. Vis pergere?",
            "usb_space_check": "Reprehendo USB Spatium...",
            "image_creation": "Creando imaginem...",
            "image_creation_done": "Imaginatio creatio finita.",
            "image_shrink": "Contrahens imaginem...",
            "piShrink_not_installed": "PiShrink non est institutus.",
            "process_cancelled": "Processus annullatus.",
            "no_device_detected": "Nullum machinam USB detectum.",
            "welcome_msg": "Salve ad Pindivil!",
        }
    }

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PindivilApp()
    window.show()
    sys.exit(app.exec_())
