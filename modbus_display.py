#! /usr/bin/env python

import drivers
import minimalmodbus
import time
import datetime
import csv
import os



display = drivers.Lcd()


try:
    estacion = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # ttyUSB0
    estacion.serial.baudrate = 4800
    estacion.serial.timeout = None

    #connection with the sensor
    test_value = estacion.read_register(0, 2)
    print(f"Comunicación establecida con éxito. Valor de prueba: {test_value}")

except Exception as e:
    print(f"Error de comunicación: {e}")
    exit(1)


current_dir = os.getcwd()
log_file_name = "log"
log_path = os.path.join(current_dir, log_file_name)

if not os.path.exists(log_path):
    os.makedirs(log_path)

fecha_comp_val = datetime.datetime.now()
fecha_val = fecha_comp_val.strftime("%d-%m-%y")  # date in DD-MM-YY format
hora_val = fecha_comp_val.strftime("%H-%M-%S")  # time in HH-MM-SS format
filename = f"{log_path}/wind_{fecha_val}_{hora_val}.csv"


def lectura():
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Fecha', 'Hora', 'Velocidad (m/s)', 'Dirección (grados)', 'Velocidad Máxima (m/s)'])


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

                    display.lcd_display_string(f"Vel: {velocidad_val}m/s", 1)
                    display.lcd_display_string(f"Dir: {direccion_val}grd", 2)


                    print(f"{fecha_val} {hora_val} - Velocidad: {velocidad_val} m/s, Dirección: {direccion_val} grados, Máximo: {maximo_val} m/s")

                    # data to csv
                    writer.writerow([fecha_val, hora_val, velocidad_val, direccion_val, maximo_val])
                    time.sleep(1)
                    display.lcd_clear()

                except Exception as e:
                    print(f"Error de lectura: {e}")
                    break

        except KeyboardInterrupt:
            print("Cleaning up!")
            display.lcd_clear()


def main():
    lectura()


if __name__ == "__main__":
    main()
