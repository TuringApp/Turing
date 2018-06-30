# Contributing to Turing

## Code

This is Python, thus following the PEP #8 is appreciated.

We do have general rules simply for the purpose of keeping everything consistent:
- `snake_case` for variables and functions
- `PascalCase` for classes
- **mandatory** UTF-8 header (`# -*- coding: utf-8 -*-`) at the beginning of all .py files 

We recommend putting 1 line between code "blocks" and 2 lines between functions, like this:

```python
def abc():
	b = 2

	return b * 3


def def():
	a = 5

	if a == 6:
		return 123

	return abc()
```

## Translation

Translators must use Qt Linguist. It can be obtained by installing the Qt toolkit.

### Editing an existing language

Just open the `.ts` file in Linguist and change what needs to be changed. If possible, run the program afterwards using `/src/run` to make sure everything is recompiled correctly. If you get errors saying that `lrelease` was not found or similar problems, write it in your pull request or commit ("need recompilation").

**Under no circumstances** shall you recompile the files manually (by calling `pylupdate5` and `lrelease` directly), you **must** call `tools/compile-gui`. This is due to an evil bug in PyQt's `pylupdate5` related to the handling of UTF-8 characters. The only workaround we found is to add `encoding="UTF-8"` to all XML tags in the `.ts` file before calling `pylupdate5`. For some reason it removes that attribute afterwards (so if you call it twice on the same `.ts` file, it will corrupt it the second time you run it. funny, isn't it?). This attribute insertion is done by `progen.py`, which is called by `compile-gui`.

Again, you **must** call `tools/compile-gui` while being in the `/src/` directory.

### Adding a new language

First, create a new .ts file in /src/lang/ using the following template:

    <?xml version="1.0" encoding="utf-8"?>
    <!DOCTYPE TS><TS version="2.0" language="LANGUAGE CODE" sourcelanguage="en">
    <context>
    </context>
    </TS>

Replace `LANGUAGE CODE` by the ISO code of the language. If the language is "generic", use the short code (example: French `fr`, German `de`, Spanish `es`), but if it's not, use the full code (example: Simplified Chinese `zh-Hans`, Traditional Chinese `zh-Hant`).

Then, download the [FatCow Hosting Icons pack](http://www.fatcow.com/free-icons), find the corresponding flag in the 16x16 folder. Rename it to the language code you used for the `.ts` file (example: fr.png, de.png, zh-Hans.png) and put that in the `/src/media/lang/` folder. 

Open a command prompt in `/src/` and run `tools/compile-gui` (make sure that the CWD is `/src/`). 

Then, open `/src/turing.qrc` in Qt Creator and add `/src/lang/LANGUAGE.qm` and `/src/media/lang/LANGUAGE.png` under the `/lang` prefix. Save, and use `/src/run` to test and make sure everything works.