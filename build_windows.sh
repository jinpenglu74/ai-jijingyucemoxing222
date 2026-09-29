#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
BUILD="$ROOT/build"
CLANG="${CLANG:-/usr/local/swift/usr/bin/clang-cl}"
LINK="${LINK:-/usr/local/swift/usr/bin/lld-link}"
mkdir -p "$BUILD"
cat > "$BUILD/kernel32.def" <<'DEF'
LIBRARY KERNEL32.dll
EXPORTS
  GetModuleHandleW
  ExitProcess
  CreateDirectoryW
  GetFileAttributesW
  CreateFileW
  ReadFile
  WriteFile
  CloseHandle
  SetFilePointer
  CopyFileW
  GetLastError
  GetDriveTypeW
  GetLocalTime
  GetTickCount64
  MoveFileExW
  CreateThread
  Sleep
  GetSystemTimeAsFileTime
  MultiByteToWideChar
  WideCharToMultiByte
  LocalFree
  GetProcessHeap
  HeapAlloc
  HeapReAlloc
  HeapFree
  GlobalAlloc
  GlobalLock
  GlobalUnlock
  GlobalFree
  CreateMutexW
  WaitForSingleObject
  ReleaseMutex
DEF
cat > "$BUILD/user32.def" <<'DEF'
LIBRARY USER32.dll
EXPORTS
  RegisterClassExW
  CreateWindowExW
  DefWindowProcW
  ShowWindow
  UpdateWindow
  GetMessageW
  TranslateMessage
  DispatchMessageW
  PostQuitMessage
  LoadCursorW
  BeginPaint
  EndPaint
  GetClientRect
  GetWindowRect
  InvalidateRect
  MessageBoxW
  SetWindowTextW
  GetWindowTextW
  GetWindowTextLengthW
  DestroyWindow
  SetFocus
  MoveWindow
  SetWindowPos
  SendMessageW
  SetWindowLongPtrW
  GetWindowLongPtrW
  EnableWindow
  GetSystemMetrics
  GetDC
  ReleaseDC
  FillRect
  DrawTextW
  GetDpiForWindow
  SetProcessDPIAware
  PostMessageW
  OpenClipboard
  EmptyClipboard
  SetClipboardData
  CloseClipboard
DEF
cat > "$BUILD/gdi32.def" <<'DEF'
LIBRARY GDI32.dll
EXPORTS
  CreateSolidBrush
  CreatePen
  DeleteObject
  SelectObject
  SetTextColor
  SetBkMode
  CreateFontW
  Rectangle
  RoundRect
  MoveToEx
  LineTo
  GetStockObject
  SetDCBrushColor
  SetDCPenColor
  Ellipse
  GetTextExtentPoint32W
DEF
cat > "$BUILD/winhttp.def" <<'DEF'
LIBRARY WINHTTP.dll
EXPORTS
  WinHttpOpen
  WinHttpConnect
  WinHttpOpenRequest
  WinHttpSendRequest
  WinHttpReceiveResponse
  WinHttpQueryDataAvailable
  WinHttpReadData
  WinHttpCloseHandle
  WinHttpSetTimeouts
  WinHttpQueryHeaders
DEF
cat > "$BUILD/crypt32.def" <<'DEF'
LIBRARY CRYPT32.dll
EXPORTS
  CryptProtectData
  CryptUnprotectData
DEF
"$LINK" /dll /noentry /def:"$BUILD/kernel32.def" /implib:"$BUILD/kernel32.lib" /machine:x64
"$LINK" /dll /noentry /def:"$BUILD/user32.def" /implib:"$BUILD/user32.lib" /machine:x64
"$LINK" /dll /noentry /def:"$BUILD/gdi32.def" /implib:"$BUILD/gdi32.lib" /machine:x64
"$LINK" /dll /noentry /def:"$BUILD/winhttp.def" /implib:"$BUILD/winhttp.lib" /machine:x64
"$LINK" /dll /noentry /def:"$BUILD/crypt32.def" /implib:"$BUILD/crypt32.lib" /machine:x64
CFLAGS=(--target=x86_64-pc-windows-msvc /c /GS- /Zl /utf-8 /W3 /WX /D_CRT_SECURE_NO_WARNINGS /I"$ROOT/src")
for f in core storage network parser provider snapshot prediction_input prediction_repair grading archive review_logic review deepseek main; do
  "$CLANG" "${CFLAGS[@]}" "$ROOT/src/$f.c" /Fo:"$BUILD/$f.obj"
done
OUT="$ROOT/AI基金预测_V0.6_AI复盘基础版_免安装.exe"
"$LINK" "$BUILD/main.obj" "$BUILD/core.obj" "$BUILD/storage.obj" "$BUILD/network.obj" "$BUILD/parser.obj" "$BUILD/provider.obj" "$BUILD/snapshot.obj" "$BUILD/prediction_input.obj" "$BUILD/prediction_repair.obj" "$BUILD/grading.obj" "$BUILD/archive.obj" "$BUILD/review_logic.obj" "$BUILD/review.obj" "$BUILD/deepseek.obj" "$BUILD/kernel32.lib" "$BUILD/user32.lib" "$BUILD/gdi32.lib" "$BUILD/winhttp.lib" "$BUILD/crypt32.lib" /subsystem:windows /entry:wWinMainCRTStartup /nodefaultlib /machine:x64 /dynamicbase /nxcompat /highentropyva /out:"$OUT"
echo "Built: $OUT"
