import ctypes
import ctypes.wintypes as wt
import struct
import sys
import os
import ctypes.wintypes

if sys.stdout is not None:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

GENERIC_READ           = 0x80000000
GENERIC_WRITE          = 0x40000000
FILE_SHARE_READ        = 0x00000001
FILE_SHARE_WRITE       = 0x00000002
OPEN_EXISTING          = 3
FILE_ATTRIBUTE_NORMAL  = 0x80
INVALID_HANDLE_VALUE   = ctypes.c_void_p(-1).value
DIGCF_PRESENT          = 0x02
DIGCF_DEVICEINTERFACE  = 0x10

IOCTL_BATTERY_QUERY_TAG         = 0x00294040
IOCTL_BATTERY_QUERY_INFORMATION = 0x00294044

BATTERY_INFORMATION_LEVEL = 0

GUID_DEVCLASS_BATTERY = (
    0x72631E54, 0x78A4, 0x11D0,
    (0xBC, 0xF7, 0x00, 0xAA, 0x00, 0xB7, 0xB3, 0x2A)
)

class GUID(ctypes.Structure):
    _fields_ = [
        ("Data1", ctypes.c_ulong),
        ("Data2", ctypes.c_ushort),
        ("Data3", ctypes.c_ushort),
        ("Data4", ctypes.c_ubyte * 8),
    ]

class SP_DEVICE_INTERFACE_DATA(ctypes.Structure):
    _fields_ = [
        ("cbSize",              ctypes.c_ulong),
        ("InterfaceClassGuid",  GUID),
        ("Flags",               ctypes.c_ulong),
        ("Reserved",            ctypes.POINTER(ctypes.c_ulong)),
    ]

class SP_DEVICE_INTERFACE_DETAIL_DATA(ctypes.Structure):
    _fields_ = [
        ("cbSize",     ctypes.c_ulong),
        ("DevicePath", ctypes.c_wchar * 260),
    ]

class BATTERY_QUERY_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BatteryTag",        ctypes.c_ulong),
        ("InformationLevel",  ctypes.c_int),
        ("AtRate",            ctypes.c_long),
    ]

class BATTERY_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("Capabilities",        ctypes.c_ulong),
        ("Technology",          ctypes.c_ubyte),
        ("Reserved",            ctypes.c_ubyte * 3),
        ("Chemistry",           ctypes.c_char * 4),
        ("DesignedCapacity",    ctypes.c_ulong),
        ("FullChargedCapacity", ctypes.c_ulong),
        ("DefaultAlert1",       ctypes.c_ulong),
        ("DefaultAlert2",       ctypes.c_ulong),
        ("CriticalBias",        ctypes.c_ulong),
        ("CycleCount",          ctypes.c_ulong),
    ]

setupapi  = ctypes.WinDLL("setupapi", use_last_error=True)
kernel32  = ctypes.WinDLL("kernel32", use_last_error=True)

SetupDiGetClassDevsW = setupapi.SetupDiGetClassDevsW
SetupDiGetClassDevsW.argtypes = [
    ctypes.POINTER(GUID), ctypes.c_wchar_p,
    wt.HWND, ctypes.c_ulong,
]
SetupDiGetClassDevsW.restype = ctypes.c_void_p

SetupDiEnumDeviceInterfaces = setupapi.SetupDiEnumDeviceInterfaces
SetupDiEnumDeviceInterfaces.argtypes = [
    ctypes.c_void_p, ctypes.c_void_p,
    ctypes.POINTER(GUID), ctypes.c_ulong,
    ctypes.POINTER(SP_DEVICE_INTERFACE_DATA),
]
SetupDiEnumDeviceInterfaces.restype = ctypes.c_bool

SetupDiGetDeviceInterfaceDetailW = setupapi.SetupDiGetDeviceInterfaceDetailW
SetupDiGetDeviceInterfaceDetailW.argtypes = [
    ctypes.c_void_p, ctypes.POINTER(SP_DEVICE_INTERFACE_DATA),
    ctypes.POINTER(SP_DEVICE_INTERFACE_DETAIL_DATA),
    ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong), ctypes.c_void_p,
]
SetupDiGetDeviceInterfaceDetailW.restype = ctypes.c_bool

SetupDiDestroyDeviceInfoList = setupapi.SetupDiDestroyDeviceInfoList
SetupDiDestroyDeviceInfoList.argtypes = [ctypes.c_void_p]
SetupDiDestroyDeviceInfoList.restype = ctypes.c_bool

