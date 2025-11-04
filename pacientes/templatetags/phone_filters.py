import re

from django import template

register = template.Library()


@register.filter(name="phone_mask")
def phone_mask(value):
    """Format a phone number to (xx) xxxxx-xxxx or (xx) xxxx-xxxx.

    The function strips all non-digit characters and then applies a
    Brazilian-style mask depending on length (11 -> 5+4, 10 -> 4+4).
    For other lengths it returns the original value unchanged.
    """
    if value is None:
        return ""

    s = re.sub(r"\D", "", str(value))
    if len(s) == 11:
        # (AA) NNNNN-NNNN
        return f"({s[0:2]}) {s[2:7]}-{s[7:11]}"
    if len(s) == 10:
        # (AA) NNNN-NNNN
        return f"({s[0:2]}) {s[2:6]}-{s[6:10]}"
    # If value seems to include country code like 5511XXXX..., try to remove leading '55'
    if len(s) == 13 and s.startswith("55"):
        s2 = s[2:]
        if len(s2) == 11:
            return f"({s2[0:2]}) {s2[2:7]}-{s2[7:11]}"

    # Fallback: return original (unmodified) value so templates can show whatever was stored
    return value
