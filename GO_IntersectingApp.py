import matplotlib.pyplot as plt
import PySimpleGUI as sg
import os


def tofloat(numbers: list[str]) -> list[float]:
    try:
        retv = [float(x) for x in numbers]
        if len(retv) != 2:
            raise ValueError
        return retv
    except ValueError:
        raise ValueError("Podano błędne dane")


def intersection(A: list[float], B: list[float], C: list[float], D: list[float]):
    t1_top = ((C[0] - A[0]) * (D[1] - C[1]) - (C[1] - A[1]) * (D[0] - C[0]))
    t1_bot = ((B[0] - A[0]) * (D[1] - C[1]) - (B[1] - A[1]) * (D[0] - C[0]))
    if t1_bot == 0:
        return None
    t1 = t1_top / t1_bot
    t2_top = ((C[0] - A[0]) * (B[1] - A[1]) - (C[1] - A[1]) * (B[0] - A[0]))
    t2_bot = ((B[0] - A[0]) * (D[1] - C[1]) - (B[1] - A[1]) * (D[0] - C[0]))
    if t2_bot == 0:
        return None
    t2 = t2_top / t2_bot
    x = A[0] + t1 * (B[0] - A[0])
    y = A[1] + t1 * (B[1] - A[1])
    if 0 <= t1 <= 1 and 0 <= t2 <= 1:
        return [x, y]
    else:
        return None


def update_plot(graph_img, a: list[float], b: list[float], c: list[float], d: list[float], p: list[float],
                ab_color='red', cd_color='blue', labels=True, ab_linewidth=2, cd_linewidth=2):
    plt.clf()
    plt.plot([a[0], b[0]], [a[1], b[1]], ab_color, label='AB', linewidth=ab_linewidth)
    plt.plot([c[0], d[0]], [c[1], d[1]], cd_color, label='CD', linewidth=cd_linewidth)
    if labels:
        plt.text(a[0], a[1], 'A', color=ab_color, fontsize=12)
        plt.text(b[0], b[1], 'B', color=ab_color, fontsize=12)
        plt.text(c[0], c[1], 'C', color=cd_color, fontsize=12)
        plt.text(d[0], d[1], 'D', color=cd_color, fontsize=12)
    if p is not None:
        plt.plot(p[0], p[1], 'go', label='P')
        if labels:
            plt.text(p[0], p[1], 'P', color='green', fontsize=12)
    plt.scatter([a[0], b[0], c[0], d[0]], [a[1], b[1], c[1], d[1]], color=[ab_color, ab_color, cd_color, cd_color])
    plt.legend()
    plt.savefig('graph.png')
    graph_img.update(filename='graph.png')
    os.remove('graph.png')


def calculate_button(window: sg.Window):
    try:
        a_float = tofloat([window['ax'].get(), window['ay'].get()])
        b_float = tofloat([window['bx'].get(), window['by'].get()])
        c_float = tofloat([window['cx'].get(), window['cy'].get()])
        d_float = tofloat([window['dx'].get(), window['dy'].get()])
    except ValueError:
        sg.popup_error('Podano bledne dane')
        return
    p = intersection(a_float, b_float, c_float, d_float)
    if p is None:
        sg.popup_error('Nie ma punktu przeciecia')
        return
    else:
        window['px'].update(p[0])
        window['py'].update(p[1])


def file_update(window: sg.Window, filename: str):
    try:
        with open(filename, 'r') as f:
            data = f.readlines()
    except FileNotFoundError:
        sg.popup_error('Nie znaleziono pliku')
        return
    if len(data) != 4:
        sg.popup_error('Plik zawiera błędne dane')
        return

    ax_input, ay_input = data[0].split()
    bx_input, by_input = data[1].split()
    cx_input, cy_input = data[2].split()
    dx_input, dy_input = data[3].split()

    window['ax'].update(ax_input)
    window['ay'].update(ay_input)
    window['bx'].update(bx_input)
    window['by'].update(by_input)
    window['cx'].update(cx_input)
    window['cy'].update(cy_input)
    window['dx'].update(dx_input)
    window['dy'].update(dy_input)


def draw(graph_img: sg.Image, window: sg.Window):
    try:
        a_float = tofloat([window['ax'].get(), window['ay'].get()])
        b_float = tofloat([window['bx'].get(), window['by'].get()])
        c_float = tofloat([window['cx'].get(), window['cy'].get()])
        d_float = tofloat([window['dx'].get(), window['dy'].get()])
    except ValueError:
        sg.popup_error('Danew polach są błędne!\nNie można narysować wykresu')
        return
    p = intersection(a_float, b_float, c_float, d_float)
    update_plot(graph_img, a_float, b_float, c_float, d_float, p, window['ab_color'].get(),
                window['cd_color'].get(),
                labels=window['oznaczenia'].get(), ab_linewidth=window['ab_line_width'].get(),
                cd_linewidth=window['cd_line_width'].get())


def save_to_file(window: sg.Window):
    try:
        if window['zapisz_nazwa_pliku'].get() != '':
            with open(window['zapisz_nazwa_pliku'].get(), 'w') as f:
                f.write(f'{window["ax"].get()} {window["ay"].get()}\n')
                f.write(f'{window["bx"].get()} {window["by"].get()}\n')
                f.write(f'{window["cx"].get()} {window["cy"].get()}\n')
                f.write(f'{window["dx"].get()} {window["dy"].get()}\n')
        else:
            raise ValueError('Nie podano nazwy pliku')
    except ValueError as error:
        sg.popup_error(str(error))


