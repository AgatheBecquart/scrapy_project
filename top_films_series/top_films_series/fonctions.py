def convert_to_minutes(duration):
    duration_str = ''.join(duration)  # Combine toutes les chaînes de la liste en une seule
    parts = duration_str.split()  # Sépare les parties de la durée par des espaces
    hours = 0
    minutes = 0
    for part in parts:
        if part.endswith('h'):  # Si la partie se termine par 'h', c'est le nombre d'heures
            hours = int(part[:-1])
        elif part.endswith('m'):  # Si la partie se termine par 'm', c'est le nombre de minutes
            minutes = int(part[:-1])
    return hours*60 + minutes