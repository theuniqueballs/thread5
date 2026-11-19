#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ECCHI-ORACLE — python-клиент для thread5 (tools/gates.py и скрипты писца).

Требования: requests (pip install requests)
Запуск сервиса: cd mini-services/oracle-service && bun run dev  (порт 3031)
"""
import json
import requests

ORACLE = "http://localhost:3031"
TIMEOUT = 60


class OracleClient:
    def __init__(self, base: str = ORACLE):
        self.base = base.rstrip("/")

    def health(self) -> dict:
        return self._get("/health")

    def taxonomy(self) -> dict:
        return self._get("/taxonomy")

    def dataset_index(self) -> dict:
        return self._get("/dataset")

    # ------------------------------------------------------------ rule engine

    def rate(self, text: str) -> dict:
        """Тир по POS-тегам/описанию: verdict / corridor / layers / warnings."""
        return self._post("/rate", {"text": text})

    def audit(self, badge: str, corridor: str, pos: str) -> dict:
        """claimPhysics-аудит слота: PASS|WARN|FAIL + self_certified + fixes."""
        return self._post("/audit", {"badge": badge, "corridor": corridor, "pos": pos})

    def volt(self, scene: str, ycard: str, target: str = "R+") -> dict:
        """Скелет VOLT-слота по Y-карте."""
        return self._post("/volt", {"scene": scene, "ycard": ycard, "target": target})

    # ------------------------------------------------------------ llm / vision

    def ask(self, question: str, mode: str = "distill") -> dict:
        """Спросить оракула (distill = полный мозг, short = персона)."""
        return self._post("/ask", {"question": question, "mode": mode})

    def vision(self, image_path: str, detailed: bool = True) -> dict:
        """Анализ картинки: VLM-описание + тир движка + вердикт оракула."""
        import base64
        from pathlib import Path
        p = Path(image_path)
        mime = "image/png" if p.suffix == ".png" else "image/jpeg"
        b64 = base64.b64encode(p.read_bytes()).decode()
        return self._post("/vision", {"image_base64": b64, "mime": mime, "detailed": detailed}, timeout=180)

    # ------------------------------------------------------------ батчевые утилиты

    def audit_batch(self, slots: list[dict]) -> dict:
        """Слоты: [{tier, corridor, pos}] → сводка батча для квитанции печи."""
        results = []
        for s in slots:
            a = self.audit(s.get("tier", "R+"), s.get("corridor", "NONE"), s.get("pos", ""))
            results.append({"id": s.get("id"), "verdict": a["verdict"],
                            "self_certified": a["self_certified"]})
        label_rplus = sum(1 for s in slots if "R+" in (s.get("tier") or ""))
        self_cert = sum(1 for r in results if r["self_certified"])
        return {
            "label_Rplus": label_rplus,
            "fact_Rplus_estimate": label_rplus - self_cert,
            "self_certified_Rplus": self_cert,
            "per_slot": results,
        }

    # ------------------------------------------------------------ internal

    def _get(self, path: str) -> dict:
        r = requests.get(self.base + path, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()

    def _post(self, path: str, body: dict, timeout: int = TIMEOUT) -> dict:
        r = requests.post(self.base + path, json=body, timeout=timeout)
        r.raise_for_status()
        return r.json()


if __name__ == "__main__":
    o = OracleClient()
    print(json.dumps(o.health(), ensure_ascii=False))

    # 1) классификация
    print(json.dumps(
        o.rate("1girl, dark fitted sweater, clothed nipples, breast clinging, sweat glistening, "
               "nothing underneath, slight from below, upper body"),
        ensure_ascii=False, indent=1))

    # 2) аудит слота (кейс болезни T5-23)
    print(json.dumps(
        o.audit("R+", "A",
                "anime style, 1girl, vinyl top, half-turn, open palm offered to the viewer, smile"),
        ensure_ascii=False, indent=1)[:800])

    # 3) вопрос оракулу
    print(o.ask("Почему cameltoe не работает как заявка?")["answer"][:300])
