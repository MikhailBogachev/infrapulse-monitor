"""Check pinned runtime compatibility and synthetic crypto/Redis operations."""

import platform
import ssl
from importlib.metadata import version

import jwt
from argon2 import PasswordHasher
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from infrapulse.config import Settings
from psycopg import pq
from redis import Redis

settings = Settings.load()
print(platform.platform(), platform.python_version(), ssl.OPENSSL_VERSION)
assert ssl.create_default_context().cert_store_stats()["x509_ca"] > 0
for package in ("fastapi", "sqlalchemy", "psycopg", "alembic", "celery", "httpx", "redis"):
    print(f"{package}=={version(package)}")
assert pq.__impl__ == "binary"
print(f"libpq={pq.version()}")
fixture = b"synthetic marker"
encoded = jwt.encode({"sub": "fixture"}, fixture.ljust(32, b"x"), algorithm="HS256")
assert jwt.decode(encoded, fixture.ljust(32, b"x"), algorithms=["HS256"])["sub"] == "fixture"
hasher = PasswordHasher()
assert hasher.verify(hasher.hash("fixture"), "fixture")
cipher = AESGCM(AESGCM.generate_key(bit_length=256))
nonce = b"fixture-noce"
assert cipher.decrypt(nonce, cipher.encrypt(nonce, fixture, b"context"), b"context") == fixture
with Redis.from_url(settings.redis_url, socket_timeout=2, socket_connect_timeout=2) as cache:
    assert (
        cache.eval(
            "local n=redis.call('INCR',KEYS[1]); redis.call('PEXPIRE',KEYS[1],1000); return n",
            1,
            "ip007:compatibility",
        )
        >= 1
    )
print("Redis atomic command and JWT, Argon2id, AES-GCM fixture round trips passed")
