import httpx
import pytest
import respx
from llama_index.core.tools.tool_spec.base import BaseToolSpec

from llama_index.tools.xdataapi import XdataapiAuthError, XdataapiError, XdataapiToolSpec

BASE = "https://api.xdataapi.io"


def spec(**kwargs):
    return XdataapiToolSpec("xd_live_test", **kwargs)


def test_it_is_a_tool_spec():
    assert isinstance(spec(), BaseToolSpec)


def test_every_named_function_exists():
    s = spec()
    for name in s.spec_functions:
        assert callable(getattr(s, name)), name


def test_the_tool_list_carries_all_of_them():
    tools = spec().to_tool_list()
    assert len(tools) == 14
    assert {t.metadata.name for t in tools} == set(XdataapiToolSpec.spec_functions)


def test_every_tool_describes_what_it_costs():
    for tool in spec().to_tool_list():
        text = (tool.metadata.description or "").lower()
        assert "credit" in text or "free" in text, tool.metadata.name


@respx.mock
def test_get_user_strips_the_at_sign():
    route = respx.get(f"{BASE}/v1/users/vercel").mock(
        return_value=httpx.Response(200, json={"data": {"handle": "vercel"}, "credits_charged": 1})
    )
    assert spec().get_user("@vercel")["credits_charged"] == 1
    assert route.called


@respx.mock
def test_search_passes_the_operators_through_untouched():
    route = respx.get(f"{BASE}/v1/tweets/search").mock(return_value=httpx.Response(200, json={"data": []}))
    spec().search_tweets(q="from:x since:2026-09-01 -filter:replies", count=10)
    assert route.calls.last.request.url.params["q"] == "from:x since:2026-09-01 -filter:replies"


@respx.mock
def test_none_valued_arguments_are_not_sent():
    route = respx.get(f"{BASE}/v1/tweets/search").mock(return_value=httpx.Response(200, json={"data": []}))
    spec().search_tweets(q="hello")
    params = route.calls.last.request.url.params
    assert "cursor" not in params and "product" not in params


@respx.mock
def test_max_results_caps_a_bigger_request():
    route = respx.get(f"{BASE}/v1/tweets/search").mock(return_value=httpx.Response(200, json={"data": []}))
    spec(max_results=25).search_tweets(q="hello", count=50)
    assert route.calls.last.request.url.params["count"] == "25"


@respx.mock
def test_batch_sends_one_comma_separated_list():
    route = respx.get(f"{BASE}/v1/users/batch").mock(return_value=httpx.Response(200, json={"data": []}))
    spec().get_users(["@x", "github"])
    assert route.calls.last.request.url.params["handles"] == "x,github"


@respx.mock
def test_no_credits_comes_back_as_data_so_the_model_can_stop():
    respx.get(f"{BASE}/v1/users/x").mock(
        return_value=httpx.Response(402, json={"error": {"code": "no_credits", "message": "balance is zero"}})
    )
    assert spec().get_user("x")["error"]["code"] == "no_credits"


@respx.mock
def test_a_bad_key_raises_because_no_model_can_repair_it():
    respx.get(f"{BASE}/v1/users/x").mock(
        return_value=httpx.Response(401, json={"error": {"code": "invalid_key", "message": "unknown key"}})
    )
    with pytest.raises(XdataapiAuthError):
        spec().get_user("x")


@respx.mock
def test_a_rate_limit_raises_so_the_framework_can_retry():
    respx.get(f"{BASE}/v1/users/x").mock(
        return_value=httpx.Response(429, json={"error": {"code": "too_many_requests"}})
    )
    with pytest.raises(XdataapiError):
        spec().get_user("x")


@respx.mock
def test_balance_reads_me():
    route = respx.get(f"{BASE}/v1/me").mock(return_value=httpx.Response(200, json={"balance": 4679.87}))
    assert spec().get_balance()["balance"] == 4679.87
    assert route.called
