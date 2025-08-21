import getpass
import math
import re
import hashlib
import requests

# Language dictionary for translations
LANGUAGES = {
    "it": {
        "prompt": "Inserisci la password: ",
        "strength": "Forza: {}",
        "entropy": "Entropia stimata: {:.2f} bit",
        "classical_time": "Tempo cracking classico (stima): {}",
        "quantum_time": "Tempo cracking quantistico (stima con Grover): {}",
        "breach_found": "ATTENZIONE: Password compromessa in {} breach!",
        "breach_not_found": "Password non trovata in breach noti.",
        "breach_error": "Impossibile controllare breach.",
        "seconds": "{:.2f} secondi",
        "minutes": "{:.2f} minuti",
        "hours": "{:.2f} ore",
        "days": "{:.2f} giorni",
        "years": "{:.2f} anni",
        "api_error": "Errore nella query API: {}"
    },
    "en": {
        "prompt": "Enter the password: ",
        "strength": "Strength: {}",
        "entropy": "Estimated entropy: {:.2f} bits",
        "classical_time": "Classical cracking time (estimate): {}",
        "quantum_time": "Quantum cracking time (estimate with Grover): {}",
        "breach_found": "WARNING: Password found in {} breaches!",
        "breach_not_found": "Password not found in known breaches.",
        "breach_error": "Unable to check for breaches.",
        "seconds": "{:.2f} seconds",
        "minutes": "{:.2f} minutes",
        "hours": "{:.2f} hours",
        "days": "{:.2f} days",
        "years": "{:.2f} years",
        "api_error": "Error in API query: {}"
    }
}

def evaluate_strength(password):
    # Base rules for strength
    length = len(password)
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_symbol = bool(re.search(r'[^A-Za-z0-9]', password))
    
    score = 0
    if length >= 12: score += 2
    elif length >= 8: score += 1
    if has_upper: score += 1
    if has_lower: score += 1
    if has_digit: score += 1
    if has_symbol: score += 1
    
    # Language-specific strength labels
    strength_it = "Debole" if score < 4 else "Media" if score < 6 else "Forte"
    strength_en = "Weak" if score < 4 else "Medium" if score < 6 else "Strong"
    strength = {"it": strength_it, "en": strength_en}
    
    # Estimate entropy (assuming charset of ~95 printable characters)
    charset_size = 95  # Letters, numbers, symbols
    entropy = length * math.log2(charset_size)
    
    # Estimate classical cracking time (brute force, assuming 10^9 attempts/sec on GPU)
    classical_attempts = 2 ** entropy
    classical_rate = 1e9  # 1 billion hashes/sec
    classical_time_sec = classical_attempts / classical_rate
    classical_time = {lang: format_time(classical_time_sec, lang) for lang in LANGUAGES}
    
    return strength, entropy, classical_time

def format_time(seconds, lang):
    if seconds < 60: return LANGUAGES[lang]["seconds"].format(seconds)
    elif seconds < 3600: return LANGUAGES[lang]["minutes"].format(seconds/60)
    elif seconds < 86400: return LANGUAGES[lang]["hours"].format(seconds/3600)
    elif seconds < 31536000: return LANGUAGES[lang]["days"].format(seconds/86400)
    else: return LANGUAGES[lang]["years"].format(seconds/31536000)

def check_breach(password):
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        response = requests.get(url, headers={"Add-Padding": "true"})  # Padding for privacy
        if response.status_code == 200:
            hashes = response.text.splitlines()
            for line in hashes:
                hash_suffix, count = line.split(':')
                if hash_suffix == suffix:
                    return int(count)
        return 0
    except Exception as e:
        return -1, e  # Return error code and exception

def estimate_quantum_time(entropy, lang):
    quantum_attempts = 2 ** (entropy / 2)
    quantum_rate = 1e6  # Conservative estimate: 1 million ops/sec on future quantum
    quantum_time_sec = quantum_attempts / quantum_rate
    return format_time(quantum_time_sec, lang)

# CLI execution
if __name__ == "__main__":
    # Ask user for language preference
    lang = input("Choose language (it/en): ").lower()
    if lang not in LANGUAGES:
        lang = "en"  # Default to English if invalid
        print("Invalid language, defaulting to English.")

    password = getpass.getpass(LANGUAGES[lang]["prompt"])
    strength, entropy, classical_time = evaluate_strength(password)
    quantum_time = estimate_quantum_time(entropy, lang)
    breach_result = check_breach(password)
    
    print(LANGUAGES[lang]["strength"].format(strength[lang]))
    print(LANGUAGES[lang]["entropy"].format(entropy))
    print(LANGUAGES[lang]["classical_time"].format(classical_time[lang]))
    print(LANGUAGES[lang]["quantum_time"].format(quantum_time))
    
    if isinstance(breach_result, tuple):  # Error case
        print(LANGUAGES[lang]["api_error"].format(breach_result[1]))
        print(LANGUAGES[lang]["breach_error"])
    elif breach_result > 0:
        print(LANGUAGES[lang]["breach_found"].format(breach_result))
    else:
        print(LANGUAGES[lang]["breach_not_found"])