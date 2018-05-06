# Contributing to Turing

## Code

just make good code

follow pep8 and everything will be good

## Translation

Translators must use Qt Linguist. It can be obtained by installing the Qt toolkit.

### Editing an existing language

Just open the .ts file in Linguist and change what needs to be changed.

### Adding a new language

First, create a new .ts file in /src/lang/ using the following template:

    <?xml version="1.0" encoding="utf-8"?>
    <!DOCTYPE TS><TS version="2.0" language="LANGUAGE CODE" sourcelanguage="en">
    <context>
    </context>
    </TS>

Replace `LANGUAGE CODE` by the ISO code of the language. If the language is "generic", use the short code (example: French `fr`, German `de`, Spanish `es`), but if it's not, use the full code (example: Simplified Chinese `zh-Hans`, Traditional Chinese `zh-Hant`).

Then, download the [FatCow Hosting Icons pack](http://www.fatcow.com/free-icons), find the corresponding flag in the 16x16 folder. Rename it to the language code you used for the .ts file (example: fr.png, de.png, zh-Hans.png) and put that in the /src/media/lang/ folder. 

Open a command prompt in /src/ and run tools/compile-gui (make sure that the CWD is /src/). 

Then, open /src/turing.qrc in Qt Creator and add /src/lang/LANGUAGE.qm and /src/media/lang/LANGUAGE.png under the /lang prefix. Save, and use /src/run to test and make sure everything works.