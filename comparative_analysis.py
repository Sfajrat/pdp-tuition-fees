import pandas as pd
import numpy as np
from scipy import stats


class ComparativeAnalysis:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.df.columns = [col.lower().strip() for col in self.df.columns]

        if 'university' not in self.df.columns:
            self.df['university'] = 'Не указан'
        if 'price' not in self.df.columns:
            raise ValueError("В данных отсутствует столбец 'price'")

    def analyze_by_program(self):
        return self.df.groupby('program').agg(
            avg_price=('price', 'mean'),
            min_price=('price', 'min'),
            max_price=('price', 'max'),
            count=('price', 'count'),
            std=('price', 'std')
        ).round(2).sort_values('avg_price', ascending=False)

    def analyze_by_university(self):
        return self.df.groupby('university').agg(
            avg_price=('price', 'mean'),
            min_price=('price', 'min'),
            max_price=('price', 'max'),
            count=('price', 'count'),
            std=('price', 'std')
        ).round(2).sort_values('avg_price', ascending=False)

    def analyze_by_year(self):
        return self.df.groupby('year').agg(
            avg_price=('price', 'mean'),
            total_students=('students_count', 'sum'),
            count=('price', 'count')
        ).round(2)

    def top_expensive(self, n=7):
        return (self.df.groupby(['university', 'program'])['price']
                .mean()
                .round(2)
                .sort_values(ascending=False)
                .head(n)
                .reset_index())

    def price_growth_by_program(self):
        result = []
        for program in self.df['program'].unique():
            prog_df = self.df[self.df['program'] == program].sort_values('year')
            if len(prog_df) < 2:
                continue
            first_price = prog_df['price'].iloc[0]
            last_price = prog_df['price'].iloc[-1]
            growth = ((last_price - first_price) / first_price) * 100
            result.append({
                'program': program,
                'growth_percent': round(growth, 2),
                'first_year': int(prog_df['year'].iloc[0]),
                'last_year': int(prog_df['year'].iloc[-1])
            })
        return pd.DataFrame(result).sort_values('growth_percent', ascending=False)

    def correlation_analysis(self):
        #Корреляционный анализ
        numeric_df = self.df.select_dtypes(include=[np.number])
        corr_matrix = numeric_df.corr().round(3)
        price_corr = corr_matrix['price'].sort_values(ascending=False).round(3)
        return {
            'correlation_matrix': corr_matrix,
            'price_correlations': price_corr
        }

    def anova_analysis(self):
        #ANOVA — проверка статистической значимости различий
        results = []

        # ANOVA по вузам
        groups_uni = [group['price'].values for name, group in self.df.groupby('university') if len(group) > 1]
        if len(groups_uni) >= 2:
            f_stat, p_value = stats.f_oneway(*groups_uni)
            results.append({
                'Группа': 'По вузам',
                'F-статистика': round(f_stat, 4),
                'p-value': round(p_value, 6),
                'Значимо (p<0.05)': p_value < 0.05
            })

        # ANOVA по программам
        groups_prog = [group['price'].values for name, group in self.df.groupby('program') if len(group) > 1]
        if len(groups_prog) >= 2:
            f_stat, p_value = stats.f_oneway(*groups_prog)
            results.append({
                'Группа': 'По программам',
                'F-статистика': round(f_stat, 4),
                'p-value': round(p_value, 6),
                'Значимо (p<0.05)': p_value < 0.05
            })

        return pd.DataFrame(results)

    def get_report_dict(self):
        corr = self.correlation_analysis()
        anova = self.anova_analysis()

        return {
            "by_program": self.analyze_by_program(),
            "by_university": self.analyze_by_university(),
            "by_year": self.analyze_by_year(),
            "top_expensive": self.top_expensive(10),
            "growth": self.price_growth_by_program(),
            "correlations": corr,
            "anova": anova
        }