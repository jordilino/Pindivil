import sys
import os
import threading
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
                             QFileDialog, QMessageBox, QTextEdit, QSizePolicy)
import subprocess

class PindivilApp(QWidget):
    # Definir una señal personalizada para actualizar la interfaz de usuario
    append_signal = pyqtSignal(str, bool)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pindivil")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.layout = QVBoxLayout()

        self.logo_label = QLabel(self)
        pixmap = QPixmap("pindivil.png")
        self.logo_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo_label)

        self.info_label = QLabel("Exoptatus Pindivil!", self)
        self.info_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.info_label)

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

        # Conectar la señal personalizada con el método para actualizar el QTextEdit
        self.append_signal.connect(self.append_output)

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
                self.append_signal.emit(f"Reduint la mida de la imatge {file_name} amb PiShrink...", True)
                command = f"sudo /usr/local/bin/pishrink {file_name}"
                if compress_to:
                    self.start_process(command, lambda: self.compress_image(file_name, compress_to))
                else:
                    self.start_process(command, self.handle_finished_shrink)

    def compress_image(self, input_file, output_file):
        self.append_signal.emit(f"Comprimin la imatge {input_file} a {output_file}...", True)
        command = f"xz -z -c {input_file} > {output_file}"
        self.start_process(command, self.handle_finished_shrink)

    def write_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Selecciona la imatge per gravar", "/home/pi/images", "Arxius d'Imatge (*.img *.xz)")
        if file_name:
            device = self.find_and_prepare_device()
            if not device:
                return
            self.append_signal.emit(f"Gravant la imatge {file_name} a {device}...", True)
            if file_name.endswith('.xz'):
                command = f"xz -d -c {file_name} | sudo dd of={device} bs=4M status=progress"
            else:
                command = f"sudo dd if={file_name} of={device} bs=4M status=progress"
            self.start_process(command, self.handle_finished_write)

    def start_process(self, command, callback):
        self.disable_buttons()
        self.current_process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        def monitor_output():
            try:
                while True:
                    output = self.current_process.stdout.readline()
                    if output:
                        self.append_signal.emit(output.strip(), False)
                    elif self.current_process.poll() is not None:
                        break

                error_output = self.current_process.stderr.read()
                if error_output:
                    self.append_signal.emit(error_output.strip(), False)

            except Exception as e:
                self.append_signal.emit(f"Error: {str(e)}", False)
            finally:
                self.current_process = None
                callback()

        threading.Thread(target=monitor_output, daemon=True).start()

    def cancel_process(self):
        if self.current_process:
            self.current_process.terminate()
            self.current_process = None
            self.append_signal.emit("Procés cancel·lat.", True)
            self.enable_buttons()

    def handle_finished_create(self):
        self.append_signal.emit("Creació de la imatge finalitzada.", False)
        self.enable_buttons()

    def handle_finished_shrink(self):
        self.append_signal.emit("Reducció de la mida de la imatge finalitzada.", False)
        self.enable_buttons()

    def handle_finished_write(self):
        self.append_signal.emit("Gravació de la imatge finalitzada.", False)
        self.enable_buttons()

    def exit_application(self):
        self.close()

    def disable_buttons(self):
        for button in self.findChildren(QPushButton):
            button.setDisabled(True)
        self.cancel_button.setDisabled(False)

    def enable_buttons(self):
        for button in self.findChildren(QPushButton):
            button.setEnabled(True)
        self.cancel_button.setDisabled(True)

app = QApplication(sys.argv)
window = PindivilApp()
window.show()
sys.exit(app.exec_())
