#! /usr/bin/env python

import drivers
import minimalmodbus
import time
import datetime

display = drivers.Lcd()

try:
    estacion = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # ttyUSB0
    estacion.serial.baudrate = 4800
    estacion.serial.timeout = None

    test_value = estacion.read_register(0, 2)
    print(f"Comunicación establecida con éxito. Valor de prueba: {test_value}")

except Exception as e:
    print(f"Error de comunicación: {e}")
    exit(1)



def lectura():
    try:
        while True:
            try:
                # read wind speed, direction, and max speed
                velocidad_val = estacion.read_register(0, 2)
                direccion_val = estacion.read_register(1, 0)
                maximo_val = estacion.read_register(2, 2)

                # date and time
                fecha_comp_val = datetime.datetime.now()
                fecha_val = fecha_comp_val.strftime("%d/%m/%y")
                hora_val = fecha_comp_val.strftime("%H:%M:%S")

                # display 
                display.lcd_display_string(f"Vel: {velocidad_val}m/s",1)
                display.lcd_display_string(f"Dir: {direccion_val}gd", 2)

                print(f"{fecha_val} {hora_val} - Velocidad: {velocidad_val} m/s, Dirección: {direccion_val} grados, Máximo: {maximo_val} m/s")
                time.sleep(1)
                display.lcd_clear()

            except Exception as e:
                print(f"Error de lectura: {e}")
                break

    except KeyboardInterrupt:
        print("Cleaning up!")
        display.lcd_clear()

lectura()
