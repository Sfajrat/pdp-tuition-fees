import nbformat as nbf

nb = nbf.v4.new_notebook()

cells = []

# 1. Заголовок и описание
cells.append(
    nbf.v4.new_markdown_cell(
        "# Интеллектуальная система мониторинга динамики стоимости образовательных услуг\n"
        "*(на примере ЧОУ ВО «Московский университет имени С.Ю. Витте»)*\n\n"
        "Данный ноутбук содержит этапы:\n"
        "1. Загрузка и анализ датасета `data.csv`.\n"
        "2. Визуализация динамики стоимости обучения.\n"
        "3. Обучение моделей линейной регрессии по образовательным программам.\n"
        "4. Прогноз стоимости обучения на будущие годы.\n"
    )
)

# 2. Импорты
cells.append(
    nbf.v4.new_code_cell(
        "import pandas as pd\n"
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "from sklearn.linear_model import LinearRegression\n"
        "import seaborn as sns\n"
        "%matplotlib inline\n"
    )
)

# 3. Загрузка данных
cells.append(
    nbf.v4.new_markdown_cell("## Загрузка и первичный анализ данных")
)
cells.append(
    nbf.v4.new_code_cell(
        "df = pd.read_csv('data.csv')\n"
        "df.head()"
    )
)

# 4. Проверка структуры
cells.append(
    nbf.v4.new_code_cell(
        "df.info()"
    )
)

# 5. Описание данных
cells.append(
    nbf.v4.new_markdown_cell(
        "Ожидаемая структура датасета:\n\n"
        "- `year` — год;\n"
        "- `university` — наименование вуза;\n"
        "- `program` — образовательная программа (направление подготовки);\n"
        "- `form` — форма обучения (например, очная);\n"
        "- `cost` — стоимость обучения в рублях."
    )
)

# 6. Базовая статистика
cells.append(
    nbf.v4.new_markdown_cell("## Базовый статистический анализ")
)
cells.append(
    nbf.v4.new_code_cell(
        "df.describe(include='all')"
    )
)

# 7. Визуализация динамики по МУИВ
cells.append(
    nbf.v4.new_markdown_cell("## Динамика стоимости обучения в МУИВ по программам")
)
cells.append(
    nbf.v4.new_code_cell(
        "muiv = df[df['university'].str.contains('МУИВ')]\n"
        "plt.figure(figsize=(10,6))\n"
        "sns.lineplot(data=muiv, x='year', y='cost', hue='program', marker='o')\n"
        "plt.title('Динамика стоимости обучения в МУИВ по программам')\n"
        "plt.ylabel('Стоимость, руб.')\n"
        "plt.grid(True)\n"
        "plt.show()"
    )
)

# 8. Сравнение вузов по одной программе (например, Экономика)
cells.append(
    nbf.v4.new_markdown_cell("## Сравнение стоимости обучения по программе «Экономика» между вузами")
)
cells.append(
    nbf.v4.new_code_cell(
        "eco = df[df['program'] == 'Экономика']\n"
        "plt.figure(figsize=(10,6))\n"
        "sns.lineplot(data=eco, x='year', y='cost', hue='university', marker='o')\n"
        "plt.title('Сравнение стоимости обучения по программе \"Экономика\"')\n"
        "plt.ylabel('Стоимость, руб.')\n"
        "plt.grid(True)\n"
        "plt.show()"
    )
)

# 9. Обучение моделей по программам
cells.append(
    nbf.v4.new_markdown_cell("## Обучение моделей линейной регрессии по образовательным программам")
)
cells.append(
    nbf.v4.new_code_cell(
        "models = {}\n"
        "for program in df['program'].unique():\n"
        "    df_prog = df[df['program'] == program]\n"
        "    X = df_prog[['year']]\n"
        "    y = df_prog['cost']\n"
        "    model = LinearRegression()\n"
        "    model.fit(X, y)\n"
        "    models[program] = model\n"
        "    print(f'Программа: {program}, коэффициент наклона: {model.coef_[0]:.2f}, сдвиг: {model.intercept_:.2f}')"
    )
)

# 10. Функция прогноза
cells.append(
    nbf.v4.new_markdown_cell("## Функция для прогноза стоимости обучения")
)
cells.append(
    nbf.v4.new_code_cell(
        "def predict_cost(program, year):\n"
        "    if program not in models:\n"
        "        raise ValueError(f'Нет модели для программы: {program}')\n"
        "    model = models[program]\n"
        "    X = np.array([[year]])\n"
        "    return float(model.predict(X)[0])\n"
        "\n"
        "predict_cost('Экономика', 2026)"
    )
)

# 11. Прогноз на несколько лет вперёд
cells.append(
    nbf.v4.new_markdown_cell("## Прогноз стоимости обучения на несколько лет вперёд")
)
cells.append(
    nbf.v4.new_code_cell(
        "future_years = list(range(2025, 2031))\n"
        "program = 'Экономика'\n"
        "preds = []\n"
        "for y in future_years:\n"
        "    preds.append({'year': y, 'program': program, 'pred_cost': predict_cost(program, y)})\n"
        "pred_df = pd.DataFrame(preds)\n"
        "pred_df"
    )
)

# 12. Визуализация прогноза + фактических данных
cells.append(
    nbf.v4.new_markdown_cell("## Визуализация фактических и прогнозных значений для выбранной программы")
)
cells.append(
    nbf.v4.new_code_cell(
        "prog = 'Экономика'\n"
        "df_prog = df[df['program'] == prog]\n"
        "\n"
        "plt.figure(figsize=(10,6))\n"
        "plt.plot(df_prog['year'], df_prog['cost'], marker='o', label='Фактические данные')\n"
        "plt.plot(pred_df['year'], pred_df['pred_cost'], marker='x', linestyle='--', label='Прогноз')\n"
        "plt.title(f'Фактическая и прогнозная стоимость обучения: {prog}')\n"
        "plt.xlabel('Год')\n"
        "plt.ylabel('Стоимость, руб.')\n"
        "plt.grid(True)\n"
        "plt.legend()\n"
        "plt.show()"
    )
)

# 13. Заключение
cells.append(
    nbf.v4.new_markdown_cell(
        "## Выводы\n\n"
        "- Построены модели линейной регрессии по образовательным программам.\n"
        "- Выполнен анализ динамики стоимости обучения в МУИВ и вузах‑аналогах.\n"
        "- Реализована функция прогноза стоимости обучения на основе исторических данных.\n"
        "- Полученные результаты могут быть использованы в интеллектуальной системе мониторинга динамики стоимости образовательных услуг."
    )
)

nb["cells"] = cells

with open("tuition_analysis.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print("Готово: создан файл tuition_analysis.ipynb")
