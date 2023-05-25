import PySimpleGUI as sg
import time
import math


def longest_common_substring(s1, s2):
    # go along the first string and search for the longest match
    maxLongest = 0
    offset = 0
    for i in range(0, len(s1)):
        longest = 0
        if ((i == len(s1) - len(s2) - 2)):
            break
        for j in range(0, len(s2)):
            if (i + j < len(s1)):
                if s1[i + j] == s2[j]:
                    longest = longest + 1
                    if (maxLongest < longest):
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
    window['-CONTAINER-'].update(window[
                                     '-CONTAINER-'].get() + "-------------------------------------------------------------------------------------------------\n‎\n‎\t\tA iniciar Compressão...\n‎-------------------------------------------------------------------------------------------------\n‎")
    while i < len(text):
        if i < previewWindowSize:
            # print ("<{0}, {1}, {2}>".format(0, 0, text[i]))
            encodedNumbers.append(0)
            encodedSizes.append(0)
            encodedLetters.append(text[i])
            i = i + 1
        else:
            previewString = text[i:i + previewWindowSize]
            searchWindowOffset = 0
            if (i < searchWindowSize):
                searchWindowOffset = i
            else:
                searchWindowOffset = searchWindowSize
            searchString = text[i - searchWindowOffset:i]
            # print(previewString)
            result = longest_common_substring(searchString + previewString,
                                              previewString)  # searchString + prevString, prevString
            nextLetter = ''
            if (result[0] == len(previewString)):
                if (i + result[0] == len(text)):
                    nextLetter = ''
                else:
                    nextLetter = text[i + previewWindowSize]
            else:
                nextLetter = previewString[result[0]]
            if (result[0] == 0):
                window['-CONTAINER-'].update(window[
                                                 '-CONTAINER-'].get() + "\n‎Dicionário: [" + searchString + "]\n‎Buffer: [" + previewString + "]\n‎Token: ({0}, {1}, {2})\n‎".format(
                    0, 0, nextLetter))
                encodedNumbers.append(0)
                encodedSizes.append(0)
                encodedLetters.append(nextLetter)
            else:
                window['-CONTAINER-'].update(window[
                                                 '-CONTAINER-'].get() + "\n‎Dicionário: [" + searchString + "]\n‎Buffer: [" + previewString + "]\n‎Token: ({0}, {1}, {2})\n‎".format(
                    searchWindowOffset - result[1], result[0], nextLetter))
                encodedNumbers.append(searchWindowOffset - result[1])
                encodedSizes.append(result[0])
                encodedLetters.append(nextLetter)
            i = i + result[0] + 1
    return encodedNumbers, encodedSizes, encodedLetters


def decode_lz77(encodedNumbers, encodedSizes, encodedLetters):
    window['-CONTAINER-'].update(window[
                                     '-CONTAINER-'].get() + "-------------------------------------------------------------------------------------------------\n‎\n‎\t\tA iniciar Descompressão...\n‎-------------------------------------------------------------------------------------------------\n‎Tokens:\n‎")

    i = 0
    decodedString = []
    while i < len(encodedNumbers):
        window['-CONTAINER-'].update(
            window['-CONTAINER-'].get() + "({0},{1},{2})\t‎".format(encodedNumbers[i], encodedSizes[i], encodedLetters[i]))
        if (encodedNumbers[i] == 0):
            decodedString.append(encodedLetters[i])
        else:
            currentSize = len(decodedString)
            for j in range(0, encodedSizes[i]):
                decodedString.append(decodedString[currentSize - encodedNumbers[i] + j])
            decodedString.append(encodedLetters[i])
        string = "".join(decodedString)
        window['-CONTAINER-'].update(
            window['-CONTAINER-'].get() + "'" + string + "'\n‎")
        i = i + 1
    return decodedString


def countBits(number):
    # log function in base 2
    # take only integer part
    return int((math.log(number) /
                math.log(2)) + 1)


def openFile(filename):
    try:
        with open(filename, "r") as f:
            stringToEncode = f.read()
            f.close()
            return stringToEncode
    except FileNotFoundError:
        msg = "O ficheiro " + filename + " não existe."


