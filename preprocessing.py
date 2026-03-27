def prepare_data(df):
    df = df.copy()

    # Приводим все названия колонок к нижнему регистру
    df.columns = [col.lower().strip() for col in df.columns]

    # Возможные названия для цены
    price_mapping = {
        "стоимость": "price",
        "cost": "price",
        "цена": "price"
    }
    for old, new in price_mapping.items():
        if old in df.columns:
            df.rename(columns={old: new}, inplace=True)
            break

    # Возможные названия для года
    year_mapping = {
        "год": "year",
        "year": "year"
    }
    for old, new in year_mapping.items():
        if old in df.columns:
            df.rename(columns={old: new}, inplace=True)
            break

    df = df.dropna()

    if "price" not in df.columns:
        raise Exception("В файле отсутствует столбец price")

    df = df[df["price"] > 0]

    # Добавляем university, если отсутствует
    if "university" not in df.columns:
        df["university"] = "Не указан"

    return df
