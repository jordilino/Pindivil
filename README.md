# Pindivil
![Gratus es in Pindivil!](https://github.com/jordilino/Pindivil/blob/main/pindivil_large_icon.png)

## Català

**Pindivil** és una eina gràfica per a la creació, manipulació i gravació d'imatges de targetes SD i dispositius USB. Aquest projecte utilitza **PiShrink** per reduir la mida de les imatges creades, i permet la creació d'imatges, la compressió i la gravació en dispositius USB o targetes SD de manera senzilla.

### Característiques

- Comprovació d'espai disponible en dispositius USB.
- Creació d'imatges de dispositius SD.
- Reducció de la mida de les imatges amb **PiShrink**.
- Gravació d'imatges en dispositius SD o USB.
- Eina gràfica desenvolupada amb **PyQt5**.

### Requisits

Abans d'instal·lar i utilitzar **Pindivil**, has d'assegurar-te que tens les següents dependències instal·lades: 

- **PiShrink**
- **git**
- **gzip**
- **lsblk**
- **parted**
- **pkexec**
- **pigz**
- **python3**
- **python3-venv**
- **udev**
- **wget**
- **xz-utils**
- **e2fsprogs**
- **xterm**
   ```bash
   sudo apt-get install PiShrink git gzip lsblk parted pkexec pigz python3 python3-venv udev wget xz-utils e2fsprogs xterm
   ```


### Instal·lació

1. **Clona el repositori**:
   ```bash
   sudo git clone https://github.com/jordilino/pindivil.git
   cd pindivil
   ```

2. **Instal·la les dependències**:
   ```bash
   sudo apt update
   sudo apt install git python3 pkexec lsblk xterm python3-venv
   ```

3. **Instal·la PiShrink**:
   ```bash
   wget https://raw.githubusercontent.com/Drewsif/PiShrink/master/pishrink.sh
   chmod +x pishrink.sh
   sudo mv pishrink.sh /usr/local/bin/piShrink
   ```
   
5. **Executa l'instal·lador**:
   ```bash
   sudo bash installer.sh
   ```

6. **Llança Pindivil**: Un cop finalitzada la instal·lació, pots llançar Pindivil des del menú d'aplicacions del teu sistema.

### Ús

- **Comprovar espai USB**: Comprova l'espai disponible en un dispositiu USB.
- **Seleccionar directori d'imatges**: Escull el directori on es guardaran les imatges.
- **Crear imatge**: Crea una imatge des de la targeta SD o USB seleccionada.
- **Crear i reduir imatge**: Crea una imatge i després redueix-ne la mida amb PiShrink.
- **Gravar imatge a la SD**: Grava una imatge prèviament creada a un dispositiu SD o USB.
- **Reduir tamany de la imatge**: Redueix la mida d'una imatge amb PiShrink.

### Contribuir

Si vols contribuir a **Pindivil**, pots fer-ho mitjançant *pull requests* al repositori.

---

## Español

**Pindivil** es una herramienta gráfica para la creación, manipulación y grabación de imágenes de tarjetas SD y dispositivos USB. Este proyecto utiliza **PiShrink** para reducir el tamaño de las imágenes creadas, y permite la creación de imágenes, la compresión y la grabación en dispositivos USB o tarjetas SD de forma sencilla.

### Características

- Comprobación del espacio disponible en dispositivos USB.
- Creación de imágenes desde dispositivos SD.
- Reducción del tamaño de las imágenes con **PiShrink**.
- Grabación de imágenes en dispositivos SD o USB.
- Herramienta gráfica desarrollada con **PyQt5**.

### Requisitos

Antes de instalar y usar **Pindivil**, debes asegurarte de que tienes las siguientes dependencias instaladas:

- **PiShrink**
- **git**
- **gzip**
- **lsblk**
- **parted**
- **pkexec**
- **pigz**
- **python3**
- **python3-venv**
- **udev**
- **wget**
- **xz-utils**
- **e2fsprogs**
- **xterm**
   ```bash
   sudo apt-get install PiShrink git gzip lsblk parted pkexec pigz python3 python3-venv udev wget xz-utils e2fsprogs xterm
   ```
  

### Instalación

1. **Clonar el repositorio**:
   ```bash
   sudo git clone https://github.com/jordilino/pindivil.git
   cd pindivil
   ```

2. **Instalar las dependencias**:
   ```bash
   sudo apt update
   sudo apt install git python3 pkexec lsblk xterm python3-venv
   ```
   
3. **Instalar PiShrink**: 
   ```bash
   wget https://raw.githubusercontent.com/Drewsif/PiShrink/master/pishrink.sh
   chmod +x pishrink.sh
   sudo mv pishrink.sh /usr/local/bin/piShrink
   ```

4. **Ejecutar el instalador**:
   ```bash
   sudo bash installer.sh
   ```

5. **Lanzar Pindivil**: Una vez finalizada la instalación, puedes lanzar **Pindivil** desde el menú de aplicaciones de tu sistema.

### Uso

- **Comprobar espacio USB**: Comprueba el espacio disponible en un dispositivo USB.
- **Seleccionar directorio de imágenes**: Elige el directorio donde se guardarán las imágenes.
- **Crear imagen**: Crea una imagen desde la tarjeta SD o USB seleccionada.
- **Crear y reducir imagen**: Crea una imagen y luego reduce su tamaño con **PiShrink**.
- **Grabar imagen en la SD**: Graba una imagen previamente creada en un dispositivo SD o USB.
- **Reducir tamaño de la imagen**: Reduce el tamaño de una imagen con **PiShrink**.

### Contribuir

Si quieres contribuir a **Pindivil**, puedes hacerlo mediante *pull requests* en el repositorio.

---

## English

**Pindivil** is a graphical tool for creating, manipulating, and writing images of SD cards and USB devices. This project uses **PiShrink** to shrink the size of created images and allows for creating images, compression, and writing to USB devices or SD cards easily.

### Features

- Check available space on USB devices.
- Create images from SD devices.
- Shrink image size using **PiShrink**.
- Write images to SD or USB devices.
- Graphical tool developed with **PyQt5**.

### Requirements

Before installing and using **Pindivil**, make sure you have the following dependencies installed:

- **PiShrink**
- **git**
- **gzip**
- **lsblk**
- **parted**
- **pkexec**
- **pigz**
- **python3**
- **python3-venv**
- **udev**
- **wget**
- **xz-utils**
- **e2fsprogs**
- **xterm**
  ```bash
   sudo apt-get install PiShrink git gzip lsblk parted pkexec pigz python3 python3-venv udev wget xz-utils e2fsprogs xterm
  ```

### Installation

1. **Clone the repository**:
   ```bash
   sudo git clone https://github.com/jordilino/pindivil.git
   cd pindivil
   ```

2. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install git python3 pkexec lsblk xterm python3-venv
   ```

3. **Install PiShrink**: 
   ```bash
   wget https://raw.githubusercontent.com/Drewsif/PiShrink/master/pishrink.sh
   chmod +x pishrink.sh
   sudo mv pishrink.sh /usr/local/bin/piShrink
   ```

4. **Run the installer**:
   ```bash
   sudo bash installer.sh
   ```

5. **Launch Pindivil**: After installation, you can launch **Pindivil** from your system’s applications menu.

### Usage

- **Check USB space**: Check available space on a USB device.
- **Select image directory**: Choose the directory where images will be saved.
- **Create image**: Create an image from the selected SD or USB device.
- **Create and shrink image**: Create an image and then shrink it using **PiShrink**.
- **Write image to SD**: Write a previously created image to an SD or USB device.
- **Shrink image size**: Shrink the size of an image using **PiShrink**.

### Contribute

If you want to contribute to **Pindivil**, you can do so through *pull requests* in the repository.
