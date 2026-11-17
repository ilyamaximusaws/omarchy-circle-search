# Omarchy Circle Search

Circle to Search для Omarchy: «замороженный» кадр, автоматические области и окна, Live Text через Tesseract, выделение прямоугольником или произвольным контуром, копирование, сохранение, поиск, перевод, Google Lens и редактирование в Omasnap.

Это нативный Omarchy overlay-плагин, а не отдельный процесс Quickshell. Исходная функциональность перенесена из [angelOS](https://github.com/MixaDoDs/AngelOS-Dotfiles) (MixaDoDs, MIT). Зафиксированный upstream-коммит указан в `vendor/UPSTREAM_COMMIT`.

## Возможности

- Auto: щелчок выбирает строку текста или найденную область; контур выделяет произвольную форму.
- Rect: прямоугольник с изменяемыми сторонами и углами; Shift+drag временно включает этот режим.
- Text: слово или диапазон слов по OCR; Ctrl+щелчок по распознанной ссылке открывает её.
- Copy/Save для изображения и текста, Ctrl+C / Enter и Ctrl+S.
- Поиск текста в Google и изображения в Google Lens через браузер.
- Кнопка Edit сохраняет выделение и открывает его через `omasnap --file <path>`.
- Esc отменяет текущий шаг, затем закрывает overlay.
- Геометрия окон и активного выхода берётся из `Quickshell.Hyprland`; координаты переводятся в пиксели захваченного кадра с учётом масштаба выхода.

Собственный редактор angelOS и его встроенный QtWebEngine Lens специально не переносились: в Omarchy уже есть Omasnap, а Lens работает через локальную HTML-форму и обычный браузер.

## Зависимости

Основные пакеты Arch/Omarchy:

```sh
omarchy pkg add quickshell grim omasnap tesseract python-numpy python-pillow python-cairo wl-clipboard xdg-utils
```

Дополнительно для перевода и русского OCR:

```sh
omarchy pkg add translate-shell tesseract-data-rus
```

`translate-shell` требуется только кнопке перевода. Если `tesseract-data-rus` не установлен, базовый OCR всё равно работает с доступными языками Tesseract, но качество русского распознавания будет ниже. Для Google/Lens и перевода нужен интернет.

## Установка

Из Git-репозитория:

```sh
omarchy plugin add https://github.com/ilyamaximusaws/omarchy-circle-search.git --enable --yes
omarchy restart shell
```

Для локальной разработки:

```sh
git clone https://github.com/ilyamaximusaws/omarchy-circle-search.git ~/.config/omarchy/plugins/angelos.circle-search
omarchy plugin enable angelos.circle-search
omarchy restart shell
```

После изменения QML/JS нужен `omarchy restart shell`: `rescanPlugins` обновляет реестр, но не заменяет уже загруженный QML-код.

Запуск:

```sh
omarchy-shell shell summon angelos.circle-search '{}'
```

Замена штатного Screenshot в `~/.config/hypr/bindings.lua`:

```lua
o.rebind("SUPER + SHIFT + S", "Circle Search", "omarchy-shell shell summon angelos.circle-search '{}'")
```

`SUPER + SHIFT + S` раньше запускал `omarchy-capture-screenshot`; теперь эта клавиша открывает Circle Search. Capture menu, Share и запись экрана не меняются.

## Структура

- `CircleSearchOverlay.qml` — контракт Omarchy `open(payload)` / `close()` / `opened`.
- `lib/services/CircleSearch.qml` — состояние, захват, OCR, выделение и действия.
- `lib/modules/CircleCanvas.qml`, `CircleOverlay.qml` — layer-shell overlay и взаимодействие.
- `lib/services/Niri.qml` — сохранённое upstream-имя адаптера; внутри используется Hyprland, не niri.
- `lib/services/Capture.qml`, `scripts/save_shot.py` — сохранение/clipboard/уведомления.
- `scripts/circle.py` — Tesseract OCR и translate-shell.
- `scripts/capture_regions.py` — поиск областей и фильтрация окон.
- `scripts/lens_page.py` — локальная форма загрузки изображения в Google Lens.
- `lib/config/Theme.qml` — адаптер к `qs.Commons.Color`.
- `vendor/angelos/` — неизменённые исходники нужных upstream-файлов.
- `tools/port_upstream.py` — воспроизводимая генерация перенесённых QML/JS из vendor.

Не редактируйте генерируемые файлы вручную. Меняйте правила в `tools/port_upstream.py`, затем выполняйте:

```sh
python3 tools/port_upstream.py
python3 tools/port_upstream.py --check
```

## Тесты

Быстрый набор без изменения живого рабочего стола:

```sh
tests/run.sh
```

Дополнительно `python3 tests/test_hyprland.py` кратко открывает и закрывает установленный overlay, проверяет свежий запуск в логе Omarchy, имя выхода, число окон и реальный `grim`-кадр. Полный набор с этой проверкой:

```sh
tests/run.sh --live
```

Покрываются структурный контракт и воспроизводимость генерации, сохранение PNG/JPEG и clipboard, локальная Lens-форма, OCR learning (34 проверки), QML smoke с реальным crop и вызовом Omasnap, а также live Hyprland/grim.

`tests/test_ocr.py` — отдельный вендоренный diagnostic-набор upstream. На установленной версии Tesseract его случайный no-junk тест иногда находит ложное слово; тот же результат воспроизводится на неизменённом upstream-коммите. Это не регрессия порта и не входит в `tests/run.sh`.

## Удаление

```sh
omarchy plugin disable angelos.circle-search
rm -rf ~/.config/omarchy/plugins/angelos.circle-search
omarchy restart shell
```

Удалите добавленный `o.bind(...)` из `~/.config/hypr/bindings.lua`, если он больше не нужен.

## Лицензия

MIT. Copyright исходного angelOS сохранены в `LICENSE`; upstream-исходники лежат в `vendor/angelos/`.
