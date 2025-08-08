from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from flask import Flask, jsonify, render_template, request


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=str(Path(__file__).resolve().parent / "templates"),
        static_folder=str(Path(__file__).resolve().parent / "static"),
        static_url_path="/static",
    )

    project_root = Path(__file__).resolve().parents[1]
    config_path = project_root / "config.json"

    def load_json_safely(path: Path, default: Any) -> Any:
        try:
            if path.exists():
                with open(path, "r", encoding="utf-8") as fh:
                    return json.load(fh)
        except Exception:
            pass
        return default

    def load_config() -> Dict[str, Any]:
        return load_json_safely(config_path, {})

    def get_data_paths() -> Dict[str, Path]:
        config = load_config()
        # Defaults from docs
        finance_input = config.get("modulos", {}).get("analise_financeira", {}).get(
            "arquivo_entrada", "MOVIMENTAÇÃO FINANCEIRA (1).xlsx"
        )
        finance_output = config.get("modulos", {}).get("analise_financeira", {}).get(
            "arquivo_saida", "analise_financeira.json"
        )
        processos_input = config.get("modulos", {}).get("analise_processos", {}).get(
            "arquivo_entrada", "PROCESSOS 10.xlsx"
        )
        processos_output = config.get("modulos", {}).get("analise_processos", {}).get(
            "arquivo_saida", "analise_processos.json"
        )
        crm_file = config.get("modulos", {}).get("crm", {}).get("arquivo_dados", "crm_data.json")

        # Prefer working dirs of scripts but keep paths relative to project root
        return {
            "finance_output": project_root / "scripts" / finance_output,
            "process_output": project_root / "scripts" / processos_output,
            "crm_data": project_root / "crm" / crm_file,
        }

    def compute_overview() -> Dict[str, Any]:
        paths = get_data_paths()
        finance = load_json_safely(paths["finance_output"], {})
        processos = load_json_safely(paths["process_output"], {})
        crm = load_json_safely(paths["crm_data"], {})

        # Novos leads: usar interações/oportunidades/criação recente
        today_iso = datetime.now().date().isoformat()
        leads_total = 0
        if isinstance(crm, dict) and "clients" in crm:
            for client in crm["clients"].values():
                created = client.get("created_at", "")[:10]
                if created == today_iso:
                    leads_total += 1
        # Fallback: contar oportunidades abertas como leads ativos
        if leads_total == 0 and isinstance(crm, dict) and "opportunities" in crm:
            leads_total = len([o for o in crm["opportunities"] if o.get("status") == "aberta"])

        # Processos novos: a partir de insights/contagem total se existir
        processos_total = 0
        if isinstance(processos, dict):
            # If there is status counts, sum them
            status = processos.get("status", {}).get("counts", {})
            if status:
                processos_total = sum(status.values())
            else:
                # fallback: count upcoming + overdue as proxy
                deadlines = processos.get("deadlines", {})
                processos_total = int(deadlines.get("overdue_count", 0)) + int(deadlines.get("upcoming_count", 0))

        # Prazos a vencer
        deadlines = processos.get("deadlines", {}) if isinstance(processos, dict) else {}
        prazos_criticos = int(deadlines.get("overdue_count", 0)) + int(deadlines.get("upcoming_count", 0))

        # Documentos pendentes (sem fonte ainda) -> placeholder 0
        docs_pendentes = 0

        # Faturamento previsto (usar revenue.total)
        faturamento_previsto = 0.0
        if isinstance(finance, dict):
            faturamento_previsto = float(finance.get("revenue", {}).get("total", 0.0) or 0.0)

        # Serviços ativos PM2/serviços (placeholder)
        services = get_services_status()
        servicos_ativos = len([s for s in services if s.get("status") == "online"])

        # Alertas de risco
        alertas_risco: List[str] = []
        if int(deadlines.get("overdue_count", 0)) > 0:
            alertas_risco.append(
                f"{int(deadlines.get('overdue_count', 0))} processos com prazo vencido"
            )
        # Placeholder: inadimplência indisponível

        return {
            "leads_novos": {
                "hoje": leads_total,
                "semana": leads_total,  # placeholder
                "mes": leads_total,     # placeholder
            },
            "processos_novos": processos_total,
            "prazos_criticos": prazos_criticos,
            "documentos_pendentes": docs_pendentes,
            "faturamento_previsto": faturamento_previsto,
            "servicos_pm2_ativos": servicos_ativos,
            "alertas_risco": alertas_risco,
            "generated_at": datetime.now().isoformat(),
        }

    def get_services_status() -> List[Dict[str, Any]]:
        # Placeholder service registry; could be extended to actually probe processes
        return [
            {"name": "analyze_data", "status": "online"},
            {"name": "process_data", "status": "online"},
            {"name": "crm", "status": "online"},
            {"name": "dashboard", "status": "online"},
        ]

    def compute_module_metrics(module_key: str) -> Dict[str, Any]:
        paths = get_data_paths()
        finance = load_json_safely(paths["finance_output"], {})
        processos = load_json_safely(paths["process_output"], {})
        crm = load_json_safely(paths["crm_data"], {})

        if module_key == "crm":
            report = {
                "leads_ativos": 0,
                "taxa_conversao": None,
                "top_consultores": [],
                "campanhas": [],
            }
            if isinstance(crm, dict):
                report["leads_ativos"] = len(crm.get("clients", {}))
                # taxa_conversao placeholder
                report["taxa_conversao"] = None
            return report

        if module_key == "processos":
            deadlines = processos.get("deadlines", {}) if isinstance(processos, dict) else {}
            return {
                "por_fase": processos.get("status", {}).get("counts", {}) if isinstance(processos, dict) else {},
                "novos_andamentos": [],
                "prazos_criticos": int(deadlines.get("overdue_count", 0)) + int(deadlines.get("upcoming_count", 0)),
            }

        if module_key == "financeiro":
            return {
                "receitas_previstas": float(finance.get("revenue", {}).get("total", 0.0) or 0.0) if isinstance(finance, dict) else 0.0,
                "inadimplencia": None,
                "a_pagar": None,
                "a_receber": None,
            }

        # Default stub for other modules
        return {"status": "sem_dados"}

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/overview")
    def api_overview():
        # Filtros simples (placeholders): period: 7d|30d|90d|12m, responsavel, status
        period = request.args.get("period", "12m")
        overview = compute_overview()

        # Série mensal de faturamento (para gráfico)
        paths = get_data_paths()
        finance = load_json_safely(paths["finance_output"], {})
        monthly = {}
        if isinstance(finance, dict):
            monthly = finance.get("revenue", {}).get("monthly", {}) or {}
        # Normalizar/ordenar por chave
        try:
            series = sorted(((k, float(v)) for k, v in monthly.items()), key=lambda x: x[0])
        except Exception:
            series = []

        overview["revenue_series"] = [{"period": k, "value": v} for k, v in series]
        overview["filters"] = {"period": period}
        return jsonify(overview)

    @app.route("/api/insights")
    def api_insights():
        ov = compute_overview()
        insights: List[str] = []
        if ov.get("prazos_criticos", 0) > 0:
            insights.append("Priorize processos com prazos críticos hoje.")
        if (ov.get("leads_novos", {}).get("hoje", 0) or 0) >= 5:
            insights.append("Há muitos leads hoje: distribua follow-ups entre a equipe.")
        if (ov.get("faturamento_previsto", 0) or 0) == 0:
            insights.append("Sem faturamento previsto: execute a análise financeira.")
        return jsonify({"insights": insights, "generated_at": datetime.now().isoformat()})

    @app.route("/api/services")
    def api_services():
        return jsonify(get_services_status())

    @app.route("/api/modules/<module_key>")
    def api_module(module_key: str):
        return jsonify({"module": module_key, "metrics": compute_module_metrics(module_key)})

    @app.route("/api/search")
    def api_search():
        query = (request.args.get("q") or "").strip().lower()
        results: Dict[str, List[Dict[str, Any]]] = {"clients": [], "processes": []}
        if not query:
            return jsonify(results)

        paths = get_data_paths()
        crm = load_json_safely(paths["crm_data"], {})
        processos = load_json_safely(paths["process_output"], {})

        if isinstance(crm, dict) and "clients" in crm:
            for client in crm["clients"].values():
                nome = (client.get("nome") or "").lower()
                email = (client.get("email") or "").lower()
                telefone = (client.get("telefone") or "").lower()
                if query in nome or query in email or query in telefone:
                    results["clients"].append({
                        "id": client.get("id"),
                        "nome": client.get("nome"),
                        "email": client.get("email"),
                        "telefone": client.get("telefone"),
                    })

        if isinstance(processos, dict):
            # Search by Numero_Processo or Cliente in overdue/upcoming arrays
            for key in ("overdue_processes", "upcoming_processes"):
                for proc in processos.get("deadlines", {}).get(key, []) if processos.get("deadlines") else []:
                    numero = str(proc.get("Numero_Processo", "")).lower()
                    cliente = str(proc.get("Cliente", "")).lower()
                    if query in numero or query in cliente:
                        results["processes"].append(proc)

        return jsonify(results)

    @app.route("/api/notifications")
    def api_notifications():
        # Poll-based demo notifications
        overview = compute_overview()
        notifications: List[Dict[str, Any]] = []
        if overview.get("prazos_criticos", 0) > 0:
            notifications.append({
                "type": "prazo",
                "message": f"Há {overview['prazos_criticos']} prazos críticos",
                "severity": "warning",
            })
        if overview.get("leads_novos", {}).get("hoje", 0) > 0:
            notifications.append({
                "type": "lead",
                "message": f"{overview['leads_novos']['hoje']} novos leads hoje",
                "severity": "info",
            })
        return jsonify({"items": notifications, "generated_at": datetime.now().isoformat()})

    @app.route("/api/actions/<action>", methods=["POST"])
    def api_actions(action: str):
        payload = request.get_json(silent=True) or {}
        # Stubs that would delegate to modules/services
        accepted = {
            "novo_cliente",
            "novo_processo",
            "enviar_peticao",
            "agendar_audiencia",
            "contato_cliente",
            "consultar_tribunal",
            "gerar_relatorio",
            "exportar_dados",
        }
        if action not in accepted:
            return jsonify({"ok": False, "error": "Ação não suportada"}), 400
        return jsonify({"ok": True, "action": action, "payload": payload, "processed_at": datetime.now().isoformat()})

    @app.route("/api/system_status")
    def api_system_status():
        return jsonify({
            "server": "online",
            "pm2": "n/a",
            "services": get_services_status(),
            "time": datetime.now().isoformat(),
        })

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)