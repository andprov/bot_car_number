from bot_car_number.value_objects.auto_model import AutoModel


class AddAutoModel:
    async def __call__(self, model: str) -> str:
        auto_model = AutoModel(value=model)
        return auto_model.value
