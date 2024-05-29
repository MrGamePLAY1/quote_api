from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from main.py import get_current_user
from main.py import role_permission

def check_permissions(permission: str):
    def pm_checker(user: dict = Depends(get_current_user)):
        user_roles = user['roles']
        user_permissions = set()
        for role in user_roles:
            user_permissions.update(role_permission.get(role, []))
        if permission not in user_permissions:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return pm_checker
        