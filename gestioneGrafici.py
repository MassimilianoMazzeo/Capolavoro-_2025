import serial

import time

import threading

import dearpygui.dearpygui as dpg

# Setup serial connection

try:

    ser = serial.Serial('COM6', 9600)

except serial.SerialException as e:

    print(f"Errore apertura porta seriale: {e}")

    exit()

# Shared data buffers

dati_temp = []

dati_um = []

# Locks for synchronizing access

dati_lock = threading.Lock()

grafici_lock = threading.Lock()


def leggi_seriale():
    global ser
    """Reads data from the serial port and stores it in shared data buffers."""

    while True:

        try:

            dati_bytes = ser.readline()

            dati_str = dati_bytes.decode('utf-8').strip()

            # Debugging: print raw data to console

            print(f"Dati grezzi dalla seriale: {dati_str}")

            dati = dati_str.split(',')

            if len(dati) == 2:

                try:

                    # Try to convert the values to floats

                    temp, umidita = map(float, dati)

                    with dati_lock:

                        # Append new data to the lists

                        dati_temp.append({'temperatura': temp, 'timestamp': time.time()})

                        dati_um.append({'umidita': umidita, 'timestamp': time.time()})

                        # Limit the length of data buffers

                        max_data_points = 100

                        if len(dati_temp) > max_data_points:
                            dati_temp.pop(0)

                        if len(dati_um) > max_data_points:
                            dati_um.pop(0)

                    # Trigger an immediate graph update after data read

                    aggiorna_grafici()

                except ValueError:

                    print(f"Errore di conversione dati: {dati_str}")

            else:

                print(f"Formato dati seriali non valido: {dati_str}")

        except serial.SerialException as e:

            print(f"Errore di lettura seriale: {e}")

            break

        except UnicodeDecodeError as e:

            print(f"Errore di decodifica dati: {e}")

        time.sleep(0.1)


def aggiorna_grafici():
    """Updates the graphs with the latest data."""

    with grafici_lock:  # Use lock to ensure the update is safe

        with dati_lock:
            # Prepare data for the graphs

            temp_x = [d['timestamp'] for d in dati_temp]

            temp_y = [d['temperatura'] for d in dati_temp]

            um_x = [d['timestamp'] for d in dati_um]

            um_y = [d['umidita'] for d in dati_um]

        # Update the graph values immediately

        dpg.set_value("temperatura_series", [list(temp_x), list(temp_y)])

        dpg.set_value("umidita_series", [list(um_x), list(um_y)])


# GUI setup using DearPyGui

dpg.create_context()

dpg.create_viewport(title='Termostato con ARDUINO', width=800, height=600)

# Create window and plots

with dpg.window(label="Grafici", width=2000, height=1000):
    with dpg.plot(label="Temperatura", height=280, width=-1):
        dpg.add_plot_axis(dpg.mvXAxis, label="Tempo", tag="time_axis_temp")

        dpg.add_plot_axis(dpg.mvYAxis, label="Temperatura (°C)", tag="temperatura_axis")

        dpg.add_line_series([], [], label="Temperatura", parent="temperatura_axis", tag="temperatura_series")

    with dpg.plot(label="Umidità", height=280, width=-1):
        dpg.add_plot_axis(dpg.mvXAxis, label="Tempo", tag="time_axis_um")

        dpg.add_plot_axis(dpg.mvYAxis, label="Umidità (%)", tag="umidita_axis")

        dpg.add_line_series([], [], label="Umidità", parent="umidita_axis", tag="umidita_series")

# Start the serial reading thread

thread_seriale = threading.Thread(target=leggi_seriale, daemon=True)

thread_seriale.start()

# Start the DearPyGui event loop

dpg.setup_dearpygui()

dpg.show_viewport()

dpg.start_dearpygui()

dpg.destroy_context()
