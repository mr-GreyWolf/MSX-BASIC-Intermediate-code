# MSX BASIC — Промежуточный код

Описание формата [здесь](https://sysadminmosaic.ru/msx/basic_intermediate_code/).

Для написания скриптов использовался Python 2.7

<a name="codetotextt"></a>
### code-to-text.py
Читает файл в бинарном формате и сохраняет его содержимое в текстово формате

Параметры:
1. Исходный файл в бинарном формате
2. Выходной файл текстовом формате

Пример запуска:

`./code-to-text.py file.bas file_a.bas`

## Тесты
<a name="testfiles"></a>

Заруск скрита с тестовым файлом:

`./code-to-text.py code.bas code.txt`

Сравнение файлов:

`diff code.txt code_a.bas`

<a name="codebas"></a>
### code.bas
Тестовый файл в бинарном формате, создан командой: `save "code.bas"`

<a name="codeabas"></a>
### code_a.bas
Тестовый файл в текстовом формате, создан командой: `save "code_a.bas",a`
