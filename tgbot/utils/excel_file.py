import io
import openpyxl


async def generate_excel_file(user_ids, first_names, user_names, registartion_date):
    # Создаем новую книгу Excel
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Users"

    # Заголовки столбцов
    sheet['A1'] = 'User ID'
    sheet['B1'] = 'First Name'
    sheet['C1'] = 'Username'
    sheet['D1'] = 'Registration Date'

    # Заполняем данными
    for user_id, first_name, user_name, registartion_date in zip(user_ids,
                                                                 first_names,
                                                                 user_names,
                                                                 registartion_date):
        sheet.append([str(user_id), first_name, user_name, registartion_date])

    # Создаем бинарный поток для записи в файл
    excel_buffer = io.BytesIO()
    workbook.save(excel_buffer)
    excel_buffer.seek(0)

    return excel_buffer
