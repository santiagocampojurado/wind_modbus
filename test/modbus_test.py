import minimalmodbus
import time
import datetime

try:
    estacion = minimalmodbus.Instrument('/dev/ttyUSB0', 1)  # ttyUSB0
    estacion.serial.baudrate = 4800
    estacion.serial.timeout = None

    test_value = estacion.read_register(0, 2)
    print(f"Comunicación establecida con éxito. Valor de prueba: {test_value}")

except Exception as e:
    print(f"Error de comunicación: {e}")
    exit(1)

# reading wind speed and direction continuously and print it
def lectura():
    while True:
        try:
            # wind speed, direction, and max speed
            velocidad_val = estacion.read_register(0, 2)
            direccion_val = estacion.read_register(1, 0)
            maximo_val = estacion.read_register(2, 2)
            
            # date and time
            fecha_comp_val = datetime.datetime.now()
            fecha_val = fecha_comp_val.strftime("%d/%m/%y")
            hora_val = fecha_comp_val.strftime("%H:%M:%S")
            
            print(f"{fecha_val} {hora_val} - Velocidad: {velocidad_val} m/s, Dirección: {direccion_val} grados, Máximo: {maximo_val} m/s")
            time.sleep(1)
        
        except Exception as e:
            print(f"Error de lectura: {e}")
            break

lectura()
