from typing import Dict, List, Tuple


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

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: int,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self,
                     LEN_STEP=LEN_STEP,
                     M_IN_KM=M_IN_KM) -> float:
        """Получить дистанцию в км."""
        return self.action * LEN_STEP / M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance: float = self.get_distance()
        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        M_IN_KM = super().M_IN_KM
        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        min_in_hour: int = 60
        mean_speed: float = self.get_mean_speed()
        return ((coeff_calorie_1 * mean_speed - coeff_calorie_2)
                * self.weight / M_IN_KM * self.duration
                * min_in_hour)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: int,
                 weight: int,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coeff_calorie_1: float = 0.035
        coeff_calorie_2: float = 0.029
        min_in_hour: int = 60
        mean_speed: float = self.get_mean_speed()
        return ((coeff_calorie_1 * self.weight
                + ((mean_speed ** 2) // self.height)
                * coeff_calorie_2 * self.weight)
                * self.duration * min_in_hour)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

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
        M_IN_KM: int = super().M_IN_KM
        return (self.length_pool * self.count_pool
                / M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        coeff_calorie_1: float = 1.1
        coeff_calorie_2: int = 2
        mean_speed: float = self.get_mean_speed()
        return ((mean_speed + coeff_calorie_1) * coeff_calorie_2
                * self.weight)

    def show_training_info(self, LEN_STEP=LEN_STEP) -> InfoMessage:
        distance = self.get_distance(LEN_STEP)
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(training_type=self.__class__.__name__,
                           duration=self.duration,
                           distance=distance,
                           speed=speed,
                           calories=calories)


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
    packages: List[Tuple[str, List[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
