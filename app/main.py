from fastapi import FastAPI

from app.api.routes.api import router


tags_metadata = [
	{
		"name": "authentication",
		"description": "Авторизация и аутентификация",
	},
	{
		"name": "operations",
		"description": "Работа с операциями",
	},
	{
		"name": "reports",
		"description": "Отчеты в csv формате",
	},
]


def get_application() -> FastAPI:
	application = FastAPI(
		title="Income/outcome manager",
		description="Сервис учета расходов и доходов",
		version="1.0.0",
		openapi_tags=tags_metadata,
	)
	application.include_router(router)
	return application


app = get_application()
