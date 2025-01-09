### **Python Starter Project Guide**

ეს სახელმძღვანელო გთავაზობთ **VS Code-ის ოპტიმიზებულ კონფიგურაციას** Python პროექტისთვის. იგი მოიცავს `settings.json`, `launch.json`, და `tasks.json` ფაილების რეკომენდირებულ პარამეტრებს, რაც უზრუნველყოფს თქვენი სამუშაო გარემოს მაქსიმალურ პროდუქტიულობას.

---

## **1. `settings.json`**

**`settings.json`** განსაზღვრავს თქვენი პროექტის ძირითადი პარამეტრები, როგორიცაა ინტერპრეტატორი, ფორმატირება, ლინტინგი და ტესტირება.

```json
{
    "python.pythonPath": "./.venv/bin/python",
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.fixAll": true
    },
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.mypyEnabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.mypyArgs": [
        "--ignore-missing-imports"
    ],
    "python.linting.pylintArgs": [
        "--disable=C0114,C0115,C0116",
        "--max-line-length=88"
    ],
    "python.linting.flake8Args": [
        "--max-line-length=88"
    ],
    "python.testing.pytestEnabled": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    },
    "python.analysis.extraPaths": [
        "./src",
        "./lib"
    ],
    "python.analysis.typeCheckingMode": "off",
    "python.terminal.activateEnvironment": true,
    "python.formatting.blackArgs": [
        "--line-length=88"
    ]
}
```

### **პარამეტრების ახსნა**
- **Linting:** ჩართულია Flake8, MyPy და Pylint.
- **Formatting:** Black ავტომატურად ფორმატირებს კოდს შენახვისას.
- **Testing:** Pytest ჩართულია VS Code-ის ტესტირების გარემოში.
- **Ignored Files:** `__pycache__` და `.pyc` ფაილები არ გამოჩნდება.

---

## **2. `launch.json`**

**`launch.json`** მართავს დებაგინგის პროცესს.

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "ENV_VAR_NAME": "value"
            },
            "args": [],
            "justMyCode": true
        },
        {
            "name": "Run Pytest",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["-v"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

### **პარამეტრების ახსნა**
- **Python: Current File:** დებაგინგის რეჟიმში უშვებს ამჟამად გახსნილ ფაილს.
- **Run Pytest:** უშვებს pytest ტესტებს დეტალური ლოგირებით.

---

## **3. `tasks.json`**

**`tasks.json`** განსაზღვრავს კონკრეტულ ამოცანებს (tasks), რომლებიც უნდა შესრულდეს ტერმინალში.

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run Pytest",
            "type": "shell",
            "command": "pytest",
            "args": [
                "-v",
                "--maxfail=3"
            ],
            "group": {
                "kind": "test",
                "isDefault": true
            },
            "presentation": {
                "reveal": "always",
                "panel": "shared"
            }
        },
        {
            "label": "Run Single Test File",
            "type": "shell",
            "command": "pytest",
            "args": [
                "${file}"
            ],
            "group": {
                "kind": "test",
                "isDefault": false
            },
            "presentation": {
                "reveal": "always",
                "panel": "shared"
            }
        }
    ]
}
```

### **პარამეტრების ახსნა**
- **Run Pytest:** უშვებს ყველა ტესტს, გაჩერდება პირველ 3 ჩავარდნის შემდეგ.
- **Run Single Test File:** უშვებს ამჟამად გახსნილ ტესტ ფაილს.

---

## **4. გარემოს ცვლადების მართვა**
თუ საჭიროა კონკრეტული გარემოს ცვლადები, დაამატეთ ისინი `env` ველში `launch.json`-სა და `tasks.json`-ში:
```json
"env": {
    "API_KEY": "your_api_key",
    "DEBUG_MODE": "true"
}
```

---

## **5. რეკომენდირებული `.gitignore`**
Git რეპოზიტორში არასაჭირო ფაილების შესანახად გამოიყენეთ `.gitignore`:
```
.venv/
__pycache__/
*.pyc
.vscode/
```

---

## **შეჯამება**
ეს სახელმძღვანელო უზრუნველყოფს:
- **სტაბილურ სამუშაო გარემოს.**
- **ინტეგრირებულ დებაგინგსა და ტესტირებას.**
- **კოდის სტილისტიკურ და ტიპის შემოწმებას.**

თუ რაიმე დამატებითი კონფიგურაცია გჭირდებათ, შეგიძლიათ დაამატოთ ამ ფაილებში. ისარგებლებთ ამ პროექტის სტრუქტურით, რათა სწრაფად დაიწყოთ Python-ის განვითარება.

---
