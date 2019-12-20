from datetime import datetime

from django.utils import timezone

from enums.symbol import SymbolFormatEnum


# def build_symbol_string(s: Symbol, fmt: SymbolFormatEnum):
#     if fmt is SymbolFormatEnum.UPPER_UNDERSCORE:
#         return "_".join([s.base.name, s.quote.name])
# elif


def symbol_format_convert(s, from_format: SymbolFormatEnum, to_format: SymbolFormatEnum):
    if from_format is SymbolFormatEnum.UPPER_UNDERSCORE and to_format is SymbolFormatEnum.LOWER:
        return ''.join(s.split('_')).lower()
    elif (from_format is SymbolFormatEnum.LOWER and
          to_format in [SymbolFormatEnum.LOWER_UNDERSCORE, SymbolFormatEnum.UPPER_UNDERSCORE]):
        # it's unknown how many chars are there for quote currency
        # try all 3 possibilities
        base = None
        for cur_base in ['btc', 'eth', 'usdt']:
            if s.endswith(cur_base):
                base = cur_base
                break
        if base is not None:
            result = s[:len(s) - len(base)] + '_' + base
            return result if to_format is SymbolFormatEnum.LOWER_UNDERSCORE else result.upper()
        else:
            return s


def ts_to_dt(ts):
    tz = timezone.get_default_timezone()

    dt = datetime.fromtimestamp(ts)
    dt = timezone.make_aware(dt, tz)
    return dt
