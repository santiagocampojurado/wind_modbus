import pandas as pd
import os
import math
import argparse
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import logging


PARENT_DIR = r"\\192.168.205.123\aac_server\ANEMOMETRO\MADRID"




def processing_average(df: pd.DataFrame,title: str, output_folder: str) -> None:
    df.set_index("datetime", inplace=True)


    #-----------------
    # componentes
    #-----------------
    # Comp N-S
    # =A2*COS((B2*PI()/180))
    df["Comp N-S"] = df["vel"] * df["dir"].apply(
        lambda x: math.cos(x * math.pi / (180))
    )
    df["Comp N-S"] = df["Comp N-S"].round(2)

    # Comp E-O
    # =A2*SIN((B2*PI()/180))
    df["Comp E-O"] = df["vel"] * df["dir"].apply(
        lambda x: math.sin(x * math.pi / 180 )
    )
    df["Comp E-O"] = df["Comp E-O"].round(2)



    #~FOR VEL MAX
    # Comp N-S
    # =C2*COS((D2*PI()/180))
    df["Comp N-S Max"] = df["vel_max"] * df["dir"].apply(
        lambda x: math.cos(x * math.pi / 180)
    )
    df["Comp N-S Max"] = df["Comp N-S Max"].round(2)

    # Comp E-O
    # =C2*SIN((D2*PI()/180))
    df["Comp E-O Max"] = df["vel_max"] * df["dir"].apply(
        lambda x: math.sin(x * math.pi / 180)
    )
    df["Comp E-O Max"] = df["Comp E-O Max"].round(2)


    # 10-minute intervals
    resampled_df = df.resample("10T").mean()

    # for components
    resampled_df["Avg Comp N-S"] = resampled_df["Comp N-S"]
    resampled_df["Avg Comp E-O"] = resampled_df["Comp E-O"]

    # for vel_max
    resampled_df["Avg Comp N-S Max"] = resampled_df["Comp N-S Max"]
    resampled_df["Avg Comp E-O Max"] = resampled_df["Comp E-O Max"]

    


    #---------------------
    # AVERAGES
    #---------------------
    # WIN SPEED
    # =SQRT(E7^2 + F7^2)
    resampled_df["Avg Wind Speed"] = (resampled_df["Comp N-S"]**2 + resampled_df["Comp E-O"]**2)**0.5

    #WIN SPEED MAX
    # =MAX(G7:G16)
    resampled_df["Avg Wind Speed Max"] = resampled_df["vel_max"]


    # WIND DIRECTION
    # =ATAN2(E7, F7) * 180 / PI()
    resampled_df["Avg Wind Direction"] = resampled_df.apply(
        lambda x: math.atan2(x["Comp N-S"], x["Comp E-O"]) * 180 / math.pi, axis=1
    )
    resampled_df["Avg Wind Direction"] = resampled_df["Avg Wind Direction"].round(2)
    resampled_df.dropna(inplace=True)



    # round to 2 decimal
    resampled_df["vel"] = resampled_df["vel"].round(2)
    resampled_df["dir"] = resampled_df["dir"].round(2)
    resampled_df["vel_max"] = resampled_df["vel_max"].round(2)  
    resampled_df["Comp N-S"] = resampled_df["Comp N-S"].round(2)
    resampled_df["Comp E-O"] = resampled_df["Comp E-O"].round(2)
    resampled_df["Comp N-S Max"] = resampled_df["Comp N-S Max"].round(2)
    resampled_df["Comp E-O Max"] = resampled_df["Comp E-O Max"].round(2)
    resampled_df["Avg Comp N-S"] = resampled_df["Avg Comp N-S"].round(2)
    resampled_df["Avg Comp E-O"] = resampled_df["Avg Comp E-O"].round(2)
    resampled_df["Avg Comp N-S Max"] = resampled_df["Avg Comp N-S Max"].round(2)
    resampled_df["Avg Comp E-O Max"] = resampled_df["Avg Comp E-O Max"].round(2)
    resampled_df["Avg Wind Speed"] = resampled_df["Avg Wind Speed"].round(2)
    resampled_df["Avg Wind Direction"] = resampled_df["Avg Wind Direction"].round(2)
    resampled_df["Avg Wind Speed Max"] = resampled_df["Avg Wind Speed Max"].round(2)
    # print(resampled_df)


    #---------------------
    # add 180 + 180 to the negative values of the wind direction 
    # to chen
    #---------------------
    resampled_df["Avg Wind Direction"] = resampled_df["Avg Wind Direction"].apply(
        lambda x: x + 360 if x < 0 else x 
    )



    # save
    output_path = os.path.join(output_folder, f"{title}_{df.index[0].strftime('%Y-%m-%d')}.csv")
    resampled_df.to_csv(output_path, index=True)
    print(f"Saved file: {output_path}")



    # -------------
    # PLOTS
    # -------------
    plot_wind_avg_speed(resampled_df,title, output_folder)
    plot_wind_avg_direction(resampled_df, title, output_folder)




