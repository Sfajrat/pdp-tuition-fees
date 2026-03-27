from datetime import datetime
from data_analytics import analyze_dataset
from statistics_module import describe_statistics
from comparative_analysis import ComparativeAnalysis


def generate_report(df):

    if df.empty:
        return "Ошибка: Нет данных для формирования отчёта."

    analytics = analyze_dataset(df)
    stats = describe_statistics(df)
    comp = ComparativeAnalysis(df)
    comp_data = comp.get_report_dict()

    report = []
    report.append("АНАЛИТИЧЕСКИЙ ОТЧЁТ ПО СТОИМОСТИ ОБРАЗОВАТЕЛЬНЫХ ПРОГРАММ")
    report.append("=" * 88)
    report.append(f"Дата формирования: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    report.append(f"Количество записей в анализе: {len(df)}")
    report.append("=" * 88)
    report.append("")

    # 1. Основные показатели
    report.append("1. ОСНОВНЫЕ ПОКАЗАТЕЛИ")
    report.append("-" * 65)
    report.append(f"Средняя стоимость обучения:          {analytics['avg_price']:,.2f} руб.")
    report.append(f"Максимальная стоимость:               {analytics['max_price']:,.2f} руб.")
    report.append(f"Минимальная стоимость:                {analytics['min_price']:,.2f} руб.")
    report.append(f"Общий темп роста за период:           {analytics['growth_rate']:.2f}%")
    report.append("")

    # 2. Статистические показатели
    report.append("2. СТАТИСТИЧЕСКИЕ ПОКАЗАТЕЛИ")
    report.append("-" * 65)
    report.append(f"Среднее значение:                     {stats['mean']:,.2f} руб.")
    report.append(f"Медиана:                              {stats['median']:,.2f} руб.")
    report.append(f"Стандартное отклонение:               {stats['std']:,.2f} руб.")
    report.append(f"Дисперсия:                            {stats['variance']:,.0f}")
    report.append("")

    # 3. Сравнительный анализ
    report.append("3. СРАВНИТЕЛЬНЫЙ АНАЛИЗ")
    report.append("-" * 65)

    report.append("\n3.1 Средняя стоимость обучения по вузам:")
    report.append(comp_data["by_university"].to_string(float_format="{:,.2f}".format))

    report.append("\n\n3.2 Средняя стоимость обучения по программам:")
    report.append(comp_data["by_program"].to_string(float_format="{:,.2f}".format))

    report.append("\n\n3.3 ТОП-7 самых дорогих направлений подготовки:")
    top_exp = comp_data["top_expensive"].head(7)
    report.append(top_exp.to_string(index=False, float_format="{:,.2f}".format))

    report.append("\n\n3.4 Темп роста стоимости по программам:")
    growth_df = comp_data["growth"].copy()
    # Переименовываем только нужные колонки для отчёта
    growth_df = growth_df.rename(columns={
        'program': 'Программа',
        'growth_percent': 'Темп роста (%)',
        'first_year': 'Первый год',
        'last_year': 'Последний год'
    })
    
    # Сортируем по убыванию роста
    growth_df = growth_df.sort_values('Темп роста (%)', ascending=False)
    report.append(growth_df.to_string(index=False, float_format="{:,.2f}".format))

    # 4. Официальная статистика
    report.append("\n" + "=" * 88)
    report.append("4. ОФИЦИАЛЬНАЯ СТАТИСТИКА МИНОБРНАУКИ И РОССТАТА")
    report.append("=" * 88)
    report.append("Детальных данных по стоимости конкретных образовательных программ")
    report.append("и отдельных вузов в открытом доступе не публикуется.")
    report.append("")
    report.append("Согласно официальным источникам:")
    report.append("• В 2025 году средний рост стоимости обучения по России составил ≈ 12%.")
    report.append("• В Москве и Санкт-Петербурге рост был выше — до 15,7%.")
    report.append("• Средняя стоимость обучения в 2025 году (по данным портала Табитуриент)")
    report.append("  составляет примерно 200 697 – 224 000 рублей в год.")
    report.append("")
    report.append("Примечание: Анализ выполнен на синтезированном датасете, построенном")
    report.append("с учётом реальных тенденций рынка образовательных услуг РФ.")

    report.append("\n" + "=" * 88)
    report.append("Отчёт сформирован автоматически системой анализа стоимости")
    report.append("образовательных программ с использованием методов машинного обучения.")
    report.append("Использованные модели: Linear Regression, Random Forest Regressor, Gradient Boosting Regressor.")


    return "\n".join(report)