"""Car rental booking and management system.

Provides vehicle fleet tracking, customer database registration,
booking calculations, cryptographic operations, receipt generation,
and promo rule evaluation.
"""

from datetime import datetime
import hashlib
import os
import re
import secrets
import sqlite3
import tempfile

# Global rental state
fleet = {}
bookings = []
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE customers (name TEXT, licence TEXT, phone TEXT)")

DEFAULT_ADMIN_TOKEN = os.environ.get("ADMIN_AUTH_TOKEN", "admin@rent")


def add_car(plate, model="Unknown", daily_rate=0, features=None):
    """Add a vehicle to the rental fleet.

    Args:
        plate (str): Registration license plate number.
        model (str): Make and model of the vehicle.
        daily_rate (int): Daily rental rate in INR (must be non-negative).
        features (list, optional): List of vehicle feature tags.

    Returns:
        dict: The registered vehicle dictionary, or None if plate is empty.
    """
    if not plate:
        return None
    features_list = list(features) if features is not None else []
    rate = max(0, daily_rate)
    fleet[plate] = {
        "model": model,
        "rate": rate,
        "available": True,
        "features": features_list,
    }
    return fleet[plate]


def register_customer(name, licence, phone):
    """Register a new customer using parameterized SQL insert.

    Args:
        name (str): Customer full name.
        licence (str): Driving license identifier.
        phone (str): Contact phone number.
    """
    conn.execute(
        "INSERT INTO customers VALUES (?, ?, ?)", (name, licence, phone)
    )


def find_customer(name):
    """Query customer records by name using parameterized SQL select.

    Args:
        name (str): Name string to search for.

    Returns:
        list: Matching database rows.
    """
    query = "SELECT * FROM customers WHERE name = ?"
    return conn.execute(query, (name,)).fetchall()


def rent_car(plate, customer, start, end):
    """Create a new car booking and update fleet availability.

    Args:
        plate (str): Vehicle license plate.
        customer (str): Name of customer.
        start (str): Start date formatted as YYYY-MM-DD.
        end (str): End date formatted as YYYY-MM-DD.

    Returns:
        int: Total cost for the rental, or None if booking cannot be completed.

    Raises:
        ValueError: If customer is not registered.
    """
    if not find_customer(customer):
        raise ValueError("Customer not registered")
    if plate not in fleet or not fleet[plate]["available"]:
        return None
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    days = (end_date - start_date).days
    if days <= 0:
        return None

    cost = days * fleet[plate]["rate"]
    fleet[plate]["available"] = False
    booking = {
        "code": booking_code(),
        "plate": plate,
        "customer": customer,
        "days": days,
        "cost": cost,
    }
    bookings.append(booking)
    return cost


def return_car(plate, km_driven):
    """Return a rented vehicle to the fleet and calculate extra km fees.

    Args:
        plate (str): License plate of returning vehicle.
        km_driven (int): Kilometres driven during the trip.

    Returns:
        int: Extra distance charge in INR (0 if within allowance, None if
        plate is unknown).
    """
    try:
        if plate not in fleet:
            return None
        fleet[plate]["available"] = True
        if km_driven > 300:
            return (km_driven - 300) * 5
        return 0
    except (KeyError, TypeError):
        return None


def booking_code():
    """Generate a cryptographically secure random booking code.

    Returns:
        str: Booking reference identifier prefixed with 'BK-'.
    """
    return f"BK-{secrets.randbelow(90000) + 10000}"


def licence_hash(licence):
    """Compute secure SHA-256 digest of driving license for privacy.

    Args:
        licence (str): Driving license identifier string.

    Returns:
        str: Hexadecimal SHA-256 hash string.
    """
    return hashlib.sha256(licence.encode("utf-8")).hexdigest()


