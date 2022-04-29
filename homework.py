from dataclasses import dataclass, asdict
from typing import Type, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке. """
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    INFO: str = ('Тип тренировки: {training_type}; '
                 'Длительность: {duration:.3f} ч.; '
                 'Дистанция: {distance:.3f} км; '
                 'Ср. скорость: {speed:.3f} км/ч; '
                 'Потрачено ккал: {calories:.3f}.')

    def get_message(self):
        """Метод, который возвращает строку сообщения
         о проделанной тренировке. """
        return self.INFO.format(**asdict(self))

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories


class Training:
    """Базовый класс тренировки. """
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_HOUR: float = 60
    action: int
    duration: float
    weight: float

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км. """
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения. """
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий. """
    pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке. """
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_RUNNING_CALORIES: int = 18
    SWIMMING_SPEED_INCREMENT: int = 20

    def get_spent_calories(self) -> float:
        """Формула для расчёта израсходованных калорий при беге. """
        return ((self.COEFF_RUNNING_CALORIES * self.get_mean_speed()
                 - self.SWIMMING_SPEED_INCREMENT)
                * self.weight / self.M_IN_KM * self.duration
                * self.MIN_IN_HOUR)
# (18 * средняя_скорость - 20) * вес_спортсмена
# / M_IN_KM * время_тренировки_в_минутах


class SportsWalking(Training):
    """Тренировка: спортивная ходьба. """
    coeff_walking_calories_1: float = 0.035
    coeff_walking_calories_2: float = 0.029
    height: float
    in_min: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Формула для расчёта израсходованных калорий
        при спортивной ходьбе. """
        return ((self.coeff_walking_calories_1
                * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.coeff_walking_calories_2 * self.weight)
                * self.duration * self.MIN_IN_HOUR)
# (0.035 * вес + (средняя_скорость**2 // рост) * 0.029 * вес)
# * время_тренировки_в_минутах


class Swimming(Training):
    """Тренировка: плавание. """
    LEN_STEP: float = 1.38
    coeff_swim_calorie_1: float = 1.1
    coeff_swim_calorie_2: int = 2
    length_pool: float
    count_pool: float

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        """Формула расчёта средней скорости при плавании. """
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)
# (средняя_скорость + 1.1) * 2 * вес

    def get_spent_calories(self):
        """Формула для расчёта израсходованных калорий при плавании. """
        return ((self.get_mean_speed() + self.coeff_swim_calorie_1)
                * self.coeff_swim_calorie_2 * self.weight)
# длина_бассейна * count_pool / M_IN_KM / время_тренировки

    def get_distance(self):
        """Формула рассчета дистанции км. при плавании. """
        return self.action * self.LEN_STEP / self.M_IN_KM


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков. """
    packages: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in packages:
        raise KeyError(f'Неизвестная тренировка: {workout_type}')

    return packages[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция. """
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
