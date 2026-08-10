import ctypes
from ctypes import wintypes

_MUTEX_NAME = "ShutdownTimer_SingleInstance_Mutex_v1"
_ERROR_ALREADY_EXISTS = 183

_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
_kernel32.CreateMutexW.restype = wintypes.HANDLE
_kernel32.CreateMutexW.argtypes = (wintypes.LPCVOID, wintypes.BOOL, wintypes.LPCWSTR)

# Kept alive for the process lifetime; Windows releases it automatically
# on exit (clean or crashed), so no explicit close is needed.
_mutex_handle = None


def acquire_single_instance_lock():
    global _mutex_handle
    _mutex_handle = _kernel32.CreateMutexW(None, False, _MUTEX_NAME)
    return ctypes.get_last_error() != _ERROR_ALREADY_EXISTS
