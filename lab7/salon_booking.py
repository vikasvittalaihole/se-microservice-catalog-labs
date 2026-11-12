import math

def _require_str(value, name):
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string, got {type(value).__name__}")
    return value

def _parse_finite(text, name):
    try:
        number = float(text)
    except ValueError:
        raise ValueError(f"{name} must be a number, got {text!r}") from None
    if not math.isfinite(number):
        raise ValueError(f"{name} must be a finite number, got {text!r}")
    return number

def parse_booking(text):
    text = _require_str(text, "booking")
    parts = text.split(':')
    if len(parts) != 2:
        raise ValueError("booking must look like 'service:minutes'")
    service, minutes = parts[0].strip(), _parse_finite(parts[1], "duration")
    if not service:
        raise ValueError("service name cannot be empty")
    if minutes < 0:
        raise ValueError("duration cannot be negative")
    return service.title(), minutes

def duration_average(durations_csv):
    durations_csv = _require_str(durations_csv, "durations")
    values = []
    for item in durations_csv.split(','):
        try:
            values.append(int(item))
        except ValueError:
            raise ValueError(f"duration must be an integer, got {item!r}") from None
    if not values:
        raise ValueError("at least one duration is required")
    if any(v < 0 for v in values):
        raise ValueError("durations cannot be negative")
    return sum(values) // len(values)

def payable_bill(text):
    text = _require_str(text, "bill")
    parts = text.split('|')
    if len(parts) != 2:
        raise ValueError("bill must look like 'amount|discount'")
    bill = _parse_finite(parts[0], "bill")
    discount = _parse_finite(parts[1], "discount")
    if bill < 0 or discount < 0:
        raise ValueError("bill and discount cannot be negative")
    total = bill * 1.18 - discount
    return max(total, 0)

def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter service:duration in min (e.g. haircut:45): ")
    result = parse_booking(user_input)
    print("Service and Duration:", result)

    print("\n==== Running duration_average ====")
    user_input = input("Enter durations as CSV (e.g. 30,45,60): ")
    result = duration_average(user_input)
    print("Average Duration:", result)

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 800|100): ")
    result = payable_bill(user_input)
    print("Payable Bill:", result)

if __name__ == "__main__":
    main()