CreateFileW = kernel32.CreateFileW
CreateFileW.argtypes = [
    ctypes.c_wchar_p, ctypes.c_ulong, ctypes.c_ulong,
    ctypes.c_void_p, ctypes.c_ulong, ctypes.c_ulong, ctypes.c_void_p,
]
CreateFileW.restype = ctypes.c_void_p

DeviceIoControl = kernel32.DeviceIoControl
DeviceIoControl.argtypes = [
    ctypes.c_void_p, ctypes.c_ulong,
    ctypes.c_void_p, ctypes.c_ulong,
    ctypes.c_void_p, ctypes.c_ulong,
    ctypes.POINTER(ctypes.c_ulong), ctypes.c_void_p,
]
DeviceIoControl.restype = ctypes.c_bool

CloseHandle = kernel32.CloseHandle
CloseHandle.argtypes = [ctypes.c_void_p]
CloseHandle.restype = ctypes.c_bool

STD_OUTPUT_HANDLE               = -11
ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

def enable_ansi():
    handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    mode = ctypes.c_ulong()
    kernel32.GetConsoleMode(handle, ctypes.byref(mode))
    kernel32.SetConsoleMode(handle, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)

def set_console_title(title):
    kernel32.SetConsoleTitleW(title)


RST   = "\033[0m"
BOLD  = "\033[1m"
DIM   = "\033[2m"
CYAN  = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED   = "\033[91m"
MAG   = "\033[95m"
WHITE = "\033[97m"
GRAY  = "\033[90m"

def make_guid():
    g = GUID()
    g.Data1 = GUID_DEVCLASS_BATTERY[0]
    g.Data2 = GUID_DEVCLASS_BATTERY[1]
    g.Data3 = GUID_DEVCLASS_BATTERY[2]
    for i, b in enumerate(GUID_DEVCLASS_BATTERY[3]):
        g.Data4[i] = b
    return g

def query_battery():
    guid = make_guid()

    hdev = SetupDiGetClassDevsW(
        ctypes.byref(guid), None, None,
        DIGCF_PRESENT | DIGCF_DEVICEINTERFACE,
    )
    if hdev == INVALID_HANDLE_VALUE:
        return None

    try:
        did = SP_DEVICE_INTERFACE_DATA()
        did.cbSize = ctypes.sizeof(SP_DEVICE_INTERFACE_DATA)

        if not SetupDiEnumDeviceInterfaces(hdev, None, ctypes.byref(guid), 0, ctypes.byref(did)):
            return None

        detail = SP_DEVICE_INTERFACE_DETAIL_DATA()
        detail.cbSize = 8 if ctypes.sizeof(ctypes.c_void_p) == 8 else 6

        required_size = ctypes.c_ulong(0)
        SetupDiGetDeviceInterfaceDetailW(
            hdev, ctypes.byref(did), ctypes.byref(detail),
            ctypes.sizeof(detail), ctypes.byref(required_size), None,
        )

        hbat = CreateFileW(
            detail.DevicePath,
            GENERIC_READ | GENERIC_WRITE,
            FILE_SHARE_READ | FILE_SHARE_WRITE,
            None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None,
        )
        if hbat == INVALID_HANDLE_VALUE:
            return None

        try:
            wait_timeout = ctypes.c_ulong(0)
            tag = ctypes.c_ulong(0)
            bytes_returned = ctypes.c_ulong(0)

            if not DeviceIoControl(
                hbat, IOCTL_BATTERY_QUERY_TAG,
                ctypes.byref(wait_timeout), ctypes.sizeof(wait_timeout),
                ctypes.byref(tag), ctypes.sizeof(tag),
                ctypes.byref(bytes_returned), None,
            ):
                return None

            bqi = BATTERY_QUERY_INFORMATION()
            bqi.BatteryTag = tag.value
            bqi.InformationLevel = BATTERY_INFORMATION_LEVEL
            bqi.AtRate = 0

            bi = BATTERY_INFORMATION()
            bytes_returned = ctypes.c_ulong(0)

            if not DeviceIoControl(
                hbat, IOCTL_BATTERY_QUERY_INFORMATION,
                ctypes.byref(bqi), ctypes.sizeof(bqi),
                ctypes.byref(bi), ctypes.sizeof(bi),
                ctypes.byref(bytes_returned), None,
            ):
                return None

            return {
                "designed":     bi.DesignedCapacity,
                "full_charged": bi.FullChargedCapacity,
                "cycle_count":  bi.CycleCount,
                "chemistry":    bi.Chemistry.decode("ascii", errors="replace").strip("\x00"),
            }
        finally:
            CloseHandle(hbat)
    finally:
        SetupDiDestroyDeviceInfoList(hdev)

