import os
import json
import pytest
import allure
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

from tests.utils.data_loader import load_json
from tests.utils.logger import setup_logger

logger = setup_logger(__name__)


# Добавляем ТОЛЬКО не конфликтующий с pytest-playwright флаг
def pytest_addoption(parser):
    parser.addoption("--har", action="store_true", help="Record HAR (network.har)")


def _get_opt(config, name, default):
    """Безопасно читаем опции pytest-playwright. Если опции нет — возвращаем default."""
    try:
        val = config.getoption(name)
        return val if val is not None else default
    except Exception:
        return default


@pytest.fixture(scope="session")
def config():
    return load_json("tests/data/config.json")


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser_context_factory(request, playwright_instance):
    # Читаем флаги плагина pytest-playwright (не объявляем их сами)
    headed       = bool(_get_opt(request.config, "--headed", False))
    browser_opt  =       _get_opt(request.config, "--browser", "chromium")
    tracing_mode =       _get_opt(request.config, "--tracing", "off")      # on|off|retain-on-failure
    video_mode   =       _get_opt(request.config, "--video", "off")        # on|off|retain-on-failure
    do_trace     = tracing_mode in ("on", "retain-on-failure")
    do_video     = video_mode   in ("on", "retain-on-failure")
    do_har       = bool(_get_opt(request.config, "--har", False))          # наш флаг

    # В CI всегда headless
    if os.getenv("CI", "").lower() == "true":
        headed = False

    # Нормализация имени браузера
    if isinstance(browser_opt, (list, tuple)):
        candidates = [str(x).strip().lower() for x in browser_opt if x]
        browser_name = candidates[0] if candidates else "chromium"
    else:
        browser_name = str(browser_opt).strip().lower()

    if browser_name in ("all", "any", ""):
        browser_name = "chromium"
    if browser_name not in ("chromium", "firefox", "webkit"):
        logger.warning(f"Unknown --browser={browser_name}, fallback to chromium")
        browser_name = "chromium"

    browser = getattr(playwright_instance, browser_name).launch(headless=not headed)

    artifacts_dir = Path("reports/artifacts")
    (artifacts_dir / "videos").mkdir(parents=True, exist_ok=True)

    def _factory():
        ctx_kwargs = {}
        if do_video:
            ctx_kwargs["record_video_dir"] = str(artifacts_dir / "videos")
        if do_har:
            ctx_kwargs["record_har_path"] = str(artifacts_dir / "network.har")

        context = browser.new_context(**ctx_kwargs)
        context._trace_started = False  # type: ignore[attr-defined]

        if do_trace:
            context.tracing.start(screenshots=True, snapshots=True, sources=True)
            context._trace_started = True  # type: ignore[attr-defined]

        return context

    yield _factory
    browser.close()


@pytest.fixture(scope="function")
def page(browser_context_factory, request, config):
    context = browser_context_factory()
    page = context.new_page()

    # Таймауты из config.json
    action_ms = config.get("timeouts", {}).get("action_ms", 10000)
    nav_ms    = config.get("timeouts", {}).get("navigation_ms", 45000)

    page.set_default_timeout(action_ms)
    page.set_default_navigation_timeout(nav_ms)

    # Агрегируем логи консоли страницы
    console_buf = []

    def _on_console(msg):
        try:
            console_buf.append(f"{msg.type.upper()}: {msg.text}")
        except Exception:
            pass

    page.on("console", _on_console)

    yield page

    # Узнаём исход теста (для вложений)
    outcome = getattr(request.node, "rep_call", None)
    failed = False
    try:
        failed = outcome.failed if outcome else False
    except Exception:
        failed = False

    if failed:
        # Скриншот, исходник страницы, консольные логи
        try:
            allure.attach(page.screenshot(), name="screenshot", attachment_type=allure.attachment_type.PNG)
        except Exception:
            pass
        try:
            allure.attach(page.content(), name="page_source", attachment_type=allure.attachment_type.HTML)
        except Exception:
            pass
        if console_buf:
            try:
                allure.attach("\n".join(console_buf), name="console.log", attachment_type=allure.attachment_type.TEXT)
            except Exception:
                pass

    # Останавливаем трейс, если он был запущен
    try:
        if getattr(context, "_trace_started", False):  # type: ignore[attr-defined]
            artifacts_dir = Path("reports/artifacts")
            artifacts_dir.mkdir(parents=True, exist_ok=True)
            safe_name = request.node.nodeid.replace("/", "_").replace("::", "__")
            trace_path = artifacts_dir / f"trace__{safe_name}.zip"
            context.tracing.stop(path=str(trace_path))
            allure.attach.file(str(trace_path), name="trace.zip", attachment_type=allure.attachment_type.ZIP)
    except Exception:
        pass

    page.close()
    context.close()


# Хук, чтобы знать фазу и статус теста в фикстуре page
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="session")
def api_request_context(playwright_instance, config):
    # Общий request-контекст Playwright для API-тестов (если вдруг понадобится)
    ctx = playwright_instance.request.new_context(base_url=config["base_url"])
    yield ctx
    ctx.dispose()


# --- Allure environment & categories (автоматически добавляем в отчет) ---
@pytest.fixture(scope="session", autouse=True)
def allure_environment(config):
    out_dir = Path("reports/allure-results")
    out_dir.mkdir(parents=True, exist_ok=True)

    env_lines = [
        f"BASE_URL={config['base_url']}",
        f"USER_EMAIL={config['valid_user']['email']}",
        f"RUN_AT={datetime.now().isoformat(timespec='seconds')}",
    ]
    (out_dir / "environment.properties").write_text("\n".join(env_lines), encoding="utf-8")

    categories = [
        {"name": "Assertion failures", "matchedStatuses": ["failed"], "messageRegex": ".*AssertionError.*"},
        {"name": "Locators / Flaky UI", "matchedStatuses": ["failed"], "messageRegex": ".*Timeout.*|.*strict mode violation.*"},
        {"name": "API Contract / Schema", "matchedStatuses": ["failed"], "messageRegex": ".*schema.*|.*KeyError.*"},
    ]
    (out_dir / "categories.json").write_text(json.dumps(categories, ensure_ascii=False, indent=2), encoding="utf-8")
