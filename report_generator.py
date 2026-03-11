from datetime import datetime
from data_analytics import analyze_dataset
from statistics import describe_statistics


def generate_report(df):

    analytics = analyze_dataset(df)
    stats = describe_statistics(df)

    report = []

    report.append("АНАЛИТИЧЕСКИЙ ОТЧЁТ")
    report.append("")
    report.append(f"Дата формирования: {datetime.now()}")
    report.append("")

    report.append("Основные показатели:")
    report.append(f"Средняя стоимость: {analytics['avg_price']:.2f}")
    report.append(f"Максимальная стоимость: {analytics['max_price']:.2f}")
    report.append(f"Минимальная стоимость: {analytics['min_price']:.2f}")
    report.append(f"Темп роста: {analytics['growth_rate']:.2f}%")

    report.append("")
    report.append("Статистические показатели:")

    report.append(f"Среднее значение: {stats['mean']:.2f}")
    report.append(f"Медиана: {stats['median']:.2f}")
    report.append(f"Стандартное отклонение: {stats['std']:.2f}")
    report.append(f"Дисперсия: {stats['variance']:.2f}")

    return "\n".join(report)