def main():
    ax = sg.InputText(size=(10, 1), key='ax')
    ay = sg.InputText(size=(10, 1), key='ay')
    bx = sg.InputText(size=(10, 1), key='bx')
    by = sg.InputText(size=(10, 1), key='by')
    cx = sg.InputText(size=(10, 1), key='cx')
    cy = sg.InputText(size=(10, 1), key='cy')
    dx = sg.InputText(size=(10, 1), key='dx')
    dy = sg.InputText(size=(10, 1), key='dy')
    px = sg.InputText(size=(10, 1), key='px')
    py = sg.InputText(size=(10, 1), key='py')
    A = sg.Frame('', [[ax, ay]])
    B = sg.Frame('', [[bx, by]])
    C = sg.Frame('', [[cx, cy]])
    D = sg.Frame('', [[dx, dy]])
    P = sg.Frame('', [[px, py]])

    colors = ['red', 'blue', 'green', 'yellow', 'black', 'white']
    ab_color_combo = sg.Combo(colors, default_value='red', key='ab_color', size=(10, 4), font=('Helvetica', 12))
    cd_color_combo = sg.Combo(colors, default_value='blue', key='cd_color', size=(10, 4), font=('Helvetica', 12))
    ab_line_width = sg.Combo(list(range(1, 11)), default_value=2, key='ab_line_width', size=(10, 4),
                             font=('Helvetica', 12))
    cd_line_width = sg.Combo(list(range(1, 11)), default_value=2, key='cd_line_width', size=(10, 4),
                             font=('Helvetica', 12))
    oznaczenia = sg.Checkbox('Oznaczenia', default=True, key='oznaczenia')
    wczytaj_z_pliku = sg.FileBrowse('Wczytaj ścieżkę pliku', file_types=(('Pliki tekstowe', '*.txt'),), key='wczytaj_plik')
    wczytaj_po_podanej_nazwie = sg.Button('Wczytaj dane ze ścieżki', key = 'wczytaj_nazwa')
    zapisz = sg.FileSaveAs('Zapisz obliczenia do pliku', file_types=(('Pliki tekstowe', '*.txt'),), key='zapisz_button')
    nazwa_pliku = sg.InputText(size=(82, 1), key='nazwa_pliku')
    zapisz_nazwa_pliku = sg.InputText(size=(25, 1), key='zapisz_nazwa_pliku')
    oblicz = sg.Button('Oblicz', key='oblicz_button', size=(20, 2))
    rysuj = sg.Button('Rysuj', key='rysuj_button', size=(20, 2))

    if os.path.isfile('graph.png'):
        os.remove('graph.png')
    plt.plot(0, 0)
    plt.savefig('graph.png')
    graph_img = sg.Image(filename='graph.png', key='graph')

    layout = [
        [sg.Text('', size=(40, 1))],
        [sg.Text('', size=(40, 20)), sg.pin(graph_img, expand_x=True, expand_y=True), sg.Text('', size=(40, 20))],
        [sg.Text('', size=(27, 1)), sg.Text('Podaj współrzędne punktu A'), A, sg.Text('Podaj współrzędne punktu B'), B],
        [sg.Text('', size=(27, 1)), sg.Text('Podaj współrzędne punktu C'), C, sg.Text('Podaj współrzędne punktu D'), D],
        [sg.Text('', size=(54, 1)), sg.Text('Współrzędne punktu P'), P],
        [sg.Text('', size=(40, 1))],
        [sg.Text('', size=(22, 1)), sg.Text('Kolor odcinka AB'), ab_color_combo, ab_line_width,
         sg.Text('Kolor odcinka CD'), cd_color_combo, cd_line_width, oznaczenia],
        [sg.Text('', size=(14, 1)), wczytaj_po_podanej_nazwie, nazwa_pliku, wczytaj_z_pliku],
        [sg.Text('', size=(50, 1)), zapisz, zapisz_nazwa_pliku],
        [sg.Text('', size=(52, 1)), oblicz, rysuj]
    ]

    window = sg.Window('IntersectingLinesApp', layout)
    window.finalize()

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            if os.path.isfile('graph.png'):
                os.remove('graph.png')
            break

        if event == 'wczytaj_nazwa':
            if values['nazwa_pliku'] != '':
                file_update(window, values['nazwa_pliku'])
            else:
                sg.popup_error('Nie podano nazwy pliku / ścieżki. \n Podaj nazwę pliku / ścieżki.')

        if event == 'wczytaj_plik':
            try:
                selected_file = values['wczytaj_plik']
                if selected_file:
                    window['nazwa_pliku'].update(selected_file)
                else:
                    raise ValueError('Nie wybrano pliku')
            except ValueError as error:
                sg.popup_error(str(error))
        if event == 'oblicz_button':
            calculate_button(window)
        elif event == 'rysuj_button':
            draw(graph_img, window)
        elif event == 'zapisz_button':
            save_to_file(window)


if __name__ == "__main__":
    sg.theme('DarkGreen')
    main()
