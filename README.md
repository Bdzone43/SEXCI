# Sexcie - Credit Card Checker Bot

![Python](https://img.shields.io/badge/Python-3.6%2B-blue)
![Luhn Algorithm](https://img.shields.io/badge/Luhn-Algorithm-green)
![Secure](https://img.shields.io/badge/Security-High-important)
![Stripe Ready](https://img.shields.io/badge/Integration-Stripe-blueviolet)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow)

Sexcie is a Python-based credit card checker bot that validates credit card numbers using the Luhn algorithm. It is designed to help users verify the validity of credit card numbers for educational or testing purposes.

---

## Features

- **Luhn Algorithm Implementation**: Uses the Luhn algorithm to validate credit card numbers.
- **Easy to Use**: Simple command-line interface.
- **Customizable**: Easily extendable for additional validation checks.
- **Secure**: Does not store or misuse sensitive data.

---

## Prerequisites

Before running Sexcie, ensure you have the following installed:

- Python 3.6 or higher

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/sexcie.git
   ```

2. Navigate to the project directory:
   ```bash
   cd sexcie
   ```

3. Install any required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. Run the bot:
   ```bash
   python sexcie.py
   ```

2. Enter a credit card number when prompted.

3. The bot will validate the number and display the result (e.g., valid or invalid).

---

## Example

```bash
$ python sexcie.py
Enter credit card number: 4111111111111111
Valid credit card number.

$ python sexcie.py
Enter credit card number: 1234567890123456
Invalid credit card number.
```

---

## Code Overview

### Main Script

The `sexcie.py` script contains:

- Input handling for credit card numbers.
- Implementation of the Luhn algorithm.
- Validation result output.

### Key Function

```python
def luhn_check(card_number):
    total = 0
    reverse_digits = card_number[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0
```

---

## Contributing

Contributions are welcome! Feel free to submit a pull request or report issues.

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## License

Sexcie is licensed under the [MIT License](LICENSE).

---

## Disclaimer

This tool is for educational and testing purposes only. Do not use it for illegal or unethical activities.