def get_health_label(pct):
    if pct >= 90: return ("Excellent", GREEN)
    if pct >= 75: return ("Good",      CYAN)
    if pct >= 50: return ("Fair",      YELLOW)
    if pct >= 25: return ("Poor",      RED)
    return                ("Critical", RED)

def get_health_bar(pct, width=20):
    filled = round(pct / 100 * width)
    filled = max(0, min(width, filled))
    empty  = width - filled

    if pct >= 75:   bar_color = GREEN
    elif pct >= 50: bar_color = YELLOW
    else:           bar_color = RED

    return f"{bar_color}{chr(0x2588) * filled}{GRAY}{chr(0x2591) * empty}{RST}"

import re

def measure(text):
    return len(re.sub(r'\033\[[0-9;]*m', '', text))

SEPARATOR = object()

def render_box(items):
    content_lines = [item for item in items if item is not SEPARATOR]
    max_w = max(measure(text) for text, _ in content_lines) if content_lines else 20

    top = f"{CYAN}{chr(0x2554)}{chr(0x2550) * (max_w + 2)}{chr(0x2557)}{RST}"
    sep = f"{CYAN}{chr(0x2560)}{chr(0x2550) * (max_w + 2)}{chr(0x2563)}{RST}"
    bot = f"{CYAN}{chr(0x255A)}{chr(0x2550) * (max_w + 2)}{chr(0x255D)}{RST}"

    print()
    print(top)
    for item in items:
        if item is SEPARATOR:
            print(sep)
        else:
            text, centered = item
            vis = measure(text)
            pad_total = max_w - vis
            if centered:
                left = pad_total // 2
                right = pad_total - left
                print(f"{CYAN}{chr(0x2551)}{RST} {' ' * left}{text}{' ' * right} {CYAN}{chr(0x2551)}{RST}")
            else:
                print(f"{CYAN}{chr(0x2551)}{RST} {text}{' ' * pad_total} {CYAN}{chr(0x2551)}{RST}")
    print(bot)
    print()

def display(data):
    pct = (data["full_charged"] / data["designed"]) * 100 if data["designed"] > 0 else 0
    label, color = get_health_label(pct)
    bar = get_health_bar(pct)

    items = [
        (f"{BOLD}{WHITE}BatHealth  v1.0{RST}", True),
        (f"{DIM}Windows Battery Health Check{RST}", True),
        SEPARATOR,
        ("", False),
        (f"  {BOLD}{WHITE}Battery Health{RST}    {BOLD}{color}{pct:>7.2f}%{RST}  {color}{label}{RST}", False),
        ("", False),
        (f"  {bar}", False),
        ("", False),
        SEPARATOR,
        ("", False),
        (f"  {DIM}Full Capacity  {RST} {WHITE}{BOLD}{data['full_charged']:>8,} mWh{RST}", False),
        (f"  {DIM}Design Capacity{RST} {WHITE}{BOLD}{data['designed']:>8,} mWh{RST}", False),
    ]

    if data["cycle_count"] > 0:
        items.append((f"  {DIM}Cycle Count    {RST} {WHITE}{BOLD}{data['cycle_count']:>8,}{RST}", False))

    if data["chemistry"]:
        items.append((f"  {DIM}Chemistry      {RST} {WHITE}{BOLD}{data['chemistry']:>8}{RST}", False))

    items.append(("", False))
    render_box(items)

def display_no_battery():
    items = [
        (f"{BOLD}{WHITE}BatHealth  v1.0{RST}", True),
        (f"{DIM}Windows Battery Health Check{RST}", True),
        SEPARATOR,
        ("", False),
        (f"  {YELLOW}No battery detected on this device.{RST}", False),
        ("", False),
        (f"  {DIM}This tool requires a laptop or tablet{RST}", False),
        (f"  {DIM}with a built-in battery to function.{RST}", False),
        ("", False),
    ]
    render_box(items)

def main():
    enable_ansi()
    set_console_title("BatHealth - Battery Health Check")

    try:
        os.system("")
    except Exception:
        pass

    data = query_battery()

    if data is None:
        display_no_battery()
    else:
        display(data)

    print(f"  {DIM}Press any key to exit...{RST}")

    try:
        import msvcrt
        msvcrt.getch()
    except Exception:
        input()

if __name__ == "__main__":
    main()
