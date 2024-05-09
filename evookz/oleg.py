import ctypes
import time

# Constantes para mensagens de teclado
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
F10 = 0x79

# Função para enviar mensagem de teclado
def send_message_keyboard(hwnd, key_code):
    ctypes.windll.user32.SendMessageW(hwnd, WM_KEYDOWN, key_code, 0)
    time.sleep(0.2)
    ctypes.windll.user32.SendMessageW(hwnd, WM_KEYUP, key_code, 0)

# Encontrar a janela do Tibia
hwnd = ctypes.windll.user32.FindWindowW(0, 'Tibia - Oleg Winchester')
if hwnd == 0:
    print("Janela do Tibia não encontrada.")
    exit()

# Endereços de memória
addresses = [
    0x0B44DC50,
    0x14367C64,
    0x196DE754,
    0x45712C00,
    0x4589B158
]

# Função para ler a memória
def read_memory(address):
    process = ctypes.windll.kernel32.OpenProcess(0x0010, False, ctypes.windll.kernel32.GetCurrentProcessId())
    if not process:
        print("Erro ao abrir o processo.")
        return None

    buffer = ctypes.c_ulong()
    ctypes.windll.kernel32.ReadProcessMemory(process, address, ctypes.byref(buffer), ctypes.sizeof(buffer), None)
    
    ctypes.windll.kernel32.CloseHandle(process)

    return buffer.value

# Verificar os valores na memória
for address in addresses:
    value = read_memory(address)
    if value is not None and value < 700:
        print(f"O valor no endereço {hex(address)} é {value}, que é menor que 700.")
        send_message_keyboard(hwnd, F10)
