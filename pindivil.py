import sys
import os
import threading
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
                             QFileDialog, QMessageBox, QTextEdit, QSizePolicy, QHBoxLayout)

import subprocess

class PindivilApp(QWidget):
    # Definir una señal personalizada per actualitzar la interfície d'usuari
    append_signal = pyqtSignal(str, bool)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pindivil")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.layout = QVBoxLayout()

        # Carregar el logo de l'aplicació
        self.logo_label = QLabel(self)
        pixmap = QPixmap("pindivil.png")
        self.logo_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo_label)

        # Frase de benvinguda en llatí
        self.info_label = QLabel("Gratus es in Pindivil!", self)
        self.info_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.info_label)

        # Botons per a les accions de l'aplicació
        self.check_space_button = QPushButton("Comprovar Espai USB", self)
        self.check_space_button.clicked.connect(self.check_space)
        self.layout.addWidget(self.check_space_button)

        self.select_dir_button = QPushButton("Seleccionar Directori d'Imatges", self)
        self.select_dir_button.clicked.connect(self.select_directory)
        self.layout.addWidget(self.select_dir_button)

        self.create_image_button = QPushButton("Crear imatge des de la SD", self)
        self.create_image_button.clicked.connect(self.create_image)
        self.layout.addWidget(self.create_image_button)

        self.create_image_shrink_button = QPushButton("Crear imatge des de la SD - Després reduir el tamany amb PiShrink", self)
        self.create_image_shrink_button.clicked.connect(self.create_and_shrink_image)
        self.layout.addWidget(self.create_image_shrink_button)

        self.write_image_button = QPushButton("Gravar imatge a la SD", self)
        self.write_image_button.clicked.connect(self.write_image)
        self.layout.addWidget(self.write_image_button)

        self.shrink_image_button = QPushButton("Reduir tamany .img amb PiShrink", self)
        self.shrink_image_button.clicked.connect(self.shrink_image)
        self.layout.addWidget(self.shrink_image_button)

        self.cancel_button = QPushButton("Cancelar", self)
        self.cancel_button.clicked.connect(self.cancel_process)
        self.cancel_button.setDisabled(True)
        self.layout.addWidget(self.cancel_button)

        self.exit_button = QPushButton("Sortir", self)
        self.exit_button.clicked.connect(self.exit_application)
        self.layout.addWidget(self.exit_button)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.layout.addWidget(self.output_text)

        self.output_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setLayout(self.layout)

        self.current_process = None

        # Connectar la senyal personalitzada amb el mètode per actualitzar el QTextEdit
        self.append_signal.connect(self.append_output)

        # Idioma per defecte (Català)
        self.current_language = "ca"

        # Afegir els botons per canviar d'idioma
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

        self.layout.addLayout(self.language_layout)

    def set_language(self, lang_code):
        """Canviar l'idioma i actualitzar els textos."""
        self.current_language = lang_code
        self.update_texts()

    def update_texts(self):
        """Actualitzar els textos segons l'idioma seleccionat."""
        if self.current_language == "ca":
            # Català
            self.check_space_button.setText("Comprovar Espai USB")
            self.select_dir_button.setText("Seleccionar Directori d'Imatges")
            self.create_image_button.setText("Crear imatge des de la SD")
            self.create_image_shrink_button.setText("Crear imatge des de la SD - Després reduir el tamany amb PiShrink")
            self.write_image_button.setText("Gravar imatge a la SD")
            self.shrink_image_button.setText("Reduir tamany .img amb PiShrink")
            self.cancel_button.setText("Cancelar")
            self.exit_button.setText("Sortir")
        elif self.current_language == "es":
            # Castellà
            self.check_space_button.setText("Comprobar Espacio USB")
            self.select_dir_button.setText("Seleccionar Directorio de Imágenes")
            self.create_image_button.setText("Crear imagen desde la SD")
            self.create_image_shrink_button.setText("Crear imagen desde la SD - Luego reducir el tamaño con PiShrink")
            self.write_image_button.setText("Grabar imagen en la SD")
            self.shrink_image_button.setText("Reducir tamaño .img con PiShrink")
            self.cancel_button.setText("Cancelar")
            self.exit_button.setText("Salir")
        elif self.current_language == "en":
            # Anglès
            self.check_space_button.setText("Check USB Space")
            self.select_dir_button.setText("Select Image Directory")
            self.create_image_button.setText("Create Image from SD")
            self.create_image_shrink_button.setText("Create Image from SD - Then Shrink Size with PiShrink")
            self.write_image_button.setText("Write Image to SD")
            self.shrink_image_button.setText("Shrink .img Size with PiShrink")
            self.cancel_button.setText("Cancel")
            self.exit_button.setText("Exit")

        self.info_label.setText("Gratus es in Pindivil!")  # Mantenir el salut en llatí

    def append_output(self, message, overwrite=False):
        if overwrite:
            self.output_text.setText(message)
        else:
            self.output_text.append(message)
        self.output_text.moveCursor(self.output_text.textCursor().End)

    def find_and_prepare_device(self):
        for device in [f"/dev/sd{chr(i)}" for i in range(ord('a'), ord('n') + 1)]:
            if os.path.exists(device):
                self.append_signal.emit(f"Dispositiu trobat: {device}", False)
                mounted = os.popen(f"lsblk -o MOUNTPOINT -nr {device}").read().strip()
                if mounted:
                    self.append_signal.emit(f"Desmuntant {device}...", False)
                    os.system(f"sudo umount {device}*")
                return device
        QMessageBox.critical(self, "Error", "No s'ha detectat cap dispositiu USB connectat.")
        return None

    def check_space(self):
        self.append_signal.emit("Comprovant espai USB...", True)
        device = self.find_and_prepare_device()
        if device:
            fdisk_output = os.popen(f"fdisk -l {device}").read().strip()
            self.append_signal.emit(fdisk_output, False)

    def select_directory(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Selecciona un directori", "/home/pi/images")
        if dir_name:
            self.append_signal.emit(f"Directori seleccionat: {dir_name}", True)

    def show_warning_dialog(self, message):
        """Mostrar un diàleg de confirmació amb missatge."""
        reply = QMessageBox.warning(self, "Advertència", message,
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return reply == QMessageBox.Yes

    def create_image(self):
        device = self.find_and_prepare_device()
        if not device:
            return

        if not self.show_warning_dialog(f"Atenció! La creació de la imatge a {device} destruirà totes les dades del dispositiu. Vols continuar?"):
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar imatge", "/home/pi/images", "Arxius d'Imatge (*.img *.xz)")
        if file_name:
            self.append_signal.emit("Creant la imatge...", True)
            if file_name.endswith('.xz'):
                command = f"sudo dd if={device} bs=4M status=progress | xz > {file_name}"
            else:
                command = f"sudo dd if={device} of={file_name} bs=4M status=progress"
            self.start_process(command, self.handle_finished_create)

    def create_and_shrink_image(self):
        device = self.find_and_prepare_device()
        if not device:
            return

        if not self.show_warning_dialog(f"Atenció! La creació de la imatge a {device} destruirà totes les dades del dispositiu. Vols continuar?"):
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Guardar imatge", "/home/pi/images", "Arxius d'Imatge (*.img *.xz)")
        if file_name:
            self.append_signal.emit("Creant la imatge...", True)
            if file_name.endswith('.xz'):
                base_file = file_name.replace('.xz', '.img')
                command = f"sudo dd if={device} of={base_file} bs=4M status=progress"
                self.start_process(command, lambda: self.shrink_image(base_file, compress_to=file_name))
            else:
                command = f"sudo dd if={device} of={file_name} bs=4M status=progress"
                self.start_process(command, lambda: self.shrink_image(file_name))

    def shrink_image(self, file_name=None, compress_to=None):
        if not file_name:
            file_name, _ = QFileDialog.getOpenFileName(self, "Selecciona la imatge per reduir", "/home/pi/images", "Arxius d'Imatge (*.img *.xz)")
        if file_name:
            if file_name.endswith('.xz'):
                uncompressed_file = file_name.replace('.xz', '.img')
                self.append_signal.emit(f"Descomprimint la imatge {file_name}...", True)
                command = f"xz -d -k {file_name}"
                self.start_process(command, lambda: self.shrink_image(uncompressed_file))
            else:
                self.append_signal.emit(f"Reduïnt la imatge {file_name}...", True)
                command = f"sudo piShrink {file_name}"
                self.start_process(command, lambda: self.compress_image(file_name, compress_to))

    def compress_image(self, file_name, compress_to=None):
        self.append_signal.emit(f"Comprimint la imatge a {compress_to or file_name}.xz...", True)
        command = f"xz {file_name}"
        self.start_process(command)

    def write_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Selecciona una imatge per escriure", "/home/pi/images", "Arxius d'Imatge (*.img *.xz)")
        if file_name:
            device = self.find_and_prepare_device()
            if device:
                self.append_signal.emit(f"Escrivint la imatge {file_name} a {device}...", True)
                if file_name.endswith('.xz'):
                    command = f"xzcat {file_name} | sudo dd of={device} bs=4M status=progress"
                else:
                    command = f"sudo dd if={file_name} of={device} bs=4M status=progress"
                self.start_process(command)

    def start_process(self, command, on_finished=None):
        self.current_process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.append_signal.emit(f"Process started with PID {self.current_process.pid}.", False)
        self.process_thread = threading.Thread(target=self.read_process_output, args=(on_finished,))
        self.process_thread.start()

    def read_process_output(self, on_finished):
        stdout, stderr = self.current_process.communicate()
        if stdout:
            self.append_signal.emit(stdout.decode(), False)
        if stderr:
            self.append_signal.emit(stderr.decode(), False)
        if on_finished:
            on_finished()

    def cancel_process(self):
        if self.current_process:
            self.current_process.terminate()
            self.append_signal.emit(f"Process {self.current_process.pid} terminated.", False)
            self.current_process = None
            self.cancel_button.setDisabled(True)

    def exit_application(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PindivilApp()
    window.show()
    sys.exit(app.exec_())
