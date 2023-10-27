def normalize_phone(phone: str) -> str:
    phone = "".join(x for x in phone if x.isdecimal())
    phone = phone.removeprefix("8")
    if phone.startswith("7") and len(phone) == 11:
        phone = phone.removeprefix("7")
    return "7" + phone
