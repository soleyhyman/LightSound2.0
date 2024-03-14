# Plotting and Logging
Python data logger, plotter, and Arduino code for LightSound 2.0 devices

### About LightSound
LightSound is an Arduino-based device that converts light intensity to sound via a light sensor and MIDI board so that blind and visually impaired (BVI) individuals may experience astronomical events like solar eclipses. The original version (LightSound 1.0) was designed and used during the total solar eclipse on August 21, 2017. In preparation for the upcoming North and South American total solar eclipses (2019, 2020, and 2024), LightSound has been redesigned with higher sensitivities and an improved sound library.

The LightSound 2.0 devices can run on a 9-volt or Li-ion battery (portable mode) or off of computer power (logging mode). When in portable mode, the switch will turn the device on and off. In order to record data, LightSound must be connected to a computer. In this case, the device runs off of the computer power and will remain on as long as it is plugged in.

To hear the sounds produced by LightSound 2.0, the device must be connected to speakers or headphones via the audio jack.

More information and building instructions for LightSound 2.0 can be found at: [https://astrolab.fas.harvard.edu/LightSound.html](https://astrolab.fas.harvard.edu/LightSound.html)

**Please note: The LightSound device code and instructions provided (both in this repository and on the website) are open source, but they may *not* be used to build LightSounds for profit.**

### Instructions for logging data
Runs on Python 2.7 or 3.x

Package requirements: `numpy`, `matplotlib`, and [`pySerial`](https://pyserial.readthedocs.io/en/latest/pyserial.html#installation)
1. Ensure that the serial logger program (LightSound2_data_logger.py) is located in the folder where you will save your data
2. Connect the LightSound 2.0 to the computer with a micro-USB B cord (must be able to transfer data)
3. Determine the appropriate serial port of the LightSound 2.0
    - Windows: type `mode` into command line, port should have the form `COM*`
    - Mac: type `ls /dev/tty.*` into terminal, port should have the form `/dev/tty.usbmodem*` or `/dev/tty.usbserial*` 
    - Linux: type `ls/dev/tty*` into terminal, port should have the form `/dev/ttyUSB*` or `/dev/ttyACM*`
4. In the terminal (Mac/Linux) or command line (Windows), navigate to data folder and type: `python LightSound2_data_logger.py port 9600 timezone file_prefix`
    - `port` is the full port name determined in Step 3 (i.e. including `/dev/tty*` for Mac or Linux)
    - `9600` is the baud rate for reading the LightSound 2.0 data
    - `timezone` is the timezone of observations (e.g. CST, EST, ART, CLT, etc.)
    - `file_prefix` is the prefix of the name of the data files (the script saves the data with the correct extension)
5. A plotting window will pop up once you start the code and will start live-plotting the data that the LightSound is recording. The brightness values that are being recorded by the LightSound will be visible in the terminal. 

6. To stop data logging:
   - If you are a **Windows/PC user**, click back into your terminal and press `Ctrl + C` in terminal/command line. Sometimes you need to do this multiple times for it properly stop. If you do accidentally exit this window via the exit button, don't panic! Just click back into the terminal and press `Ctrl + C` repeatedly until it exits the code. The .csv file will not be produced, but the raw data will still be saved, which you can later turn into a csv file.
   - If you are a **Mac user**, as of 10/12/2023, there is a bug in the code for exiting the script. Until a long-term solution is found, first exit the ploting window by clicking the red X. This will throw an error in the command that you can ignore. Click into the terminal window with the serial data and end the script via `Ctrl + C`. This will save the data in both `_raw.log` and `_data.csv` file formats, but the plot will not save. To plot from the data, use the instructions provided below for the plotter script.



### Instructions for plotting data
Runs on Python 2.7 or 3.x

Package requirements: `datetime`, `matplotlib`, `numpy`, `sys`
1. Ensure that the serial logger program (LightSound2_data_plotter.py) is located in the folder where you will save your data
2. In the terminal (Mac/Linux) or command line (Windows), navigate to data folder and type: `python LightSound2_data_plotter.py filename plot_lines savename.png`
    - `filename` is the full name of the data file (should end with \_raw.log or \_data.csv)
    - `plot_lines` determines whether the plot will include whether the gain and integration times
        - To plot the lux (intensity) values only, replace `plot_lines` with `0`
        - To plot the lux, gain, and integration times, replace `plot_lines` with `1`
    - `savename` is the prefix of the image name the plot will save to; use none if you do not want to save the image (extension typically is .png)

-----

# LightSound2.0
Python data logger, plotter y código para Arduino de dispositivos LightSound 2.0

### Acerca de LightSound

LightSound es un dispositivo basado en Arduino que convierte la intensidad de la luz en sonido a través de un sensor de luz y una placa MIDI para que las personas ciegas y con discapacidades visuales (BVI) puedan experimentar eventos astronómicos como los eclipses solares. La versión original (LightSound 1.0) se diseñó y usó durante el eclipse total de Sol el 21 de agosto de 2017, en los Estados Unidos. En preparación para los próximos eclipses solares totales en Norteamérica y Sudamérica (2019, 2020 y 2024), LightSound se ha rediseñado con mayor sensibilidad y una biblioteca de sonido mejorada. 

El LightSound trabaja con una batería de 9 voltios o batería de Li-Ion si se lo usa en su modo portátil. El interruptor del dispositivo lo apaga unicamente si se usa esa batería. 

Para escuchar la transformación de luz en sonido, es necesario que el LightSound esté conectado a un dispositivo externo: auriculares o parlantes.

 Para registro y analisis de datos, el LightSound debe estar conectado a la PC, en este caso no necesita batería y el interruptor no tiene acción sobre el dispositivo, por eso, conectado a la PC el dispositivo estará trabajando permanentemente.

Se puede encontrar más información e instrucciones de construcción para LightSound 2.0 en: [https://astrolab.fas.harvard.edu/LightSound.html](https://astrolab.fas.harvard.edu/LightSound.html)


### Instrucciones para el registro de datos
El script corre en Python 2.7 o 3.x

Paquetes python requeridos: `datetime`, `sys` y [`pySerial`](https://pyserial.readthedocs.io/en/latest/pyserial.html#installation)

1. Asegúrese de que el programa registrador serie (LightSound2_data_logger.py) esté ubicado en la carpeta donde guardará sus datos.
2. Conecte el LightSound 2.0 a la computadora con un cable micro-USB B (debe poder transferir datos).
3. Determine el puerto serie utilizado por el LightSound 2.0. Según su sistema operativo:
    - En Windows: escriba `mode` en la línea de commandos del símbolo de sistema, el puerto debe tener el formato `COM*`
    - En Mac: escriba `ls /dev/tty.*` en la terminal, el puerto debe tener el formato `/dev/tty.usbmodem*` o `/dev/tty.usbserial*`
    - En Linux: escriba `ls /dev/tty*` en la terminal, el puerto debe tener el formato `/dev/ttyUSB*` o `/dev/ttyACM*` (considerando * como 0, 1, o 2)
4. En la terminal (Mac/Linux) o en la línea de comandos (Windows), navegue hasta la carpeta de datos y escriba: `python LightSound2_data_logger.py port 9600 timezone file_prefix`
    - `port` es el nombre del puerto determinado en el Paso 3, debe escribir completo `/dev/ttyACM*`
    - `9600` es la velocidad en baudios para leer los datos de LightSound 2.0
    - `timezone` (ona horaria) es la zona horaria de las observaciones (por ejemplo, CST, EST, ART, CLT, etc.). ART significa Hora en Argentina. CLT, hora en Chile.
    - `file_prefix` es el prefijo para el nombre de los archivos de datos, considerar que el script coloca automaticamente la extensión
5. Se verán en la terminal los valores que está registrando el LightSound
6. Para detener e registro de datos, presionar Ctrl + C en la terminal/linea de comandos. El script salvará automáticamente los datos crudos (\*\_raw.log) como un archivo .csv (\*\_data.csv) para su uso posterior.

### Instrucciones para graficar los datos
Corre en Python 2.7 o 3.x

Paquetes Python requeridos: `datetime`, `matplotlib`, `numpy`, `sys`

1. Asegúrese de que el programa de registro en serie (LightSound2_data_plotter.py) esté ubicado en la carpeta donde guardará sus datos.
2. En la terminal (Mac/Linux) o en la línea de comandos (Windows), navegue hasta la carpeta de datos y escriba: `python LightSound2_data_plotter.py filename plot_lines savename.png`
    - `filename` es el nombre completo del archivo de datos (debe terminar con \_raw.log o \_data.csv) 
    - `filename` (nombre-archivo) es el prefijo del nombre del archivo de registro para los datos (la extensión debe ser la misma que la utilizada para el registro de datos)
    - `plot_lines` determina si la gráfica incluirá  ganancia o tiempo de integración
        - Para  graficar solo los valores de lux (intensidad), reemplace `plot_lines` con `0`
        - Para  graficar los tiempos de lux, ganancia e integración, reemplace `plot_lines` con `1`
    - `savename` es el prefijo del nombre del archivo en que se guardará el gráfico; no use ninguno si no desea guardar la imagen (la extensión es típicamente .png)
