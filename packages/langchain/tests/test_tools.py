import json

import httpx
import pytest
import respx

from langchain_xdataapi import (
    GetBalance,
    GetTweets,
    GetUser,
    SearchTweets,
    XdataapiAuthError,
    XdataapiClient,
    XdataapiError,
    XdataapiToolkit,
)

BASE = "https://api.xdataapi.io"


def client(**kwargs):
    return XdataapiClient("xd_live_test", **kwargs)


@respx.mock
def test_get_user_strips_the_at_sign():
    route = respx.get(f"{BASE}/v1/users/vercel").mock(
        return_value=httpx.Response(200, json={"data": {"handle": "vercel"}, "credits_charged": 1})
    )
    out = GetUser(client=client()).invoke({"handle": "@vercel"})
    assert route.called
    assert json.loads(out)["credits_charged"] == 1


@respx.mock
def test_search_passes_the_operators_through_untouched():
    route = respx.get(f"{BASE}/v1/tweets/search").mock(
        return_value=httpx.Response(200, json={"data": [], "credits_charged": 0})
    )
    SearchTweets(client=client()).invoke({"q": "from:x since:2026-09-01 -filter:replies", "count": 10})
    assert route.calls.last.request.url.params["q"] == "from:x since:2026-09-01 -filter:replies"
    assert route.calls.last.request.url.params["count"] == "10"


@respx.mock
def test_none_valued_arguments_are_not_sent():
    route = respx.get(f"{BASE}/v1/tweets/search").mock(return_value=httpx.Response(200, json={"data": []}))
    SearchTweets(client=client()).invoke({"q": "hello"})
    params = route.calls.last.request.url.params
    assert "cursor" not in params and "fresh" not in params and "product" not in params


@respx.mock
def test_max_results_caps_a_bigger_request():
    route = respx.get(f"{BASE}/v1/tweets/search").mock(return_value=httpx.Response(200, json={"data": []}))
    SearchTweets(client=client(max_results=25)).invoke({"q": "hello", "count": 50})
    assert route.calls.last.request.url.params["count"] == "25"


@respx.mock
def test_max_results_applies_when_the_model_names_no_count():
    route = respx.get(f"{BASE}/v1/tweets/search").mock(return_value=httpx.Response(200, json={"data": []}))
    SearchTweets(client=client(max_results=5)).invoke({"q": "hello"})
    assert route.calls.last.request.url.params["count"] == "5"


@respx.mock
def test_max_results_never_raises_a_smaller_request():
    route = respx.get(f"{BASE}/v1/tweets/search").mock(return_value=httpx.Response(200, json={"data": []}))
    SearchTweets(client=client(max_results=25)).invoke({"q": "hello", "count": 5})
    assert route.calls.last.request.url.params["count"] == "5"


@respx.mock
def test_batch_sends_one_comma_separated_list():
    route = respx.get(f"{BASE}/v1/tweets/batch").mock(return_value=httpx.Response(200, json={"data": []}))
    GetTweets(client=client()).invoke({"ids": ["20", "21"]})
    assert route.calls.last.request.url.params["ids"] == "20,21"


@respx.mock
def test_no_credits_comes_back_as_data_so_the_model_can_stop():
    respx.get(f"{BASE}/v1/users/x").mock(
        return_value=httpx.Response(402, json={"error": {"code": "no_credits", "message": "balance is zero"}})
    )
    out = json.loads(GetUser(client=client()).invoke({"handle": "x"}))
    assert out["error"]["code"] == "no_credits"


@respx.mock
def test_not_found_comes_back_as_data():
    respx.get(f"{BASE}/v1/users/nope").mock(
        return_value=httpx.Response(404, json={"error": {"code": "not_found", "message": "no such object"}})
    )
    out = json.loads(GetUser(client=client()).invoke({"handle": "nope"}))
    assert out["error"]["code"] == "not_found"


@respx.mock
def test_a_bad_key_raises_because_no_model_can_repair_it():
    respx.get(f"{BASE}/v1/users/x").mock(
        return_value=httpx.Response(401, json={"error": {"code": "invalid_key", "message": "unknown key"}})
    )
    with pytest.raises(XdataapiAuthError) as caught:
        GetUser(client=client()).invoke({"handle": "x"})
    assert caught.value.code == "invalid_key"


@respx.mock
def test_a_rate_limit_raises_so_the_framework_can_retry():
    respx.get(f"{BASE}/v1/users/x").mock(
        return_value=httpx.Response(429, json={"error": {"code": "too_many_requests", "message": "slow down"}})
    )
    with pytest.raises(XdataapiError) as caught:
        GetUser(client=client()).invoke({"handle": "x"})
    assert caught.value.status == 429


@respx.mock
def test_an_upstream_fault_raises():
    respx.get(f"{BASE}/v1/users/x").mock(return_value=httpx.Response(503, json={"error": {"code": "upstream"}}))
    with pytest.raises(XdataapiError):
        GetUser(client=client()).invoke({"handle": "x"})


def test_a_missing_key_is_reported_before_any_request():
    with pytest.raises(XdataapiAuthError):
        XdataapiClient(None, base_url=BASE)


@respx.mock
def test_balance_takes_no_arguments_and_reads_me():
    route = respx.get(f"{BASE}/v1/me").mock(return_value=httpx.Response(200, json={"balance": 4679.87}))
    out = json.loads(GetBalance(client=client()).invoke({}))
    assert route.called and out["balance"] == 4679.87


@respx.mock
async def test_the_async_path_calls_the_same_url():
    route = respx.get(f"{BASE}/v1/users/x").mock(return_value=httpx.Response(200, json={"data": {}}))
    await GetUser(client=client()).ainvoke({"handle": "x"})
    assert route.called


def test_the_toolkit_offers_every_tool_once():
    tools = XdataapiToolkit.from_api_key("xd_live_test").get_tools()
    names = [t.name for t in tools]
    assert len(names) == 14
    assert len(set(names)) == 14
    assert "x_search_tweets" in names


def test_include_narrows_the_surface():
    tools = XdataapiToolkit.from_api_key("xd_live_test", include=["x_search_tweets"]).get_tools()
    assert [t.name for t in tools] == ["x_search_tweets"]


def test_exclude_drops_the_expensive_reads():
    tools = XdataapiToolkit.from_api_key("xd_live_test", exclude=["x_get_followers"]).get_tools()
    assert "x_get_followers" not in [t.name for t in tools]


def test_the_toolkit_shares_one_capped_client():
    tools = XdataapiToolkit.from_api_key("xd_live_test", max_results=10).get_tools()
    assert {t.client for t in tools}.__len__() == 1
    assert tools[0].client.max_results == 10


def test_every_tool_describes_what_it_costs():
    for tool in XdataapiToolkit.from_api_key("xd_live_test").get_tools():
        assert "credit" in tool.description.lower() or "free" in tool.description.lower()
