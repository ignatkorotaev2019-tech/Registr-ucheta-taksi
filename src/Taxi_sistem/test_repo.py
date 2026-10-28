from repositories import role_repository

print(role_repository.get_all())
print(role_repository.get_by_id(1))
print(role_repository.get_by_id(99))