import os
from groq import Groq


class AIService:
    def __init__(self, api_key: str = ""):
        if not api_key:
            api_key = os.environ.get("GROQ_API_KEY", "")
        if not api_key:
            raise ValueError("GROQ_API_KEY no está configurada. Agrégala en config.py o como variable de entorno.")
        self.client = Groq(api_key=api_key)

    def generate_chart_insights(self, chart_data: dict) -> str:
        prompt = self._build_prompt(chart_data)
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Eres un analista de negocios experto en interpretar datos de ventas e inventario. "
                            "Proporciona análisis concisos y accionables en español."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"No se pudo generar el análisis en este momento: {str(e)}"

    def _build_prompt(self, chart_data: dict) -> str:
        prompt_parts = ["Analiza los siguientes datos del negocio y proporciona insights clave:\n"]

        if "ventas_dia" in chart_data:
            prompt_parts.append(
                f"- Ventas del día: Bs. {chart_data['ventas_dia']:.2f}"
            )
        if "ventas_semana" in chart_data:
            prompt_parts.append(
                f"- Ventas de la semana: Bs. {chart_data['ventas_semana']:.2f}"
            )
        if "ventas_mes" in chart_data:
            prompt_parts.append(
                f"- Ventas del mes: Bs. {chart_data['ventas_mes']:.2f}"
            )

        if "productos_mas_vendidos" in chart_data and chart_data["productos_mas_vendidos"]:
            prompt_parts.append("\nProductos más vendidos (top 5):")
            for p in chart_data["productos_mas_vendidos"]:
                prompt_parts.append(
                    f"  - {p['nombre']}: {p['total_vendido']} unidades, Bs. {p['monto_total']:.2f}"
                )

        if "clientes_frecuentes" in chart_data and chart_data["clientes_frecuentes"]:
            prompt_parts.append("\nClientes frecuentes (top 5):")
            for c in chart_data["clientes_frecuentes"]:
                prompt_parts.append(
                    f"  - {c['nombre_completo']}: {c['total_compras']} compras, Bs. {c['monto_total']:.2f}"
                )

        if "productos_ok" in chart_data:
            prompt_parts.append(
                f"\nEstado del inventario: {chart_data['productos_ok']} productos con stock normal, "
                f"{chart_data['productos_stock_bajo']} con stock bajo, {chart_data['productos_agotados']} agotados."
            )

        if "ingresos_mensuales" in chart_data and "ventas_mensuales" in chart_data:
            prompt_parts.append("\nEvolución de ingresos vs ventas (últimos 6 meses):")
            meses = chart_data.get("meses_etiquetas", [])
            for i, mes in enumerate(meses):
                ing = chart_data["ingresos_mensuales"][i] if i < len(chart_data["ingresos_mensuales"]) else 0
                ven = chart_data["ventas_mensuales"][i] if i < len(chart_data["ventas_mensuales"]) else 0
                prompt_parts.append(f"  - {mes}: Ingresos Bs. {ing:.2f}, Ventas Bs. {ven:.2f}")

        prompt_parts.append(
            "\nProporciona un análisis breve (3-5 puntos) sobre tendencias, oportunidades y alertas."
        )
        return "\n".join(prompt_parts)