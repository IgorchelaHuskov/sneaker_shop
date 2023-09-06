"""Класс Result представляет результат операции."""

class Result:
    """Предоставить результат операции."""

    def __init__(self, success, value, error):
        self.succes = success
        self.value = value
        self.error = error


    def __str__(self) -> str:
        """Неформальное строковое представление результата"""
        if self.succes:
            return "[Success]"
        else:
            return f"[Failure] {self.error}"
        

    def __repr__(self) -> str:
        """Официальное строковое представление результата"""
        if self.succes:
            return f"<Result success={self.succes}>"
        else:
            return f"<Result success={self.succes}, mesage={self.error}>"
        

    @property
    def failure(self):
        """Флаг, указывающий, что операция не удалась."""
        return not self.succes
    

    def on_success(self, func, *args, **kwargs):
        """Передача сообщения об ошибке из неудачной операции в последующую функцию."""
        if self.succes:
            return self.value if self.value else None
        if self.error:
            return func(self.error, *args, **kwargs)
        return func(*args, **kwargs)
    

    def on_both(self, func, *args, **kwargs):
        """Передать результат (успешно/неуспешно) в последующую функцию.""" 
        if self.value:
            return func(self.value, *args, **kwargs)
        return func(*args, **kwargs)
    

    @staticmethod
    def Fail(error_message):
        """Создать объект Result для неудачной операции.""" 
        return Result(False, value=None, error=error_message)
    

    @staticmethod
    def Ok(value=None):
        """Создать объект Result для успешной операции.""" 
        return Result(True, value=value, error=None)
    

    @staticmethod
    def Combine(results):
        """Вернуть объект Result на основе результатов списка результатов.""" 
        if all(result.succes for result in results):
            return Result.Ok()
        errors = [result.error for result in results if result.failure]
        return Result.Fail("\n".join(errors))
    
