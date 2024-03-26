# LightSound2.0
Code and executables for logging and plotting LightSound data, as well as Arduino code, 3D-printable case designs, and instructions for building LightSound devices. See [Overview of Repository](#overview-of-repository) for information on the structure of this GitHub repository.

### About LightSound
LightSound is an Arduino-based device that converts light intensity to sound via a light sensor and MIDI board so that blind and visually impaired (BVI) individuals may experience astronomical events like solar eclipses. The original prototype was designed and used during the total solar eclipse on August 21, 2017. In preparation for the upcoming North and South American total and annular solar eclipses (2019, 2020, 2023, and 2024), LightSound has been redesigned with higher sensitivities and an improved sound library.

The LightSound 2.0 devices can run on a 9-volt or Li-ion battery (portable mode) or off of computer power (logging mode). When in portable mode, the switch will turn the device on and off. In order to record data, LightSound must be connected to a computer. In this case, the device runs off of the computer power and will remain on as long as it is plugged in.

To hear the sounds produced by LightSound 2.0, the device must be connected to speakers or headphones via the audio jack.

More information and building instructions for LightSound 2.0 can be found at: [https://astrolab.fas.harvard.edu/LightSound.html](https://astrolab.fas.harvard.edu/LightSound.html)

**Please note: The LightSound device code and instructions provided (both in this repository and on the website) are open source, but they may *not* be used to build LightSounds for profit.**

### Overview of Repository
- [LightSound-Computer-Interface](https://github.com/soleyhyman/LightSound2.0/tree/main/LightSound-Computer-Interface): Contains files for standalone executable computer interface program for both Windows and Mac OSX machines, as well as the Python code for any operating system (currently English-only). 
- [pcb-LightSound-Feather328p](https://github.com/soleyhyman/LightSound2.0/tree/main/pcb-LightSound-Feather328p): Contains files and instructions for building the PCB LightSound version with Feather 328p microcontroller board (currently English-only)
- [pcb-LightSound-Feather32u4](https://github.com/soleyhyman/LightSound2.0/tree/main/pcb-LightSound-Feather32u4): Contains files and instructions for building the PCB LightSound version with Feather 328p microcontroller board (currently English-only)
- [wired-LightSound-Flora](https://github.com/soleyhyman/LightSound2.0/tree/main/wired-LightSound-Flora): Contains files and instructions for building the wired LightSound

Previous versions of the plotting and logging code (Python-only) are deprecated and no longer supported but are archived [here](https://github.com/soleyhyman/LightSound2.0/tree/main/LightSound-Computer-Interface/deprecated_code).

-----

# LightSound2.0
Python data logger, plotter y código para Arduino de dispositivos LightSound 2.0

### Acerca de LightSound

LightSound es un dispositivo basado en Arduino que convierte la intensidad de la luz en sonido a través de un sensor de luz y una placa MIDI para que las personas ciegas y con discapacidades visuales (BVI) puedan experimentar eventos astronómicos como los eclipses solares. La versión original (LightSound 1.0) se diseñó y usó durante el eclipse total de Sol el 21 de agosto de 2017, en los Estados Unidos. En preparación para los próximos eclipses solares totales en Norteamérica y Sudamérica (2019, 2020 y 2024), LightSound se ha rediseñado con mayor sensibilidad y una biblioteca de sonido mejorada.

El LightSound trabaja con una batería de 9 voltios o batería de Li-Ion si se lo usa en su modo portátil. El interruptor del dispositivo lo apaga unicamente si se usa esa batería. 

Para escuchar la transformación de luz en sonido, es necesario que el LightSound esté conectado a un dispositivo externo: auriculares o parlantes.

 Para registro y analisis de datos, el LightSound debe estar conectado a la PC, en este caso no necesita batería y el interruptor no tiene acción sobre el dispositivo, por eso, conectado a la PC el dispositivo estará trabajando permanentemente.

Se puede encontrar más información e instrucciones de construcción para LightSound 2.0 en: [https://astrolab.fas.harvard.edu/LightSound.html](https://astrolab.fas.harvard.edu/LightSound.html)