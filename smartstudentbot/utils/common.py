import re
from typing import Optional
from aiogram.utils.markdown import hbold, hitalic

# --- Validators ---

def is_valid_email(email: str) -> bool:
    """Checks if the provided string is a valid email address."""
    # This regex is more strict and prevents consecutive dots in the domain.
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?$'
    return re.match(pattern, email) is not None

def is_valid_age(age_str: str) -> bool:
    """Checks if the age is a number between 16 and 100."""
    if not age_str.isdigit():
        return False
    age = int(age_str)
    return 16 <= age <= 100

# --- Sanitizers ---

def sanitize_markdown(text: str) -> str:
    """
    Escapes characters that have special meaning in Telegram's MarkdownV2.
    This is a simplified version. For a robust solution, you might need a more comprehensive list.
    """
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

# --- ISEE Calculator Logic ---
# As provided in the prompt, moved to a common utility file.

# These coefficients are just examples and should be verified with official sources.
FAMILY_COEFFICIENTS = {1: 1.00, 2: 1.57, 3: 2.04, 4: 2.46, 5: 2.85}
ISEE_THRESHOLD = 23000.0  # Example threshold

def get_family_coeff(family_n: int) -> float:
    """Gets the family coefficient for ISEE calculation."""
    return FAMILY_COEFFICIENTS.get(family_n, FAMILY_COEFFICIENTS[5] + 0.35 * (family_n - 5))

def calculate_isee(income: float, property_value: float, family_n: int) -> tuple[float, str]:
    """
    Calculates the ISEE value and determines the scholarship status.
    Note: This is a simplified model. Real ISEE calculation is much more complex.
    """
    # ISP (Indicatore della Situazione Patrimoniale) = 20% of total property value
    isp = property_value * 0.20

    # ISE (Indicatore della Situazione Economica) = Income + ISP
    ise = income + isp

    # ISEE = ISE / Family Coefficient
    isee = ise / get_family_coeff(family_n)

    # Determine scholarship status based on percentage of the threshold
    if isee <= 0:
        return isee, "Borsa di studio completa" # Full scholarship

    percentage = (isee / ISEE_THRESHOLD) * 100

    if percentage <= 55:
        status = "Borsa di studio completa" # Full scholarship
    elif percentage <= 71.5:
        status = "Borsa di studio media" # Medium scholarship
    elif percentage <= 100:
        status = "Borsa di studio parziale" # Partial scholarship
    else:
        status = "Non idoneo alla borsa di studio" # Not eligible for scholarship

    return isee, status

def format_isee_results(isee: float, status: str) -> str:
    """Formats the ISEE results into a user-friendly message."""
    return (
        f"📄 {hbold('Risultati Calcolo ISEE')}\n\n"
        f"🧮 {hbold('Valore ISEE Calcolato:')} {isee:.2f} €\n"
        f"📊 {hbold('Stato Borsa di Studio:')} {hitalic(status)}\n\n"
        f"{hitalic('Nota: Questo è un calcolo semplificato e non ufficiale.')}"
    )
