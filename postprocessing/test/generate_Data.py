import pandas as pd
from datetime import datetime, timedelta
import random
import math


random.seed(42)


def generate_data(start_date, num_rows):
    data = []
    current_time = datetime.strptime(start_date, "%d/%m/%Y %H:%M:%S")

    for _ in range(num_rows // 3):
        for i in range(3):
            time_increment = timedelta(milliseconds=i * 333)  # ~333ms apart
            timestamp = current_time + time_increment

            # Wind speed in m/s
            velocidad = random.uniform(0, 5)
            # Wind direction in degrees
            direccion = random.uniform(0, 360)

            data.append(
                [timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"), velocidad, direccion]
            )

        current_time += timedelta(seconds=1)

    return data


def processing_average(df: pd.DataFrame):
    # Comp N-S
    # =A2*COS((B2*PI()/180))
    df["Comp N-S"] = df["Velocity (m/s)"] * df["Direction (grados)"].apply(
        lambda x: math.cos(x * math.pi / 180)
    )

    # Comp E-O
    # =A2*SIN((B2*PI()/180))
    df["Comp E-O"] = df["Velocity (m/s)"] * df["Direction (grados)"].apply(
        lambda x: math.sin(x * math.pi / 180)
    )

    # average Comp N-S of 10 minutes
    # =AVERAGE(C2:C6)
    df["Avg Comp N-S"] = (
        df["Comp N-S"].rolling(window=3).mean()
    )  # window=x --> x rows per second

    # average Comp E-O of 10 minutes
    # =AVERAGE(D2:D6)
    df["Avg Comp E-O"] = df["Comp E-O"].rolling(window=3).mean()

    # Average wind speed
    # =SQRT(E7^2+F7^2)
    df["Avg Wind Speed"] = df["Avg Comp N-S"] ** 2 + df["Avg Comp E-O"] ** 2

    # Average wind direction
    # =ATAN2(E7;F7)*180/PI()
    df["Avg Wind Direction"] = df["Avg Comp N-S"] / df["Avg Comp E-O"] * 180 / math.pi

    print(df)


def main():
    num_rows = 100
    start_date = "22/10/2024 16:47:00"
    data = generate_data(start_date, num_rows)

    df = pd.DataFrame(
        data, columns=["Fecha_Hora", "Velocity (m/s)", "Direction (grados)"]
    )
    df["Fecha_Hora"] = pd.to_datetime(df["Fecha_Hora"], format="%Y-%m-%d %H:%M:%S.%f")

    # processing average
    processing_average(df)


if "__main__" == "__main__":
    main()
