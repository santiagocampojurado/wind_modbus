import pandas as pd
import os



PARENT_DIR = r"\\192.168.205.123\aac_server\ANEMOMETRO"



def main():
    list_csv_files = os.listdir(PARENT_DIR)
    print("CSV Files:", list_csv_files)

    df_list = []
    for file in list_csv_files:
        if file.endswith(".csv"):
            file_path = os.path.join(PARENT_DIR, file)
            df = pd.read_csv(file_path)

            df["Fecha"] = pd.to_datetime(df["Fecha"], format="%d/%m/%y")
            df["Hora"] = pd.to_datetime(df["Hora"], format="%H:%M:%S")
            df["Fecha_Hora"] = pd.to_datetime(df["Fecha"].dt.strftime("%Y-%m-%d") + " " + df["Hora"].dt.strftime("%H:%M:%S"))

            df.drop(columns=["Fecha", "Hora"], inplace=True)
            df_list.append(df)

    # concatenate
    final_df = pd.concat(df_list)
    final_df.sort_values(by="Fecha_Hora", inplace=True)
    final_df.reset_index(drop=True, inplace=True)
    final_df.dropna(inplace=True)
    print(final_df)

    # change order of columns
    # Velocidad (m/s), Dirección (grados), Fecha_Hora
    final_df = final_df[['Fecha_Hora', 'Velocidad (m/s)', 'Dirección (grados)']]

    # add 2 hours to the time
    final_df["Fecha_Hora"] = final_df["Fecha_Hora"] + pd.Timedelta(hours=2, minutes=9)

    #save df
    final_df.to_csv("wind_concat.csv", index=False)

    min_date = final_df["Fecha_Hora"].min()
    max_date = final_df["Fecha_Hora"].max()
    print(f"The df start date is: {min_date}")
    print(f"The df end date is: {max_date}")



if __name__ == "__main__":
    main()
