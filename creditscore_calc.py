import pandas as pd

# Define the path to the Excel file
excel_path = '/content/SORTED DATASET FOR CODE.xlsx'
def calculate_score(variable, score_ranges):
    for i in range(len(score_ranges)):
        if variable <= score_ranges[i][0]:
            return score_ranges[i][1]

    # If the variable exceeds the given range, assign the score for "and higher values"
    return score_ranges[-1][1]

def payment_history_score(row):
    variables = ['DerogCnt', 'TLDel60Cnt', 'TLDel3060Cnt24', 'TLDel90Cnt24',
                 'TLDel60CntAll', 'TLDel60Cnt24', 'TLBadDerogCnt', 'TLBadCnt24']

    total_score = 0
    for variable in variables:
        value = row[variable]
        score_ranges = [(0, 105), (1, 90), (2, 75), (4, 60), (7, 45), (15, 30)]
        total_score += calculate_score(value, score_ranges)

    return total_score

def credit_exposure_score(row):
    variables = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Column indices

    total_score = 0
    for idx in variables:
        value = row.iloc[idx]
        if idx == 0:  # CollectCnt
            score_ranges = [(0, 77), (1, 66), (2, 55), (3, 44), (4, 33), (5, 22), (10, 11)]
        elif idx == 1:  # TLSum (in rupees)
            score_ranges = [(0, 11), (800001, 22), (1600001, 33), (2400001, 44), (3600001, 55), (8000001, 66), (100000001, 77)]
        elif idx == 2:  # TLMaxSum (in rupees)
            score_ranges = [(0, 11), (1000001, 22), (2000001, 33), (3000001, 44), (4000001, 55), (6000001, 66), (100000001, 77)]
        elif idx in [3, 4, 5]:  # TLCnt03, TLCnt12, TLCnt24
            score_ranges = [(0, 11), (1, 22), (2, 33), (3, 44), (4, 55), (5, 66), (10, 74)]
        elif idx == 6:  # TLSatCnt
            score_ranges = [(0, 11), (6, 22), (11, 33), (16, 44), (21, 55), (26, 66), (30, 77)]
        elif idx in [7, 8]:  # TL75UtilCnt, TL50UtilCnt
            score_ranges = [(0, 77), (1, 70), (2, 65), (3, 60), (4, 55), (5, 50), (6, 45), (7, 40), (8, 35), (9, 30), (10, 25), (11, 20), (15, 10)]
        elif idx == 9:  # TLBalHCPct
            score_ranges = [(0, 77), (20, 66), (30, 55), (40, 44), (50, 33), (60, 22), (70, 11), (100, 5)]
        elif idx == 10:  # TLSatPct
            score_ranges = [(0, 11), (30, 22), (50, 33), (60, 44), (70, 55), (80, 66), (90, 77)]

        total_score += calculate_score(value, score_ranges)

    return total_score

def credit_history_score(row):
    variables = ['TLTimeFirst', 'TLTimeLast', 'TLCnt']

    total_score = 0
    for variable in variables:
        value = row[variable]
        if variable == 'TLTimeFirst':
            score_ranges = [(0, 120), (60, 130), (120, 140), (180, 150), (240, 160), (300, 170),
                            (360, 180), (420, 190), (480, 200), (540, 210), (600, 220), (660, 230),
                            (720, 240), (780, 250), (840, 260), (900, 270), (960, 283)]
        elif variable == 'TLTimeLast':
            score_ranges = [(0, 283), (60, 270), (120, 260), (180, 250), (240, 240), (300, 230),
                            (360, 220), (420, 210), (480, 200), (540, 190), (600, 180), (660, 170),
                            (720, 160), (780, 150), (840, 140), (900, 130), (960, 120)]
        elif variable == 'TLCnt':
            score_ranges = [(0, 120), (6, 140), (11, 160), (16, 180), (21, 200), (26, 220), (31, 240),
                            (36, 260), (40, 283)]

        total_score += calculate_score(value, score_ranges)

    return total_score

def credit_type_score(row):
    value = row['BanruptcyInd']
    score_ranges = [(0, 850), (1, 0)]
    return calculate_score(value, score_ranges)


def recent_activities_score(row):
    variables = ['InqCnt06', 'InqTimeLast', 'InqFinanceCnt24', 'TLOpenPct', 'TLOpen24Pct']

    total_score = 0
    for variable in variables:
        value = row[variable]
        if variable == 'InqCnt06' or variable == 'InqFinanceCnt24':
            score_ranges = [(0, 170), (1, 150), (2, 130), (4, 110), (8, 90), (15, 70)]
        elif variable == 'InqTimeLast':
            score_ranges = [(0, 70), (1, 90), (2, 110), (4, 130), (8, 150), (15, 170)]
        elif variable == 'TLOpenPct' or variable == 'TLOpen24Pct':
            score_ranges = [(0, 50), (10, 70), (20, 90), (40, 110), (60, 130), (80, 150), (96, 170)]

        total_score += calculate_score(value, score_ranges)

    return total_score


def calculate_total_score():
    results = []
    payment_history_weight = 0.35
    credit_exposure_weight = 0.30
    credit_history_weight = 0.15
    credit_type_weight = 0.10
    recent_activities_weight = 0.10

    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(excel_path)

    for index in range(len(df)):
        payment_history = payment_history_score(df.loc[index])
        credit_exposure = credit_exposure_score(df.loc[index])
        credit_history = credit_history_score(df.loc[index])
        credit_type = credit_type_score(df.loc[index])
        recent_activities = recent_activities_score(df.loc[index])

        total_credit_score = (
            payment_history * payment_history_weight +
            credit_exposure * credit_exposure_weight +
            credit_history * credit_history_weight +
            credit_type * credit_type_weight +
            recent_activities * recent_activities_weight
        )

        result_dict = {
            'Row Number': f'Row {index + 1}',
            'Total Credit Score': total_credit_score
        }
        results.append(result_dict)

    # Print the results outside the loop
    for result in results:
        print(f"{result['Row Number']}: {result['Total Credit Score']:.2f}")

    # Save results to Excel file
    results_df = pd.DataFrame(results)
    results_df.to_excel('/content/CREDIT_SCORES.xlsx', index=False)

if __name__ == "__main__":
    calculate_total_score()
