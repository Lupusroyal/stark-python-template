from stark.core.security import hash_password, verify_password

senha = "123456"

hash_senha = hash_password(senha)

print("Hash:", hash_senha)
print("Senha correta:", verify_password(senha, hash_senha))
print("Senha errada:", verify_password("abcdef", hash_senha))
