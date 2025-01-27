from dishka.integrations.aiogram import wrap_injection


def aiogram_middleware_inject(func):
    return wrap_injection(
        func=func,
        is_async=True,
        container_getter=lambda args, kwargs: args[3]["dishka_container"],
    )
