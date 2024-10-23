#!/usr/bin/env python

import drivers
import minimalmodbus
import time
import datetime
import csv
import os


display = drivers.Lcd()

def connect_sensor():
    """
    Establishes communication with the wind sensor and returns the instrument object.
    """
    try:
        sensor = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
        sensor.serial.baudrate = 4800
        sensor.serial.timeout = None
        
        test_value = sensor.read_register(0, 2)
        print(f"Connection successful. Test value: {test_value}")
        
        return sensor

    except Exception as e:
        print(f"Communication error: {e}")
        exit(1)


def create_log_file():
    """
    Creates a directory for logging and returns the filename for storing CSV data.
    """
    current_dir = os.getcwd()
    log_file_name = "log"
    log_path = os.path.join(current_dir, log_file_name)

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    fecha_comp_val = datetime.datetime.now()
    fecha_val = fecha_comp_val.strftime("%d-%m-%y")  # date in DD-MM-YY format
    hora_val = fecha_comp_val.strftime("%H-%M-%S")   # time in HH-MM-SS format
    filename = f"{log_path}/wind_{fecha_val}_{hora_val}.csv"

    return filename


def read_sensor_data(sensor, writer):
    """
    Reads wind speed, direction, and max speed from the sensor and writes to CSV.
    """
    while True:
        try:
            #  wind speed, direction, and max speed from registers
            velocidad_val = sensor.read_register(0, 2)
            direccion_val = sensor.read_register(1, 0)
            maximo_val = sensor.read_register(2, 2)

            # current date and time
            fecha_comp_val = datetime.datetime.now()
            fecha_val = fecha_comp_val.strftime("%d/%m/%y")
            hora_val = fecha_comp_val.strftime("%H:%M:%S")


            display.lcd_display_string(f"Vel: {velocidad_val} m/s", 1)
            display.lcd_display_string(f"Dir: {direccion_val} grd", 2)

            print(f"{fecha_val} {hora_val} - Velocidad: {velocidad_val} m/s, "
                  f"Dirección: {direccion_val} grados, Máximo: {maximo_val} m/s")

            writer.writerow([fecha_val, hora_val, velocidad_val, direccion_val, maximo_val])
            time.sleep(1)
            display.lcd_clear()

        except Exception as e:
            print(f"Read error: {e}")
            break


def lectura(sensor, filename):
    """
    Opens the CSV file and continuously logs sensor data until interrupted.
    """
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Fecha', 'Hora', 'Velocidad (m/s)', 'Dirección (grados)', 'Velocidad Máxima (m/s)'])

        try:
            read_sensor_data(sensor, writer)

        except KeyboardInterrupt:
            print("Interrupted! Cleaning up.")
            display.lcd_clear()


def main():
    sensor = connect_sensor()
    filename = create_log_file()
    lectura(sensor, filename)


if __name__ == "__main__":
    main()
