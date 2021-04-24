from prettyconf import config


class Settings:
    GITHUB_API_KEY = config("GITHUB_API_KEY")


settings = Settings()