def plot_wind_avg_speed(df: pd.DataFrame,title: str, output_folder: str) -> None:
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["Avg Wind Speed"], label="Speed")
    # plot '*'
    # plt.plot(df.index, df["Avg Wind Speed Max"], label="Speed Max", marker='*')
    plt.plot(df.index, df["Avg Wind Speed Max"], label="Speed Max", linestyle='--')
    plt.xlabel("Datetime")
    plt.ylabel("Wind Speed (m/s)")
    plt.title(f"Wind Speed {title}")
    
    # legend out of the plot
    plt.legend(loc='center left', bbox_to_anchor=(1, 1))
    plt.grid(True)

    # limit the x-axis
    plt.xlim(df.index[0], df.index[-1])
    
    ax = plt.gca()  # Get current axes
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

    plt.xticks(rotation=90)
    plt.tight_layout()


    # save plot
    filename = f"{title}_wind_speed"
    output_path = os.path.join(output_folder, f"{filename}_{df.index[0].strftime('%Y-%m-%d')}.png")
    plt.savefig(output_path)
    print(f"Saved plot: {output_path}")


    # save plot xlsx
    output_xlsx_path = os.path.join(output_folder, f"{filename}_{df.index[0].strftime('%Y-%m-%d')}.xlsx")
    # slect order
    # datetime; Avg Wind Speed; Avg Wind Speed Max; Avg Wind Direction
    df_xlsx = df[['Avg Wind Speed', 'Avg Wind Speed Max', 'Avg Wind Direction']]
    df_xlsx.to_excel(output_xlsx_path)
    print(f"Saved xlsx: {output_xlsx_path}")



def plot_wind_avg_direction(df: pd.DataFrame, title: str, output_folder: str) -> None:
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["Avg Wind Direction"], label="Direction")

    plt.xlabel("Datetime")
    plt.ylabel("Wind Direction (degrees)")
    plt.title(f"Wind Direction {title}")

    # legend out of the plot
    plt.legend(loc='center left', bbox_to_anchor=(1, 1))
    plt.grid(True)

    # plt.ylim(180, -180)
    plt.xlim(df.index[0], df.index[-1])

    ax = plt.gca()  # Get current axes
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

    plt.xticks(rotation=90)
    plt.tight_layout()


    # save plot
    filename = f"{title}_wind_direction"
    output_path = os.path.join(output_folder, f"{filename}_{df.index[0].strftime('%Y-%m-%d')}.png")
    plt.savefig(output_path)
    print(f"Saved plot: {output_path}")






def find_wind_folders(base_path: str):
    for root, dirs, files in os.walk(base_path):
        if '3-Medidas' in dirs:
            medidas_path = os.path.join(root, '3-Medidas')
            # lsit subfolder in 3-Medidas
            for item in os.listdir(medidas_path):
                item_path = os.path.join(medidas_path, item)
                if os.path.isdir(item_path):
                    print(f"Found wind folder: {item_path}")
                    yield item_path



def get_csv_wind_files(path: str) -> list:
    audio_files = [file for file in os.listdir(path) if file.lower().endswith('.csv')]
    return audio_files


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Exploring wind sensor data')
    parser.add_argument('-p', '--path', type=str, required=False, help='Directory to be processed')
    return parser.parse_args()





def main():
    # initialize the parser
    args = parse_arguments()

    # get the path from the arguments
    base_path = args.path
    if not base_path:
        base_path = PARENT_DIR

    title = base_path.split("\\")[-1]


    wind_folders = list(find_wind_folders(base_path))
    print(f"Found {len(wind_folders)} folders to process. --> {wind_folders}")
    
    for subfolder in tqdm(wind_folders, desc='Processing folders'):
        print()
        print(f"Processing folder: {subfolder}")

        # change name 3-Medidas to 5-Resultados
        output_folder = subfolder.replace('3-Medidas', '5-Resultados')
        # make the folder if it does not exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)


        # get csv files        
        csv_files = get_csv_wind_files(subfolder)
        print(f"Found {len(csv_files)} csv files in {subfolder}")


        #-------------------
        # process csv files
        #-------------------
        for csv_file in tqdm(csv_files, desc='Processing csv files'):
            print(f"Processing file: {csv_file}")

            #read the csv file
            csv_path = os.path.join(subfolder, csv_file)
            df = pd.read_csv(csv_path, sep=';')


            df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
            df["time"] = pd.to_datetime(df["time"], format="%H:%M:%S")
            df["datetime"] = pd.to_datetime(df["date"].dt.strftime("%Y-%m-%d") + " " + df["time"].dt.strftime("%H:%M:%S"))

            df.drop(columns=["date", "time"], inplace=True)

            # change order of columns
            # datetime; vel;  dir;  vel_max
            df = df[['datetime', 'vel', 'dir', 'vel_max']]


            # add 8 hours to the time
            df["datetime"] = df["datetime"] + pd.Timedelta(hours=8)
            # df["datetime"] = df["datetime"] - pd.Timedelta(minutes=10)
    

            #------------------------
            # processing average wind
            #------------------------
            print()
            print("Processing average wind")
            processing_average(df,title, output_folder)




if __name__ == "__main__":
    main()
