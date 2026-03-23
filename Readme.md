# Dashboard Task
---

[Відкрити дашборд як публічний лінк](https://app.powerbi.com/view?r=eyJrIjoiYTc0ODc0MTYtMTI5Yy00ZjdlLWEzMDYtZWMwZjY2NThiN2Y0IiwidCI6IjU5YTZhM2Y5LTMwYWItNDBmZi1hNDZhLWYzZThkZDU4OGZhOSIsImMiOjl9&pageName=14cfc832784b366d6726)


## Виконані кроки:
1. Згенеровано dataset в Python - 3 таблиці фактів (impressions, cliks, conversions)
2. Моделювання даних в Power BI - dimentional refactoring (реляційні таблиці з зв'язками, в тому числі календар)
3. Figma дизайн
4. Побудова Дашборда


## Примітки:
1. Таблиця календар прив'язана до усіх fact tables in funnel
2. Profit (можна знайти в custom card) розрахований як Marketing Profit ( [Total Revenue] - [Marketing Cost] ), оскільки, як правило, в маркетингових даних відсутні дані про зарплати і операційні витрати для розрахунку справжнього Company Profit
3. RLS не активований, інакше Microsoft server видалить public link. Для налаштування: У Power BI можна задати RLS прямо на dim_geo через DAX (наприклад, dim_geo[geo] IN {"US","DE"}) — тоді фільтр пошириться на всі fact-таблиці через зв’язки.


Успішні компанії: TT_Scale, FB_Prospecting, GG_Search (відсортовано по спаданню показників ROMI & ROAS & ROI). Провальних нема якщо таргет = Revenue > Ads Spend.
Device: Mobile має кращу конверсію ніж Desktop.
