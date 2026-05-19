from fastapi import Depends, HTTPException, status, Request
from jose import jwt, JWTError
import requests
import os
from typing import Optional, Dict
from functools import lru_cache
from datetime import datetime

SUPABASE_PROJECT_ID = "niifawzdamlgbwlhwmbg"
SUPABASE_JWKS_URL = f"https://{SUPABASE_PROJECT_ID}.supabase.co/auth/v1/.well-known/jwks.json"
SUPABASE_AUDIENCE = os.environ.get("SUPABASE_AUDIENCE", SUPABASE_PROJECT_ID)
SUPABASE_ISSUER = f"https://{SUPABASE_PROJECT_ID}.supabase.co/auth/v1"

@lru_cache
def get_jwks():
    resp = requests.get(SUPABASE_JWKS_URL, timeout=5)
    resp.raise_for_status()
    return resp.json()['keys']

def get_bearer_token(request: Request) -> str:
    auth: str = request.headers.get('authorization', '')
    parts = auth.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")

def get_public_key(token: str) -> Optional[str]:
    # Parse JWT header for key id
    from jose.utils import base64url_decode
    import json
    headers = jwt.get_unverified_header(token)
    jwks = get_jwks()
    key = next((k for k in jwks if k['kid'] == headers['kid']), None)
    if not key:
        return None
    return jwt.construct_rsa_public_key(key)

def decode_supabase_jwt(token: str) -> Dict:
    """Verify the JWT from Supabase and return the claims dict, or raise HTTPException."""
    from jose.exceptions import ExpiredSignatureError

    key = get_public_key(token)
    if not key:
        raise HTTPException(status_code=401, detail="Invalid Supabase token—key not found")
    try:
        # Audience (aud) can be project id or custom, verify as needed
        claims = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=SUPABASE_AUDIENCE,
            issuer=SUPABASE_ISSUER,
        )
        # Optionally check additional claims here
        exp = claims.get('exp')
        if exp and datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Supabase JWT expired")
        return claims
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Supabase JWT expired")
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Supabase JWT invalid: {str(e)}")

def get_current_user(request: Request) -> dict:
    token = get_bearer_token(request)
    claims = decode_supabase_jwt(token)
    return {
        "id": claims.get("sub"),
        "email": claims.get("email"),
        "claims": claims,
    }