import os

os.environ.setdefault(
    "CLERK_JWKS_URL",
    "https://example.clerk.accounts.dev/.well-known/jwks.json",
)
os.environ.setdefault("OPENROUTER_API_KEY", "test-key")
