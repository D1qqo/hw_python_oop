class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Возврат строки сообщения."""
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000  # Количество метров в километре
    LEN_STEP: float = 0.65  # Длина шага в метрах
    HOUR: int = 60  # Количесвто минут в часе

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        end_distance = self.action * self.LEN_STEP / self.M_IN_KM
        return end_distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Требуется определить get_spent_calories()')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    mean_spead_multiplier: int = 18  # Множитель средней скорости
    mean_speed_shift: float = 1.79  # Сдвиг средней скорости

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий во время бега."""
        return ((self.mean_spead_multiplier * self.get_mean_speed()
                 + self.mean_speed_shift)
                * self.weight / self.M_IN_KM * self.duration * self.HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    weight_multiplier: float = 0.035  # Множитель веса
    mean_speed_height_multiplier: float = 0.029
    # Множитель корректировки частного квадрата средней скорости на рост
    m_s_mean_speed_multiplier: float = 0.278
    # Множитель сердней скорости для перевода в м/с
    mean_speed_multiplier: int = 2  # Множитель средней скорости
    height_multiplier: int = 100  # Множитель перевода роста в метры

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """
        Получить количество затраченных калорий
        во время спортивной ходьбы.
        """
        return ((self.weight_multiplier * self.weight
                + ((self.get_mean_speed()
                    * self.m_s_mean_speed_multiplier)
                   ** self.mean_speed_multiplier
                   / (self.height / self.height_multiplier))
                * self.mean_speed_height_multiplier * self.weight)
                * self.duration * self.HOUR)


class Swimming(Training):
    """Тренировка: плавание."""

    mean_speed_shift: float = 1.1  # Сдвиг средней скорости
    weight_multiplier: int = 2  # Множитель веса
    LEN_STEP: float = 1.38  # Расстояние одного гребка

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плавания."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий во время плавания."""
        return ((Swimming.get_mean_speed(self) + self.mean_speed_shift)
                * self.weight_multiplier * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in workout:
        return workout[workout_type](*data)
    else:
        print(f'Данные о тренировке "{workout_type}" не найдены')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
