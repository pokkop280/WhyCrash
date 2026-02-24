import sys
import traceback
import os
import re

def debug():
    """Эту функцию нужно вызвать в начале кода: WhyCrash.debug() (ГЛОБАЛЬНЫЙ ПЕРЕХВАТ)"""
    start_debug()

def start_debug():
    """Включает AI-анализ ошибок для всего последующего кода"""
    if not hasattr(sys, 'ps1'):
        sys.excepthook = _ai_excepthook

def end_debug():
    """Выключает AI-анализ ошибок (возвращает стандартное поведение Python)"""
    if sys.excepthook == _ai_excepthook:
        sys.excepthook = sys.__excepthook__

import contextlib
import functools

@contextlib.contextmanager
def catch_block():
    """Контекстный менеджер для перехвата ошибок только в определенном блоке кода"""
    try:
        yield
    except Exception:
        _ai_excepthook(*sys.exc_info())
        sys.exit(1)

def catch_errors(func):
    """Декоратор для перехвата ошибок только в конкретной функции"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            _ai_excepthook(*sys.exc_info())
            sys.exit(1)
    return wrapper

def _ai_excepthook(exc_type, exc_value, exc_traceback):
    try:
        import requests
        import json
    except ImportError:
        print("Для работы WhyCrash необходимо установить пакет 'requests': pip install requests")
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    try:
        from rich.console import Console
        from rich.markdown import Markdown
        from rich.panel import Panel
        RICH = True
        console = Console()
    except ImportError:
        RICH = False

    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

    if RICH:
        console.print(Panel("Oops! Произошла ошибка. WhyCrash собирает контекст и анализирует проблему...", border_style="bold red", expand=False))
    else:
        print(f"\n{RED}Oops! Произошла ошибка. WhyCrash собирает контекст и анализирует проблему...{RESET}\n")

    tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    tb_text = "".join(tb_lines)

    local_files = {}
    deepest_file = None
    deepest_line = 0

    tb = exc_traceback
    while tb:
        filename = tb.tb_frame.f_code.co_filename
        lineno = tb.tb_lineno
        deepest_file = filename
        deepest_line = lineno
        
        if isinstance(filename, str) and os.path.exists(filename):
            if 'site-packages' not in filename and 'lib\\python' not in filename.lower() and 'lib/python' not in filename.lower():
                if filename not in local_files:
                    try:
                        with open(filename, 'r', encoding='utf-8') as f:
                            local_files[filename] = f.read()
                    except Exception:
                        pass
        tb = tb.tb_next

    context_str = ""
    for fpath, code in local_files.items():
        context_str += f"### Файл: {fpath} ###\n```python\n{code}\n```\n\n"

    first_prompt = f"""Произошла ошибка в Python приложении.
Исключение вызвано в файле '{deepest_file}' на строке {deepest_line}.

Traceback:
{tb_text}

Исходный код контекстных файлов (только те, что относятся к проекту):
{context_str}

