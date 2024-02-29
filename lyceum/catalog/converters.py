class MyConverter:
    regex = r"[1-9]\d*"

    def to_python(self, value) -> int:
        return int(value)

    def to_url(self, value) -> str:
        return f"{value}"


__all__ = [
    MyConverter,
]
