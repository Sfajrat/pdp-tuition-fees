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


    return "\n".join(report)