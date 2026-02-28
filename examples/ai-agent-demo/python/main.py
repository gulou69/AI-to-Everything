"""
A2E AI Agent Integration Demo

This script demonstrates how an AI Agent discovers and invokes services
through the A2E (Agent-to-EveryThing) protocol.

本脚本演示 AI Agent 如何通过 A2E 协议发现和调用服务。
"""

import httpx
import json
import os
import sys


BASE_URL = os.getenv("A2E_BASE_URL", "https://api.a2e-platform.com")
API_PREFIX = f"{BASE_URL}/api/v1"


def print_step(step: int, title: str):
    print(f"\n{'='*60}")
    print(f"  Step {step}: {title}")
    print(f"{'='*60}\n")


def print_json(data: dict):
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    """
    Simulates an AI Agent completing a full service interaction
    through the A2E protocol.
    """
    client = httpx.Client(base_url=API_PREFIX, timeout=30)

    # ── Step 1: Platform Discovery ──────────────────────────────
    print_step(1, "Platform Discovery / 平台发现")
    print("AI Agent discovers the A2E platform capabilities...")

    resp = client.get("/open/discovery")
    if resp.status_code == 200:
        discovery = resp.json().get("data", {})
        print(f"Platform: {discovery.get('platform', {}).get('name', 'N/A')}")
        print(f"Version:  {discovery.get('platform', {}).get('version', 'N/A')}")
        endpoints = discovery.get("endpoints", {})
        print(f"Available endpoints: {len(endpoints)}")
    else:
        print(f"Discovery failed (status {resp.status_code}), continuing...")

    # ── Step 2: Service Search ──────────────────────────────────
    print_step(2, "Service Search / 服务搜索")
    keyword = "奶茶"
    print(f'AI Agent searches for services with keyword: "{keyword}"')

    resp = client.get("/open/services", params={"keyword": keyword, "page": 1, "size": 5})
    if resp.status_code != 200:
        print(f"Search failed with status {resp.status_code}")
        return

    result = resp.json().get("data", {})
    services = result.get("list", [])
    print(f"Found {result.get('total', 0)} services:")
    for svc in services:
        print(f"  - [{svc.get('id')}] {svc.get('name')}: {svc.get('description', '')[:50]}")

    if not services:
        print("No services found. Make sure the platform has published services.")
        return

    service = services[0]
    service_id = service.get("id")
    print(f"\nAI Agent selects service: {service.get('name')} (ID: {service_id})")

    # ── Step 3: Get A2E Protocol ────────────────────────────────
    print_step(3, "Get A2E Protocol / 获取 A2E 协议")
    print(f"AI Agent retrieves the A2E protocol document for service {service_id}...")

    resp = client.get(f"/open/services/{service_id}/protocol")
    if resp.status_code != 200:
        print(f"Failed to get protocol (status {resp.status_code})")
        return

    protocol = resp.json().get("data", {})
    semantic = protocol.get("semantic", {})
    endpoints = protocol.get("endpoints", [])
    permissions = protocol.get("permissions", {})

    print("Protocol received! AI Agent now understands the service:")
    print(f"  Description: {semantic.get('description', 'N/A')[:100]}...")
    print(f"  Capabilities: {semantic.get('capabilities', [])}")
    print(f"  Constraints:  {semantic.get('constraints', [])}")
    print(f"  Endpoints:    {[e.get('name') for e in endpoints]}")
    print(f"  Required permissions: {[p.get('name') for p in permissions.get('required', [])]}")

    # ── Step 4: Create Consumer Token ───────────────────────────
    print_step(4, "Authentication / 身份认证")
    print("AI Agent creates a Consumer Token on behalf of the user...")

    resp = client.post("/open/consumer-tokens", json={
        "phone": "13800138000",
        "nickname": "Demo User",
        "agent_name": "A2E-Demo-Agent",
        "agent_platform": "demo"
    })

    if resp.status_code != 200 and resp.status_code != 201:
        print(f"Token creation failed (status {resp.status_code})")
        consumer_token = "demo_token"
    else:
        token_data = resp.json().get("data", {})
        consumer_token = token_data.get("token", "demo_token")
        print(f"Consumer Token obtained: {consumer_token[:20]}...")

    # ── Step 5: Execute Service ─────────────────────────────────
    print_step(5, "Execute Service / 执行服务")
    print(f"AI Agent calls service endpoint using Consumer Token...")

    resp = client.post(f"/open/services/{service_id}/execute", json={
        "consumer_token": consumer_token,
        "input": {
            "action": "get_menu"
        }
    })

    if resp.status_code == 200:
        exec_result = resp.json().get("data", {})
        print(f"Execution status: {exec_result.get('status', 'N/A')}")
        print("Output:")
        print_json(exec_result.get("output", {}))
    else:
        print(f"Execution returned status {resp.status_code}")
        print(resp.text[:500])

    # ── Summary ─────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("  Demo Complete / 演示完成")
    print(f"{'='*60}")
    print("""
The AI Agent successfully completed the full A2E workflow:
  1. Discovered the platform
  2. Searched for services by keyword
  3. Retrieved the A2E protocol document
  4. Authenticated on behalf of the user
  5. Executed a service endpoint

In a real scenario, the AI Agent would continue to:
  - Parse the menu and present it to the user
  - Take the user's order (e.g., "一杯珍珠奶茶，半糖少冰")
  - Call the create_order endpoint
  - Handle payment through the platform
""")

    client.close()


if __name__ == "__main__":
    main()