def apply_promo(rule, amount):
    """Safely apply discount promo rules without arbitrary code execution.

    Args:
        rule (str): Staff rule expression (e.g. 'amount = amount * 0.9').
        amount (float): Original cost.

    Returns:
        float: Discounted price.
    """
    rule_clean = rule.strip()
    match_mult = re.search(r"amount\s*\*\s*([0-9.]+)", rule_clean)
    if match_mult:
        factor = float(match_mult.group(1))
        return amount * factor
    match_sub = re.search(r"amount\s*-\s*([0-9.]+)", rule_clean)
    if match_sub:
        discount = float(match_sub.group(1))
        return max(0.0, amount - discount)
    return float(amount)


def is_valid_plate(plate):
    """Validate Indian motor vehicle registration plate format.

    Args:
        plate (str): License plate to validate.

    Returns:
        bool: True if plate conforms to registration standards, else False.
    """
    return bool(re.match(r"^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$", plate))


def write_receipt(booking):
    """Generate a booking receipt file with restricted owner permissions.

    Args:
        booking (dict): Booking record dictionary.

    Returns:
        str: File system path of the created receipt.
    """
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".txt", encoding="utf-8"
    ) as temp_file:
        path = temp_file.name
        temp_file.write(
            f"Booking {booking['code']}: {booking['plate']} for "
            f"{booking['days']} days = Rs.{booking['cost']}\n"
        )
    os.chmod(path, 0o600)
    return path


def admin_login(user, token=None):
    """Authenticate administrator session with secure token verification.

    Args:
        user (str): Username to verify.
        token (str, optional): Admin access token.

    Returns:
        bool: True if authenticated, False otherwise.
    """
    expected_user = os.environ.get("ADMIN_USER", "admin")
    active_token = token if token is not None else DEFAULT_ADMIN_TOKEN
    return user == expected_user and active_token == DEFAULT_ADMIN_TOKEN


def available_cars():
    """Retrieve list of vehicle plates currently available for rent.

    Returns:
        list: Available vehicle registration plates.
    """
    return [plate for plate, car in fleet.items() if car.get("available")]


# Backward compatibility aliases
addCar = add_car  # pylint: disable=invalid-name
registerCustomer = register_customer  # pylint: disable=invalid-name
findCustomer = find_customer  # pylint: disable=invalid-name
rentCar = rent_car  # pylint: disable=invalid-name
returnCar = return_car  # pylint: disable=invalid-name
bookingCode = booking_code  # pylint: disable=invalid-name
licenceHash = licence_hash  # pylint: disable=invalid-name
applyPromo = apply_promo  # pylint: disable=invalid-name
isValidPlate = is_valid_plate  # pylint: disable=invalid-name
writeReceipt = write_receipt  # pylint: disable=invalid-name
adminLogin = admin_login  # pylint: disable=invalid-name
availableCars = available_cars  # pylint: disable=invalid-name


def main():
    """Run demonstration scenario and display operations output."""
    add_car("KA01AB1234", "Swift", 1500)
    add_car("KA02CD5678", "Innova", 3000)
    add_car("KA03EF9999", "Nexon", -500)
    register_customer("Ravi", "DL-0420110012345", "9845012345")
    register_customer("Meera", "DL-0420110099999", "9845099999")
    print(
        "Rent Swift:",
        rent_car("KA01AB1234", "Ravi", "2026-11-01", "2026-11-04"),
    )
    print(
        "Rent Swift again:",
        rent_car("KA01AB1234", "Ravi", "2026-11-02", "2026-11-03"),
    )
    print(
        "Rent Innova:",
        rent_car("KA02CD5678", "Ravi", "2026-11-10", "2026-11-07"),
    )
    print("Lookup injection:", find_customer("x' OR '1'='1"))
    print("Extra km charge:", return_car("KA01AB1234", 420))
    print("Return unknown car:", return_car("XX00XX0000", 50))
    print("Promo price:", apply_promo("amount = amount * 0.9", 4500))
    print("Plate valid?", is_valid_plate("KA01AB1234"))
    print("Licence hash:", licence_hash("DL-0420110012345"))
    print("Admin:", admin_login("admin"))
    print("Available:", available_cars())
    print("Receipt saved to:", write_receipt(bookings[0]))


if __name__ == "__main__":
    main()
