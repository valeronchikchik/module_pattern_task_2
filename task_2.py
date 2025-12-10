import random
from typing import Optional, Dict, List

#Базовий клас обробника

class Handler:
    def __init__(self, next_handler: Optional['Handler'] = None) -> None:
        self.next: Optional[Handler] = next_handler

    def handle(self, request: Dict[str, object]) -> str:
        if self.next:
            return self.next.handle(request)
        return "Обробку завершено."


# 1. Перевірка спеціальності та курсу

class CheckSpecialtyAndCourse(Handler):
    def handle(self, request: Dict[str, object]) -> str:
        specialty: int = request.get("specialty", -1)
        course: int = request.get("course", -1)

        if specialty != 124 or course != 2:
            return "Доступ заборонено: лише 2 курс, спеціальність 124."
        return super().handle(request)


#2. Перевірка прізвища

class CheckSurname(Handler):
    def __init__(self, allowed_list: List[str], next_handler: Optional[Handler] = None) -> None:
        super().__init__(next_handler)
        self.allowed: List[str] = allowed_list

    def handle(self, request: Dict[str, object]) -> str:
        surname: str = request.get("surname", "")

        if surname not in self.allowed:
            return "Доступ заборонено: студент не у списку допущених."
        return super().handle(request)


# 3. Призначення білету

class AssignTicket(Handler):
    def handle(self, request: Dict[str, object]) -> str:
        ticket: int = random.randint(1, 20)
        return f"Доступ дозволено. Ваш білет: №{ticket}"


# Використання системи

if __name__ == "__main__":
    allowed_students: List[str] = ["Брич", "Вакі", "Цанько"]

    # Формуємо ланцюг
    chain: Handler = CheckSpecialtyAndCourse(
        CheckSurname(
            allowed_students,
            AssignTicket()
        )
    )

    # Приклад запиту
    student: Dict[str, object] = {
        "course": 2,
        "specialty": 124,
        "surname": "Цанько"
    }

    result: str = chain.handle(student)
    print(result)
