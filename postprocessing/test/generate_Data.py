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
            # round to 2 decimal
            velocidad = round(velocidad, 2)
            # Wind direction in degrees
            direccion = random.uniform(0, 360)
            # round to 2 decimal
            direccion = round(direccion, 2)

            data.append(
                [timestamp.strftime("%Y-%m-%d %H:%M:%S.%f"), velocidad, direccion]
            )

        current_time += timedelta(seconds=1)

    return data



def convert_date_index(df: pd.DataFrame):
    df["Fecha_Hora"] = pd.to_datetime(df["Fecha_Hora"], format="%Y-%m-%d %H:%M:%S.%f")
    df.set_index("Fecha_Hora", inplace=True)
    return df




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
    
    print(df)
    print(f"The df start date is: {df.index[0]}")
    print(f"The df end date is: {df.index[-1]}")
    print(f"The df is {df.index[-1] - df.index[0]} long")
    

    # 10-minute intervals for Comp N-S and Comp E-O
    # resample_df = df[['Comp N-S', 'Comp E-O']].resample("10min").mean()
    # resample_df = resample_df.round(2)

    # average wind speed
    # =SQRT(E7^2 + F7^2)
    df["Avg Wind Speed"] = (
        df["Comp N-S"] ** 2 + df["Comp E-O"] ** 2
    ) ** 0.5 # remember that ** 0.5 is the same as square root

    # average wind direction
    # =ATAN2(E7, F7) * 180 / PI()
    df["Avg Wind Direction"] = df.apply(
        lambda x: math.atan2(x["Comp N-S"], x["Comp E-O"]) * 180 / math.pi, axis=1
    )

    print(df)




def main():
    num_rows = 100000
    start_date = "22/10/2024 16:47:00"
    data = generate_data(start_date, num_rows)

    df = pd.DataFrame(
        data, columns=["Fecha_Hora", "Velocity (m/s)", "Direction (grados)"]
    )
    df["Fecha_Hora"] = pd.to_datetime(df["Fecha_Hora"], format="%Y-%m-%d %H:%M:%S.%f")

    # processing average
    df = convert_date_index(df)
    processing_average(df)


if "__main__" == "__main__":
    main()
