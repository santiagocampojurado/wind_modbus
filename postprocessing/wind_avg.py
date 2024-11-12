import pandas as pd
import os
import math

def processing_average(df: pd.DataFrame):
    # Comp N-S
    # =A2*COS((B2*PI()/180))
    df["Comp N-S"] = df["Velocidad (m/s)"] * df["Dirección (grados)"].apply(
        lambda x: math.cos(x * math.pi / 180)
    )
    df["Comp N-S"] = df["Comp N-S"].round(2)

    # Comp E-O
    # =A2*SIN((B2*PI()/180))
    df["Comp E-O"] = df["Velocidad (m/s)"] * df["Dirección (grados)"].apply(
        lambda x: math.sin(x * math.pi / 180)
    )
    df["Comp E-O"] = df["Comp E-O"].round(2)

    # 10-minute intervals
    resampled_df = df.resample("10T").mean()
    resampled_df["Avg Comp N-S"] = resampled_df["Comp N-S"]
    resampled_df["Avg Comp E-O"] = resampled_df["Comp E-O"]

    # average wind speed
    # =SQRT(E7^2 + F7^2)
    resampled_df["Avg Wind Speed"] = (resampled_df["Comp N-S"]**2 + resampled_df["Comp E-O"]**2)**0.5

    # # average wind direction
    # =ATAN2(E7, F7) * 180 / PI()
    resampled_df["Avg Wind Direction"] = resampled_df.apply(
        lambda x: math.atan2(x["Comp N-S"], x["Comp E-O"]) * 180 / math.pi, axis=1
    )
    resampled_df["Avg Wind Direction"] = resampled_df["Avg Wind Direction"].round(2)
    resampled_df.dropna(inplace=True)

    # round to 2 decimal
    resampled_df["Velocidad (m/s)"] = resampled_df["Velocidad (m/s)"].round(2)
    resampled_df["Dirección (grados)"] = resampled_df["Dirección (grados)"].round(2)
    resampled_df["Comp N-S"] = resampled_df["Comp N-S"].round(2)
    resampled_df["Comp E-O"] = resampled_df["Comp E-O"].round(2)
    resampled_df["Avg Comp N-S"] = resampled_df["Avg Comp N-S"].round(2)
    resampled_df["Avg Comp E-O"] = resampled_df["Avg Comp E-O"].round(2)
    resampled_df["Avg Wind Speed"] = resampled_df["Avg Wind Speed"].round(2)
    resampled_df["Avg Wind Direction"] = resampled_df["Avg Wind Direction"].round(2)
    print(resampled_df)


    # save
    resampled_df.to_csv("wind_avg.csv", index=True)
    print("File saved as wind_avg.csv")




def main():
    csv_file = r"C:\Users\scjaa\Documents\GitHubRepos\wind_modbus\prepro\wind_concat.csv"
    df = pd.read_csv(csv_file)

    df["Fecha_Hora"] = pd.to_datetime(df["Fecha_Hora"])
    df.set_index("Fecha_Hora", inplace=True)
    df.dropna(inplace=True)
    
    processing_average(df)




if __name__ == "__main__":
    main()
