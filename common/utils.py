import arrow

from datetime import datetime

from django.utils import timezone

from enums.symbol import SymbolFormatEnum


# def build_symbol_string(s: Symbol, fmt: SymbolFormatEnum):
#     if fmt is SymbolFormatEnum.UPPER_UNDERSCORE:
#         return "_".join([s.base.name, s.quote.name])
# elif


def symbol_format_convert(s, from_format: SymbolFormatEnum, to_format: SymbolFormatEnum):
    if from_format is to_format:
        return s
    if from_format is SymbolFormatEnum.UPPER_UNDERSCORE or from_format is SymbolFormatEnum.LOWER_UNDERSCORE:
        if to_format is SymbolFormatEnum.LOWER_UNDERSCORE:
            return s.lower()
        elif to_format is SymbolFormatEnum.UPPER_UNDERSCORE:
            return s.upper()

        base, quote = s.split('_')
        if to_format is SymbolFormatEnum.LOWER:
            return f"{base}{quote}".lower()
        elif to_format is SymbolFormatEnum.UPPER:
            return f"{base}{quote}".upper()
        elif to_format is SymbolFormatEnum.LOWER_HYPHEN:
            return f"{base}-{quote}".lower()
        elif to_format is SymbolFormatEnum.UPPER_HYPHEN:
            return f"{base}-{quote}".upper()

    elif from_format is SymbolFormatEnum.UPPER_HYPHEN or from_format is SymbolFormatEnum.LOWER_HYPHEN:
        if to_format is SymbolFormatEnum.LOWER_HYPHEN:
            return s.lower()
        elif to_format is SymbolFormatEnum.UPPER_HYPHEN:
            return s.upper()

        base, quote = s.split('-')
        if to_format is SymbolFormatEnum.LOWER:
            return f"{base}{quote}".lower()
        elif to_format is SymbolFormatEnum.UPPER:
            return f"{base}{quote}".upper()
        elif to_format is SymbolFormatEnum.LOWER_UNDERSCORE:
            return f"{base}_{quote}".lower()
        elif to_format is SymbolFormatEnum.UPPER_UNDERSCORE:
            return f"{base}_{quote}".upper()

    elif from_format is SymbolFormatEnum.LOWER or from_format is SymbolFormatEnum.UPPER:
        if to_format is SymbolFormatEnum.LOWER:
            return s.lower()
        elif to_format is SymbolFormatEnum.UPPER:
            return s.upper()
        # it's unknown how many chars are there for quote currency
        # try all 3 possibilities
        quote = None
        for _quote in ['btc', 'eth', 'usdt']:
            if s.lower().endswith(_quote):
                quote = _quote
                break

        if quote is not None:
            base = s[:len(s) - len(quote)]

            if to_format is SymbolFormatEnum.LOWER_UNDERSCORE:
                return f"{base}_{quote}".lower()
            elif to_format is SymbolFormatEnum.UPPER_UNDERSCORE:
                return f"{base}_{quote}".upper()
            elif to_format is SymbolFormatEnum.LOWER_HYPHEN:
                return f"{base}_{quote}".lower()
            elif to_format is SymbolFormatEnum.UPPER_HYPHEN:
                return f"{base}_{quote}".upper()
        else:
            return s


def ts_to_dt(ts):
    tz = timezone.get_default_timezone()

    dt = datetime.fromtimestamp(ts)
    dt = timezone.make_aware(dt, tz)
    return dt


def dt_str_to_dt(s):
    return arrow.get(s).datetime
