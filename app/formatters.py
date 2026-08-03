def format_salary_range(salary_min, salary_max):
    if salary_min is None and salary_max is None:
        return "Unknown"
    elif salary_min is not None and salary_max is not None and salary_min == salary_max:
        return f"${salary_max:,.0f}"
    elif salary_min is not None and salary_max is None:
        return f"From ${salary_min:,.0f}"
    elif salary_max is not None and salary_min is None:
        return f"Up to ${salary_max:,.0f}"
    elif salary_min is not None and salary_max is not None:
        return f"${salary_min:,.0f} - ${salary_max:,.0f}"
