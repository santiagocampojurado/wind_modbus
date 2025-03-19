import os
import argparse
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt


PARENT_DIR = r"\\192.168.205.123\aac_server\ANEMOMETRO\MADRID"



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





def main() -> None:
    # initialize the parser
    args = parse_arguments()

    # get the path from the arguments
    base_path = args.path
    if not base_path:
        base_path = PARENT_DIR

    
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
            


            #-------------
            # PLOT
            #-------------
            # plot vel
            plt.figure(figsize=(12, 6))
            plt.plot(df["datetime"], df["vel"], label='vel')
            plt.plot(df["datetime"], df["vel_max"], label='vel_max')
            plt.legend()
            plt.grid()
            # plt.show()


            #---------------------
            # save df and plot
            #---------------------
            # save df
            # replace .csv with _processed.csv
            csv_file = csv_file.replace('.csv', '_processed.csv')
            output_df_file = os.path.join(output_folder, csv_file)           
            df.to_csv(output_df_file, index=False)
            print(f"Saved df to: {output_df_file}")

            # save plot
            output_plot_file = os.path.join(output_folder, csv_file.replace('.csv', '.png'))
            plt.savefig(output_plot_file)
            print(f"Saved plot to: {output_plot_file}")



if __name__ == "__main__":
    main()