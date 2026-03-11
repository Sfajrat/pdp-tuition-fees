def export_to_csv(df, path):

    df.to_csv(path, index=False)

def export_to_excel(df, path):

    df.to_excel(path, index=False)

def export_report(report_text, path):

    with open(path, "w", encoding="utf-8") as f:
        f.write(report_text)