import os
import django
from django.utils import timezone

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SoPaC.settings")

# Инициализируем Django
django.setup()


from contracts_projects.models import Contract, Project


def view_projects():
    print("Список проектов")
    projects = Project.objects.all()

    if not projects:
        print("Нет существующих проектов.")
        return

    for project in projects:
        print(f"Номер проекта: {project.id}, Название проекта: {project.name}")


def view_contracts():
    print("Список договоров")
    contracts = Contract.objects.all()

    if not contracts:
        print("Нет существующих договоров.")
        return

    for contract in contracts:
        print(f"Номер договора: {contract.id}, Название договора: {contract.name}, Статус: {contract.status}")


def create_contract():
    print("Создание договора")
    name = input("Введите название договора: ")
    contract = Contract(name=name, status='draft')
    contract.save()
    print("Договор успешно создан.")


def confirm_contract():
    print("Подтверждение договора")
    contracts = Contract.objects.filter(status='draft')
    contract_list = []

    if not contracts:
        print("В настоящее время все договоры активны")
        return

    for contract in contracts:
        contract_list.append((contract.pk, contract.name))
        print(f"Номер договора: {contract.pk}, Название договора: {contract.name}")

    contract_id = input("Выберите номер договора для подтверждения: ")

    try:
        contract_id = int(contract_id)
        if contract_id not in [contract[0] for contract in contract_list]:
            raise Contract.DoesNotExist

        contract = Contract.objects.get(pk=contract_id)
        contract.status = 'active'
        contract.signing_date = timezone.now().date()
        contract.save()
        print("Договор успешно подтвержден.")
    except ValueError:
        print("Некорректный номер договора. Введите число.")
    except Contract.DoesNotExist:
        print("Договор с указанным номером не найден.")


def complete_contract():
    print("Завершение договора")
    contracts = Contract.objects.filter(status='active')

    if not contracts:
        print("Нет активных договоров, чтобы завершить.")
        return

    for contract in contracts:
        print(f"Номер договора: {contract.pk}, Название договора: {contract.name}")

    contract_id = input("Выберите номер договора для завершения: ")

    try:
        contract = Contract.objects.get(pk=contract_id)

        if contract.status != 'active':
            print("Нельзя завершить черновик или завершенный договор.")
            return

        contract.complete_action()
        print("Договор успешно завершен.")
    except Contract.DoesNotExist:
        print("Договор с указанным номером не найден.")


def create_project():
    contracts = Contract.objects.filter(status='active', project_id=None)

    if not contracts:
        print("Нет активных договоров.")
        return

    print("Создание проекта")
    name = input("Введите название проекта: ")
    project = Project(name=name)
    project.save()


def add_contract_to_project():
    print("Добавление договора в проект")
    projects = Project.objects.all()

    for project in projects:
        print(f"Номер проекта: {project.pk}, Название проекта: {project.name}")

    project_id = input("Выберите номер проекта: ")

    try:
        project = Project.objects.get(pk=project_id)

        if project.contract_set.filter(status='active').exists():
            print("У проекта уже есть активный договор.")
            return

        contracts = Contract.objects.filter(status='active')

        if not contracts:
            print("Нет активных договоров.")
            return

        for contract in contracts:
            print(f"Номер договора: {contract.pk}, Название договора: {contract.name}")

        contract_id = input("Выберите номер договора для добавления: ")

        try:
            contract = Contract.objects.get(pk=contract_id)

            if contract.status != 'active':
                print("Выбранный договор не является активным.")
                return

            if contract.project is not None:
                print("Договор уже привязан к другому проекту.")
                return

            if project.contract_set.filter(pk=contract_id).exists():
                print("Договор уже добавлен в этот проект.")
                return

            contract.project = project
            contract.save()
            print("Договор успешно добавлен в проект.")
        except Contract.DoesNotExist:
            print("Договор с указанным номером не найден.")
    except Project.DoesNotExist:
        print("Проект с указанным номером не найден.")


def complete_action_in_project():
    print("Завершение действия в проекте")

    projects = Project.objects.filter(contract__status='active').distinct()

    if not projects:
        print("Нет доступных проектов с активными договорами.")
        return

    for project in projects:
        print(f"Номер проекта:{project.pk} Название проекта:{project.name}")

    project_id = input("Введите номер проекта: ")
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        print("Проект с указанным номером не найден.")
        return

    contract = project.contract_set.filter(status='active').first()

    if not contract:
        print("Нет активного договора в данном проекте.")
        return

    contract.complete_action()
    print("Действие в договоре успешно завершено.")


def complete_program():
    print("Завершение работы с программой")


def print_menu():
    print("Меню:")
    print("  Договор:")
    print("    1. Создать договор")
    print("    2. Подтвердить договор")
    print("    3. Завершить договор")
    print("  Проект")
    print("    4. Создать проект")
    print("    5. Добавить договор в проект")
    print("    6. Завершить действие по договору")
    print("7. Список договоров")
    print("8. Список проектов")
    print("9. Завершить работу с программой")


while True:
    print_menu()
    choice = input("Выберите действие (1-9): ")

    if choice == "1":
        create_contract()
    elif choice == "2":
        confirm_contract()
    elif choice == "3":
        complete_contract()
    elif choice == "4":
        create_project()
    elif choice == "5":
        add_contract_to_project()
    elif choice == "6":
        complete_action_in_project()
    elif choice == "7":
        view_contracts()
    elif choice == "8":
        view_projects()
    elif choice == "9":
        complete_program()
        break
    else:
        print("Некорректный выбор. Попробуйте снова.")