Пожалуйста, проанализируй эту ошибку и детально объясни на русском языке, почему она произошла.
Пока что НЕ пиши исправленный код, только проанализируй и объясни причину проблемы."""

    API_KEY = "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"

    # ========= ПЕРВЫЙ ЗАПРОС К OPENROUTER =========
    messages = [{"role": "user", "content": first_prompt}]

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "minimax/minimax-m2.5",
                "messages": messages,
                "reasoning": {"enabled": True}
            })
        )
        response.raise_for_status()
        resp_json = response.json()
        assistant_message = resp_json['choices'][0]['message']
        
        reasoning = assistant_message.get('reasoning_details') or ""
        content = assistant_message.get('content') or ""

        if RICH:
            if reasoning:
                console.print(Panel(Markdown(f"**Мысли (Reasoning):**\n\n{reasoning}"), title="AI Обдумывает", border_style="cyan"))
            console.print(Panel(Markdown(content), title="Анализ ошибки", border_style="yellow"))
        else:
            print(f"{CYAN}============== Знания и Анализ (Minimax) =============={RESET}\n")
            if reasoning:
                print(f"{CYAN}--- Размышления ---{RESET}\n{reasoning}\n")
            print(f"{YELLOW}--- Объяснение ---{RESET}\n{content}\n")
            print(f"{CYAN}======================================================={RESET}\n")

        # Просим у пользователя подтверждение
        try:
            import questionary
            answer = questionary.select(
                "Хотите, чтобы WhyCrash исправил эту ошибку?",
                choices=["Да", "Нет"]
            ).ask()
            if answer != "Да":
                print(f"{YELLOW}Отменено. Выходим...{RESET}")
                sys.exit(1)
        except ImportError:
            answer = input(f"{GREEN}Хотите, чтобы WhyCrash исправил эту ошибку? (y/n, enter=yes): {RESET}")
            if answer.strip().lower() not in ('', 'y', 'yes', 'да', 'д'):
                print(f"{YELLOW}Отменено. Выходим...{RESET}")
                sys.exit(1)

        # ========= ВТОРОЙ ЗАПРОС К OPENROUTER (ПРОДОЛЖАЕМ РАЗМЫШЛЕНИЯ) =========
        if RICH:
            console.print(f"[bold green]Генерируем исправление...[/bold green]")
        else:
            print(f"\n{GREEN}Генерируем исправление...{RESET}")

        messages.append({
            "role": "assistant",
            "content": content,
            "reasoning_details": reasoning
        })
        
        second_prompt = """Напиши ПОЛНЫЙ исправленный код для файла, в котором нужно сделать изменения.
ВАЖНО: Выведи исправленный код внутри одного блока ```python ... ```.
Непосредственно перед блоком кода напиши пустой комментарий или строку, указывающую какой файл ты исправляешь, в таком точном формате:
FILE_TO_FIX: <полный_путь_к_файлу>
Выводи весь файл целиком, чтобы я мог полностью заменить старый файл."""
        
        messages.append({"role": "user", "content": second_prompt})

        response2 = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "minimax/minimax-m2.5",
                "messages": messages,
                "reasoning": {"enabled": True}
            })
        )
        response2.raise_for_status()
        resp_json2 = response2.json()
        assistant_message2 = resp_json2['choices'][0]['message']
        
        content2 = assistant_message2.get('content') or ""

        # Парсим ответ
        file_to_fix = deepest_file
        match_file = re.search(r"FILE_TO_FIX:\s*(.*)", content2)
        if match_file:
            file_to_fix = match_file.group(1).strip()

        parts = content2.split("```python")
        if len(parts) > 1:
            last_block = parts[-1].split("```")[0]
            fixed_code = last_block.strip()

            if os.path.exists(file_to_fix):
                try:
                    with open(file_to_fix, 'w', encoding='utf-8') as f:
                        f.write(fixed_code + '\n')
                    if RICH:
                        console.print(f"[bold green][+] Файл '{file_to_fix}' успешно исправлен! Запустите скрипт заново.[/bold green]")
                    else:
                        print(f"{GREEN}\n[+] Файл '{file_to_fix}' успешно исправлен! Запустите скрипт заново.{RESET}")
                except Exception as e:
                    if RICH:
                        console.print(f"[bold red][-] Не удалось записать файл: {e}[/bold red]")
                    else:
                        print(f"{RED}\n[-] Не удалось записать файл: {e}{RESET}")
            else:
                if RICH:
                    console.print(f"[bold red]Не найден файл для исправления: {file_to_fix}[/bold red]")
                else:
                    print(f"\n{RED}Не найден файл для исправления: {file_to_fix}{RESET}")
        else:
            if RICH:
                console.print(f"[bold yellow]Код для исправления не найден в ответе.[/bold yellow]")
            else:
                print(f"\n{YELLOW}Код для исправления не найден в ответе.{RESET}")

    except Exception as e:
        if RICH:
            console.print(f"[bold red]ОШИБКА WhyCrash API: {e}[/bold red]")
        else:
            print(f"{RED}ОШИБКА WhyCrash API: {e}{RESET}")
        print("\nОригинальный Traceback:")
        print(tb_text)
