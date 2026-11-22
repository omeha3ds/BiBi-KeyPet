# Вебсимулятор прошивки Піпа (`localhost:8466`)

Симулятор компілює **той самий C-код екранів прошивки** (`ui/*.c` + `LVGL`) у WebAssembly (`sim/web/pip.js` та `sim/web/pip.wasm`), тож на комп'ютері можна перевіряти меню, бейдж, QR, теми й шрифти без фізичної плати.

Зібрані файли (`sim/web/pip.js`, `sim/web/pip.wasm` і `build-web/`) навмисно додані в `.gitignore` і не зберігаються в Git.

## 1. Одноразове встановлення Emscripten (на диск D, без змін глобального PATH)

```powershell
git clone --depth 1 https://github.com/emscripten-core/emsdk.git D:\emsdk
cmd /c "cd /d D:\emsdk && emsdk.bat install latest && emsdk.bat activate latest"
```

Потрібний також `cmake` (підхоплюється автоматично з уже встановленого ESP-IDF 5.5.6 у `C:\Espressif\tools`) та бібліотека `LVGL` (підхоплюється автоматично з `firmware/managed_components/lvgl__lvgl` або `third_party/lvgl`).

## 2. Збірка симулятора

З кореня репозиторію виконай:

```powershell
.\sim\build-web.ps1
```

Скрипт сам підключає `D:\emsdk` лише на час збірки (глобальні змінні Windows не змінюються) і створює `sim/web/pip.js` та `sim/web/pip.wasm`.

## 3. Запуск у браузері

```powershell
python sim/serve.py
```

Після цього відкрий у браузері: **http://localhost:8466**

### Корисні параметри в адресному рядку (для швидкого перегляду екранів)
- `?screen=menu` — головне меню (також `badge`, `qr`, `style`, `updating`, `pip`)
- `?theme=4` — палітра Pixel (`4` Півонія, `5` Обсидіан, `6` Затока, `7` Шавлія, `8` Корал, `9` Порцеляна)
- `?name=Максим|Коваленко|KeyPet` — тестовий бейдж
- `?qr=Telegram|@pip_keypet|https://t.me/pip_keypet` — тестовий QR-код (параметр можна повторювати до 4 разів)
