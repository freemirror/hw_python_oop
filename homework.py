from typing import Dict, List, Tuple
from training_generator import packages

class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: int,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Формирование сообщения о тренировке."""
        return (f'Тип тренировки: {self.training_type}; Длительность:'
                f' {self.duration:.3f} ч.; Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    M_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: int,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_CAL_RUN: int = 18
    COEFF_CAL_RUN_MIN: int = 20

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CAL_RUN * self.get_mean_speed()
                - self.COEFF_CAL_RUN_MIN) * self.weight / self.M_IN_KM
                * self.duration * self.M_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CAL_WALK: float = 0.035
    COEFF_CAL_WALK_AVE: float = 0.029
    SQUARE_POW: int = 2

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: int,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.COEFF_CAL_WALK * self.weight
                + ((self.get_mean_speed() ** self.SQUARE_POW) // self.height)
                * self.COEFF_CAL_WALK_AVE * self.weight)
                * self.duration * self.M_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_CAL_SWM: float = 1.1
    COEFF_CAL_SWM_WGH: int = 2

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: int,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEFF_CAL_SWM)
                * self.COEFF_CAL_SWM_WGH * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict: Dict = {'SWM': Swimming,
                               'RUN': Running,
                               'WLK': SportsWalking}
    if workout_type in workout_type_dict:
        return workout_type_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    message: InfoMessage = training.show_training_info()
    print(message.get_message())


if __name__ == '__main__':
    '''packages: List[Tuple[str, List[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]'''

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