def executar(stringToEncode, searchWindowSize, previewWindowSize):
    # 8 bits por caracter(char)
    TotalSize = len(stringToEncode) * 8
    start_time = (time.time() * 1000)
    window['-CONTAINER-'].update(window['-CONTAINER-'].get() + "String Original: " + stringToEncode)
    window['-CONTAINER-'].update(
        window['-CONTAINER-'].get() + "\n‎Numero total de bits da String: {0}\n‎\n‎".format(TotalSize))
    [encodedNumbers, encodedSizes, encodedLetters] = encode_lz77(stringToEncode, searchWindowSize, previewWindowSize)
    end_time = (time.time() * 1000)

    bitsSearchWindowSize = countBits(searchWindowSize)
    bitsPreviewWindowSize = countBits(previewWindowSize)
    bitsPerToken = 8 + bitsSearchWindowSize + bitsPreviewWindowSize
    TokenLength = len(encodedNumbers) * bitsPerToken

    window['-CONTAINER-'].update(
        window['-CONTAINER-'].get() + "\nTempo de Compressão = {0} ms\n‎".format(end_time - start_time))
    window['-CONTAINER-'].update(
        window['-CONTAINER-'].get() + "\n‎Rácio de Compressão = {0}\n‎\n‎".format(float(TotalSize / TokenLength)))
    start_time = (time.time() * 1000)
    decodedString = decode_lz77(encodedNumbers, encodedSizes, encodedLetters)
    string = "".join(decodedString)
    end_time = (time.time() * 1000)
    window['-CONTAINER-'].update(
        window['-CONTAINER-'].get() + "\n‎\n‎Total de Tokens: {0}\n‎".format(len(encodedNumbers)))
    window['-CONTAINER-'].update(
        window['-CONTAINER-'].get() + "Comprimento total de Tokens: {0}\n‎".format(TokenLength))
    window['-CONTAINER-'].update(window['-CONTAINER-'].get() + "\n‎Decoded string: \n‎" + string)
    window['-CONTAINER-'].update(
        window['-CONTAINER-'].get() + "\n‎\n‎Tempo de Descompressão = {0} ms\n‎\n‎".format(end_time - start_time))


# -----------------------------------------------------------------------------------------------------------------------
#                                                       LZ77 GUI
# -----------------------------------------------------------------------------------------------------------------------
sg.theme('TealMono')
# ------ Menu Definition ------ #
menu_def = [['File', ['Open']]]

# ------ Column Definition ------ #
column1 = [[sg.Text('Column 1', background_color='#F7F3EC', justification='center', size=(10, 1))],
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]

layout = [
    [sg.Menu(menu_def, tearoff=True)],
    [sg.Text('Tamanho da Janela', font=('Arial', 12), size=(15, 1)), sg.InputText('', key='-SEARCH-', size=(10, 1))],
    [sg.Text('Tamanho do buffer', font=('Arial', 12), size=(15, 1)), sg.InputText('', key='-LOOKAHEAD-', size=(10, 1))],
    [sg.Multiline(default_text='', size=(90, 30), key='-CONTAINER-')],
    [sg.Submit('Executar'), sg.Cancel('Limpar')]
]
filename = ''
window = sg.Window('LZ77 Algorithm', layout, default_element_size=(80, 3), grab_anywhere=False)

while True:
    event, values = window.read()
    if event in (sg.Menu, 'Open'):
        filename = sg.popup_get_file('File')
    elif event in (sg.Submit, 'Executar'):
        searchWindowSize = values['-SEARCH-']
        previewWindowSize = values['-LOOKAHEAD-']
        stringToEncode = openFile(filename)
        if filename == '' or searchWindowSize == '' or searchWindowSize == '':
            window['-CONTAINER-'].update('Ficheiro não carregado!')
        else:
            window['-CONTAINER-'].update("Ficheiro carregado com sucesso!\n‎\n‎\n‎")
            executar(stringToEncode, int(searchWindowSize), int(previewWindowSize))

    elif event in (sg.Cancel(), 'Limpar'):
        window['-SEARCH-'].update('')
        window['-LOOKAHEAD-'].update('')
        window['-CONTAINER-'].update('')
        filename = ''
    elif event in (sg.WIN_CLOSED, 'Cancel'):
        break

window.close()