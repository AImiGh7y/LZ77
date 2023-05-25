import threading
import PySimpleGUI as sg
import time
import math


def longest_common_substring(s1, s2):
    # Percorre a primeira string e busca a maior correspondência
    maxLongest = 0
    offset = 0
    for i in range(0, len(s1)):
        longest = 0
        if i == len(s1) - len(s2) - 2:
            break
        for j in range(0, len(s2)):
            if i + j < len(s1):
                if s1[i + j] == s2[j]:
                    longest = longest + 1
                    if maxLongest < longest:
                        maxLongest = longest
                        offset = i
                else:
                    break
            else:
                break
    return maxLongest, offset

def encode_lz77(text, searchWindowSize, previewWindowSize):
    encodedNumbers = []
    encodedSizes = []
    encodedLetters = []
    i = 0
    while i < len(text):
        if i < previewWindowSize:
            encodedNumbers.append(0)
            encodedSizes.append(0)
            encodedLetters.append(text[i])
            i = i + 1
        else:
            previewString = text[i:i + previewWindowSize]
            searchWindowOffset = 0
            if i < searchWindowSize:
                searchWindowOffset = i
            else:
                searchWindowOffset = searchWindowSize
            searchString = text[i - searchWindowOffset:i]
            result = longest_common_substring(searchString + previewString, previewString)
            nextLetter = ''
            if result[0] == len(previewString):
                if i + result[0] == len(text):
                    nextLetter = ''
                else:
                    nextLetter = text[i + previewWindowSize]
            else:
                nextLetter = previewString[result[0]]
            if result[0] == 0:
                encodedNumbers.append(0)
                encodedSizes.append(0)
                encodedLetters.append(nextLetter)
            else:
                encodedNumbers.append(searchWindowOffset - result[1])
                encodedSizes.append(result[0])
                encodedLetters.append(nextLetter)
            i = i + result[0] + 1
    return encodedNumbers, encodedSizes, encodedLetters


def decode_lz77(encodedNumbers, encodedSizes, encodedLetters):
    i = 0
    decodedString = []
    while i < len(encodedNumbers):
        if encodedNumbers[i] == 0:
            decodedString.append(encodedLetters[i])
        else:
            currentSize = len(decodedString)
            for j in range(0, encodedSizes[i]):
                decodedString.append(decodedString[currentSize - encodedNumbers[i] + j])
            decodedString.append(encodedLetters[i])
        i = i + 1
    return decodedString

def countBits(number):
    return int((math.log(number) / math.log(2)) + 1)

def openFile(filename):
    try:
        with open(filename, "r") as f:
            stringToEncode = f.read()
            f.close()
            return stringToEncode
    except FileNotFoundError:
        return None


def encode_decode_thread(stringToEncode, searchWindowSize, previewWindowSize, window):
    # Compressão
    start_time = time.time()
    encodedNumbers, encodedSizes, encodedLetters = encode_lz77(stringToEncode, searchWindowSize, previewWindowSize)
    end_time = time.time()
    update_ui_compress(encodedNumbers, encodedSizes, encodedLetters, window)
    compression_time = end_time - start_time

    # Descompressão
    start_time = time.time()
    decodedString = decode_lz77(encodedNumbers, encodedSizes, encodedLetters)
    end_time = time.time()
    update_ui_decompress(decodedString, window)
    decompression_time = end_time - start_time

    # Rácio de compressão
    total_bits = len(stringToEncode) * 8
    token_length = len(encodedNumbers) * (8 + countBits(searchWindowSize) + countBits(previewWindowSize))
    compression_ratio = total_bits / token_length

    # Exibir informações adicionais
    window['-CONTAINER-'].print("\n‎Tempo de Compressão: {0:.2f} ms".format(compression_time * 1000), text_color='green')
    window['-CONTAINER-'].print("Tempo de Descompressão: {0:.2f} ms".format(decompression_time * 1000), text_color='green')
    window['-CONTAINER-'].print("Rácio de Compressão: {0:.2f}".format(compression_ratio), text_color='green')
    window.refresh()

def update_ui_compress(encodedNumbers, encodedSizes, encodedLetters, window):
    for i in range(len(encodedNumbers)):
        token = "({0},{1},{2})".format(encodedNumbers[i], encodedSizes[i], encodedLetters[i])
        window['-CONTAINER-'].print(token, end='\t‎', text_color='blue')
        window.refresh()


def update_ui_decompress(decodedString, window):
    decoded_string = "".join(decodedString)
    window['-CONTAINER-'].print("\n\nDecoded string:\n" + decoded_string + '\n', text_color='green')
    window.refresh()




# -----------------------------------------------------------------------------------------------------------------------
#                                                       LZ77 GUI
# -----------------------------------------------------------------------------------------------------------------------
sg.theme('TealMono')

menu_def = [['File', ['Open']]]

layout = [
    [sg.Menu(menu_def, tearoff=True)],
    [sg.Text('Tamanho da Janela', font=('Arial', 12), size=(15, 1)), sg.InputText('', key='-SEARCH-', size=(10, 1))],
    [sg.Text('Tamanho do buffer', font=('Arial', 12), size=(15, 1)), sg.InputText('', key='-LOOKAHEAD-', size=(10, 1))],
    [sg.Multiline(size=(90, 30), key='-CONTAINER-')],
    [sg.Submit('Executar'), sg.Cancel('Limpar')]
]

filename = ''
window = sg.Window('LZ77 Algorithm', layout, default_element_size=(80, 3), grab_anywhere=False)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Open':
        filename = sg.popup_get_file('Open file')
        if filename:
            stringToEncode = openFile(filename)
            if stringToEncode is not None:
                window['-CONTAINER-'].update("")
    elif event == 'Executar':
        if not filename:
            sg.popup('Por favor, abra um arquivo primeiro.')
        else:
            searchWindowSize = int(values['-SEARCH-'])
            previewWindowSize = int(values['-LOOKAHEAD-'])
            threading.Thread(target=encode_decode_thread, args=(stringToEncode, searchWindowSize, previewWindowSize, window)).start()
    elif event == 'Limpar':
        window['-SEARCH-'].update('')
        window['-LOOKAHEAD-'].update('')
        window['-CONTAINER-'].update('')

window.close()