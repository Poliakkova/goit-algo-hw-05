"""
Доробіть консольного бота помічника з попереднього домашнього завдання
та додайте обробку помилок за допомоги декораторів
"""
import colorama


colorama.init(autoreset=True)


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValueError as e:
            print(e, e.args)
            return colorama.Fore.RED + "🔴 Error! Wrong arguments. Must be: [command] [name] [phone number]"

        except KeyError as e:
            # якщо в KeyError поклали другий аргумент exists
            if len(e.args) == 2 and e.args[1] == 'exists':
                return colorama.Fore.RED + f"🔴 Error! Contact with name '{e.args[0]}' already exists"

            return colorama.Fore.RED + f"🔴 Contact with name '{e.args[0]}' not found"

        except IndexError as e:
            print(e, e.args)
            return colorama.Fore.RED + "🔴 Error! Wrong arguments. Must be: [command] [name]"

    return inner


@input_error
def main():
    print(colorama.Style.BRIGHT + colorama.Fore.LIGHTYELLOW_EX +
          "Welcome to bot-assistant 📞Phone Book📞! What can I help you with? 😊")
    print(show_help())

    contacts = {}

    while True:
        input_str = input(">> ").strip().lower()
        if input_str == '':
            continue

        command, *args = parse_input(input_str)

        if command in ('exit', 'close'):
            break
        elif command == 'hello':
            print('How can I help you?')
        elif command == 'help':
            print(show_help())
        elif command == 'add':
            print(add_contact(args, contacts))
        elif command == 'change':
            print(change_contact(args, contacts))
        elif command == 'phone':
            print(find_contact(args, contacts))
        elif command == 'all':
            print(show_all(contacts))
        else:
            print(colorama.Fore.YELLOW + "⚠️ It's not a command. Type 'help' to see available commands")

    print(colorama.Style.BRIGHT + colorama.Fore.LIGHTYELLOW_EX +
          "Good bye! 😊")


@input_error
def parse_input(input_str: str):
    command, *args = input_str.split()
    command = command.strip().lower()
    return command, *args


def show_help():
    return ("Command list:\n"
            "\tadd [name] [phone number]        | add new name and phone number\n"
            "\tphone [name]                     | find phone number by person's name\n"
            "\tchange [name] [new phone number] | edit phone number by person's name\n"
            "\tall                              | show all phone numbers\n"
            "\thelp                             | if you need to see this commands again\n"
            "\texit / close                     | to close bot-assistant")


@input_error
def change_contact(args, contacts:dict):
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return colorama.Fore.GREEN + '✅ Contact changed!'
    else:
        raise KeyError


@input_error
def add_contact(args, contacts:dict):
    name, phone = args

    if name in contacts:
        raise KeyError(name, 'exists')

    contacts[name] = phone
    return colorama.Fore.GREEN + '✅ Contact added!'


@input_error
def find_contact(name, contacts:dict):
    return f"{name[0]}: {contacts[name[0]]}"


@input_error
def show_all(contacts:dict):
    if len(contacts) == 0:
        return 'No contacts found'

    all_contacts = "All contacts:\n"
    for i, (name, phone) in enumerate(contacts.items()):
        all_contacts += f"{i+1}. {name}: {phone}\n"
    return all_contacts


if __name__ == '__main__':
    main()