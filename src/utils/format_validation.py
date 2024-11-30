import logging

from pydantic import ValidationError

logger = logging.getLogger('agent_logger')


def format_validation_error(error: ValidationError):
    """Extract and format validation errors for a beautiful output."""
    for err in error.errors():
        loc = " → ".join(map(str, err['loc']))  # Location of the error
        msg = err['msg']  # Error message
        ctx = err.get('ctx', {})  # Additional context if available
        expected = ctx.get('expected', 'N/A')  # Expected value from context
        logging.error(
            f"\nLocation: {loc}\n"
            f"Message: {msg}\n"
            f"Expected: {expected}\n"
        )
