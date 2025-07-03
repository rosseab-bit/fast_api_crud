from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from auth import verificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    email = verificar_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Token inválido")
    return email
